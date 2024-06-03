decomposition_template = decomposition_template = '''
Please based on the inquiry, identify the customer's question. The answerable questions are primarily about the order information based on "Order ID" or "Tracking Number".
Please return the decomposition with the format:
["Unique ID type", ID value, "Information interested in"]

1. ID value: Identify the value with the specified format:
    A. Order ID format is with length 7. Order ID format consists of 7 characters. It starts with the uppercase letters "ORD" followed by a four-digit number, for example, "ORD1005".
       - If an Order ID matching this format is identified:
           - Set "Unique ID type" to "Order ID".
           - Set "ID value" to the identified Order ID, ensuring it is enclosed in quotation marks, e.g., "ORD1005".
       - If no Order ID matching this format is found:
           - Return an empty string ("") for both "Unique ID type" and "ID value".
       
    B. Tracking Number format is with length 9. Tracking Number is a 9-digit number integer string, e.g., 123456789. If identified, "Unique ID type" = "Tracking Number".
       and ID value = this 9-digit integer.
       - If no such value is present, return "" for both "Unique ID type" and "ID value".
       
    Please strictly identify these ID value formats; if not found, do not fabricate them.

2. "Information interested in": Apart from Order ID or Tracking Number, the customer may be interested in:
    C. Status
    D. Refund Status
    Identify if the customer is interested in these details. If identified, set identified Status or Refund Status to
    "Information interested in" If not mentioned, return "".

Examples:
Query: Hi, g'day. I need to check the status of my order. My tracking number is 123456789.
Decomposition: ["Unique ID type": "Tracking Number", "ID value": 123456789, "Information interested in": "Status"]

Query: Hi, g'day. I need to check the refund status of my order. My order ID is ORD1001.
Decomposition: ["Unique ID type": "Order ID", "ID value": "ORD1001", "Information interested in": "Refund Status"]

Query: Hi, g'day. Can you support me I need to check the refund status of my order number 123456795 
Decomposition: ["Unique ID type": "Tracking Number", "ID value": 123456795, "Information interested in": "Refund Status"]

Query: Hi, g'day. Can you support me I need to check the refund status of my order 123456795 
Decomposition: ["Unique ID type": "Tracking Number", "ID value": 123456795, "Information interested in": "Refund Status"]

Query: Hi, g'day. I need to check the refund status.
Decomposition: ["Unique ID type": "", "ID value": "", "Information interested in": "Refund Status"]


inquery：<<<{question}>>>
decomposition:
'''

compression_template = '''

Given the key parts of the question, structure a useful inquiry sentence like: "I want documentation about Type id_value thank you"

You will be given key parts of the question with this structure:
["Unique ID type": Type, "ID value": id_value, "Information interested in": Info].

In this list, each element is separated by a comma ",".
Each element is a key-value pair.

1. Please firstly identify the id_value in the given key parts of the question:
    - if id_value has a value or string, not "":
       - if Type is "Order ID", then return a sentence in this format without starting a new line: I want documentation about Order ID "id_value" thank you . Note the id_value is enclosed in quotation marks.
         Note: Do not add a period at the end of the sentence. Ensure the sentence ends immediately after the id_value with a space.
       - if Type is "Tracking Number", then return a sentence in this format without starting a new line: I want documentation about Tracking Number id_value thank you . Note the id_value is not enclosed in quotation marks.
         Note: Do not add a period at the end of the sentence. Ensure the sentence ends immediately after the id_value with a space.
   
   - If id_value is empty or is a "", then return a sentence without new lines and without a period at the end:
     "Sure. But to know your Info, please provide your Order ID or Tracking Number"

Instructions for sentence construction:
- Do not add a period at the end of the inquiry sentence.
- Ensure there is no newline character at the begining or the end of your sentence.
- The response should directly follow the instructions and should not include punctuation such as periods or commas at the end.

Key parts of the question: {decomposition}.
New context:

'''

chat_template = '''

You are a customer service assistant of a glasses shop. 
Your job is to answer customer's questions about order status or refund status based on the knowledge base provided.
In addition to the order status or refund status, you can provide more information in the knowledge base provided.
Always remember that customer should have Order ID or Tracking Number to identify their knowledge. If the knowledge base is empty or a [], 
ask them their exact "Order ID" or "Tracking number" first.
If in the question the customer really provide something, but the knowledge base is empty or a []. Let the customer confirm their exact "Order ID" or "Tracking number". You don't need to mention the knowledge base is empty. Just say no related data.

Don't make up any information that's not from the the knowledge base. 
If you don't know an answer, say you don't know.


questions：{question}
knowledge base：{new_context}

your answer：
'''
