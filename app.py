import csv
from langchain.docstore.document import Document 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#from templates.templates import decomposition_template, compression_template, chat_template
from config import metadata_field_info, document_content_description
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

st.title('🦜🐧Your friendly assistant')

openai_api_key = os.getenv('OPENAI_API_KEY')

decomposition_template = '''
Please based on the inquiry, identify the customer's question. The answerable questions are primarily about the order information based on "Order ID" or "Tracking Number".
Please return the decomposition with the format:
["Unique ID type", "ID value", "Information interested in"]

1. "ID value": Identify the value with the specified format:
    A. Order ID has the format of 7 characters: starts with upper capital "ORD" followed by 4 numbers string, e.g., "ORD1005"
       If identified these 7 characters, set "Unique ID type" = "Order ID". If no such Order ID format is found, return "" for "Unique ID type".
    B. Tracking Number is a 9-digit integer, e.g., 123456789. If identified, "Unique ID type" = "Tracking Number".
       and "ID value" = this 9-digit integer, please transfer it to string., e.g., key "ID value"= "123456789".
       If no such value is present, return "" for both "Unique ID type" and "ID value".
       Please strictly identify these ID formats; if user just say "order", no followed by 4 numbers characters, 
       it should return "" for both "Unique ID type" and "ID value".
       if not found, do not fabricate them.

2. "Information interested in": Apart from Order ID or Tracking Number, the customer may be interested in:
    C. Status
    D. Refund Status
    Identify if the customer is interested in these details. If not mentioned, return "".

Examples:
Query: Hi, g'day. I need to check the status of my order. My tracking number is 123456789.
Decomposition: ["Unique ID type": "Tracking Number", "ID value": "123456789", "Information interested in": "Status"]

Query: Hi, g'day. I need to check the refund status of my order. My order ID is ORD1001.
Decomposition: ["Unique ID type": "Order ID", "ID value": "ORD1001", "Information interested in": "Refund Status"]

Query: Hi, g'day. I need to check the refund status.
Decomposition: ["Unique ID type": "", "ID value": "", "Information interested in": "Refund Status"]


inquery：<<<{question}>>>
decomposition:
'''

compression_template = '''

Given the following question and the key parts of the question,
extract the information from the following context,
and combine the extracted information into a new context.

Remember, *USE* the key parts and known part to extract the information. And if key part involves "Status" or "Refund Status", please use exact value.
Remember, *DO NOT* edit the extracted information.
Remember, *KEEP* the new context relevant to answer the question.

Question: {question}
key parts of the question: {decomposition}
Context: {context}

new context:
'''

chat_template = '''

You are a customer service assistant of a glasses shop. 
Your job is to answer customer's questions based on the knowledge base.
don't make up any information that's not from the context. 
If you don't know an answer, say you don't know.


questions：{question}
knowledge base：{new_context}

your answer：
'''

## load vector store
@st.cache_resource
def load_db():

    persist_directory = './chromadb'
    embedding = OpenAIEmbeddings()

    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

def generate_response(input_text, decomposition_chain, retriever,
                      compression_chain, chat_chain):

    question = input_text
    decomposition = decomposition_chain.invoke(question)
    print("d")
    print(decomposition)
    context = retriever.invoke(question)
    print("context")
    print(context)
    new_context = compression_chain.invoke({'question':question,
                                            'decomposition':decomposition,
                                            'context':context})

    answer = chat_chain.invoke({'question':question,
                                'new_context':new_context['new_context']})

    st.info(answer['text'])

with st.form('my_form'):
    text = st.text_area('Enter text:', "Hi, g'day. I need to check the refund status of my order. My tracking number is 123456789.")
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if submitted and openai_api_key.startswith('sk-'):

        #db = load_db()
        persist_directory = './data/chromadb2/'
        embedding = OpenAIEmbeddings()
        db = Chroma(persist_directory=persist_directory,
                       embedding_function=embedding)
        llm = OpenAI(temperature=0)
        retriever = SelfQueryRetriever.from_llm(llm, db, document_content_description, metadata_field_info, verbose=True)
        print("test")
        print(retriever.get_relevant_documents("give me documentation about Tracking Number '123456823' "))


        decomposition_prompt = PromptTemplate.from_template(decomposition_template)
        llm = OpenAI(openai_api_key=openai_api_key)
        decomposition_chain = LLMChain(llm=llm, prompt=decomposition_prompt, output_key="decomposition")

        compression_prompt = PromptTemplate.from_template(compression_template)
        compression_llm = OpenAI(max_tokens=-1, openai_api_key=openai_api_key)
        compression_chain = LLMChain(llm=compression_llm, prompt=compression_prompt, output_key="new_context")

        chat_prompt = ChatPromptTemplate.from_template(chat_template)
        chat_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0301", temperature=0, openai_api_key=openai_api_key)
        chat_chain = LLMChain(llm=chat_llm, prompt=chat_prompt)

        generate_response(text, decomposition_chain, retriever, compression_chain, chat_chain)