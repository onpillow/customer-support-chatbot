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
from templates.templates import decomposition_template, compression_template, chat_template
from config import metadata_field_info, document_content_description
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

st.title('🦜🐧Your friendly assistant')

openai_api_key = os.getenv('OPENAI_API_KEY')


def generate_response(input_text, decomposition_chain, retriever,
                      compression_chain, chat_chain):

    question = input_text
    decomposition = decomposition_chain.invoke(question)
    print("d")
    print(decomposition)
    new_context = compression_chain.invoke({'decomposition':decomposition['decomposition']})
    print("new_context")
    print(new_context)
    retrived_context = retriever.invoke(new_context['new_context'])
    print("retrived_context")
    print(retrived_context)

    answer = chat_chain.invoke({'question':question,
                                'new_context':retrived_context})

    st.info(answer['text'])

with st.form('my_form'):
    text = st.text_area('Enter text:', "Hi, g'day. I need to check the refund status of my order. My tracking number is 123456789.")
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if submitted and openai_api_key.startswith('sk-'):

        #db = load_db()
        persist_directory = './data/chromadb3/'
        embedding = OpenAIEmbeddings()
        db = Chroma(persist_directory=persist_directory,
                       embedding_function=embedding)
        llm = OpenAI(temperature=0)
        retriever = SelfQueryRetriever.from_llm(llm, db, document_content_description, metadata_field_info, verbose=True,  enable_limit=True)

        decomposition_prompt = PromptTemplate.from_template(decomposition_template)
        llm = OpenAI(temperature=0)
        decomposition_chain = LLMChain(llm=llm, prompt=decomposition_prompt, output_key="decomposition")

        compression_prompt = PromptTemplate.from_template(compression_template)
        compression_llm = OpenAI()
        compression_chain = LLMChain(llm=compression_llm,
                                     prompt=compression_prompt,
                                     output_key="new_context")

        chat_prompt = ChatPromptTemplate.from_template(chat_template)
        chat_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0301", temperature=0, openai_api_key=openai_api_key)
        chat_chain = LLMChain(llm=chat_llm, prompt=chat_prompt)

        generate_response(text, decomposition_chain, retriever, compression_chain, chat_chain)