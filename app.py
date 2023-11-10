
from flask import Flask, request, json
from langchain.chat_models import AzureChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)

CORS(app)

load_dotenv()

prompt_template = """

You are a sentiment analysis bot. You are given a journal entry or entries from a person and 
you have to classify it as positive, negative or neutral.

{journal_entries}

output in [positive, negative, neutral]
"""

prompt_template2 = """sumary_line: You are a helpful mental health bot. Analyze the 
given journals by {person_name} and seek insights. Explain the situation to the writer's
loved ones in a friendly manner and also suggest ways his loved ones can help him.

{journal_entries}

output the email body in a dict format under the key "body"
"""


gpt_key = os.environ['AZURE_OPENAI_KEY']
gpt_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
gpt_deployment_name = os.environ['AZURE_OPENAI_DEPLOYMENT_NAME']

llm = AzureChatOpenAI(
            openai_api_base=gpt_endpoint,
            openai_api_key=gpt_key,
            deployment_name=gpt_deployment_name,
            openai_api_type='azure',
            openai_api_version='2023-05-15'
        )

qa_chain = load_qa_chain(llm=llm, chain_type="map_reduce")

@app.route('/message', methods=['GET'])
def test():
    query = request.args.get('message')
    prompt = PromptTemplate.from_template(prompt_template)
    sentiment_chain = LLMChain(llm=llm, prompt=prompt)   
    response = sentiment_chain({"journal_entries": query})

    tmp = json.dumps(response)
    return json.loads(tmp)

def send_email(recipient, body):
    msg = MIMEText(body)
    sender = 'makeucdemo@outlook.com'
    password = 'subhashis@2204'
    msg['Subject'] = 'Help Needed'

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        print("Message sent!")

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    receipient = data['email']
    documents = data['data']
    name = data['name']

    journals = []
    for document in documents :
        journals.append(document['text'])

    prompt = PromptTemplate.from_template(prompt_template2)
    sentiment_chain = LLMChain(llm=llm, prompt=prompt)
    response = sentiment_chain({"person_name" : name, "journal_entries": journals})

    tmp = json.dumps(response)
    output = json.loads(tmp)

    body = json.loads(output['text'])['body']

    send_email(receipient, body)

    return data

if __name__ == '__main__':
    app.run(debug=True)

