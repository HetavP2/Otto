from flask import Flask, request
from datetime import date
from flask_mail import Mail, Message


from twilio.twiml.messaging_response import MessagingResponse

import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")



app = Flask(__name__)
import resend

resend.api_key = os.getenv("RESEND_API_KEY")



@app.route("/sms", methods=['POST'])
def send_sms():
    

    # people saying this:
    
    inb_msg = str(request.form['Body'].lower())
    resp = MessagingResponse()

        # Get the phone number of the sender
    senderPhone = request.values['From']
    senderPhone = senderPhone[1:]

        # Airtable config
    # Your Airtable API key and base ID
    AIRTABLE_API_KEY = 'pat7bOTWBcOFlviX4.4e2db2c1bc7ef9c99e8244fe41d8e72212e7655a757bcfd1668a1e9cda67f819'
    AIRTABLE_BASE_ID = 'app6XaQTziEVjhjGs'
    TABLE_NAME = 'sms_responses'

    # URL for the Airtable endpoint
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}'

    # Headers containing the API key and content type
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }


    # Find the index of the /j
    first_j_index = int(inb_msg.find("/j"))

    # Find index of /a
    first_a_index = int(inb_msg.find("/a"))

    # Find index of /s
    first_s_index = int(inb_msg.find("/s"))
    
    # Find index of /e
    first_e_index = int(inb_msg.find("/e"))


    if (first_j_index == 0):
        
        # Function to create a new record in Airtable
        def create_record(data):
            new_record = {
                'fields': data  # The data you want to add
            }
            response = requests.post(url, json=new_record, headers=headers)
            if response.status_code == 200:
                print("Record created successfully")
            else:
                print("Failed to create record")

        # Add journal entry to airtable
        

        inb_msg=str(inb_msg[first_j_index + 2:] if first_j_index != -1 else "")

        output = query_follow_up_otto({
                "question": f"Below is a user's journal entry. You are an AI follow-up question suggestion model. Based on whatever the user input is, offer a small response then, with a line break, put in a follow up question relevant to their entry to help them reflect better and write more. {inb_msg}",
            })
        resp.message(f"Reflection Follow Up Question: {output['text']}")  

        # get current date
        current_date = date.today()

         # Create a new record in Airtable
        new_data = {
            'response': f"{inb_msg}",
            'date': f"{current_date}",
            'user': f"{senderPhone}",
            'followup': str(output['text'])
        }
        create_record(new_data)

    else:

        def in_fetch_records(sender_phone):
            print("sender phone is: ", sender_phone)
            url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}?filterByFormula=({{user}}="{sender_phone}")'
            
            headers = {
                'Authorization': f'Bearer {AIRTABLE_API_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.get(url, headers=headers)
            # if response.status_code == 200:
            
            data = response.json()
            print(data)
            return data['records']
            # else:
            #     print("Failed to fetch records")
            #     return None

        if (first_a_index == 0):
            inb_msg=str(inb_msg[first_a_index + 1:] if first_a_index != -1 else "")
            # retrieve all records
            records = in_fetch_records(senderPhone)
            # analytics data
            output = summarize_or_analytics({
                    "question": f"Below is a list of the past journal entries and conversations you have had with them. Display some analytics and percentages based on emotions based on these records: {records}",
                })
            resp.message(f"/a: f{output['text']}")    
        elif (first_s_index == 0):

           
            inb_msg=str(inb_msg[first_s_index + 1:] if first_s_index != -1 else "")
            
            # summarize data
            records = in_fetch_records(senderPhone)
            # analytics data
            output = summarize_or_analytics({
                    "question": f"Below is a list of the past journal entries and conversations you have had with them. Summarize the topics and content of the journal entries into a short paragraph: {records}",
                })
            resp.message(f"/s: f{output['text']}")  
        elif (first_e_index == 0):
            records = in_fetch_records(senderPhone)
            
            # analytics data
            output = summarize_or_analytics({
                    "question": f"Below is a list of the past journal entries and conversations you have had with them. Summarize the topics and content of the journal entries into a short paragraph: {records}",
                })
            inb_msg=str(inb_msg[first_e_index + 3:] if first_e_index != -1 else "")
            params = {
                "from": "Acme <onboarding@resend.dev>",
                "to": [f"{inb_msg}"],
                "subject": "Journal summary",
                "html": f"<strong>{str(output['text'])}</strong>",
            }
            email = resend.Emails.send(params)
            resp.message("Email sent. A pleasure talking to you!")  

        else:
            # normal conversation
            output = query_therapist_otto({
                    "question": f"You are Otto, a personalised therapist meant to help others and be an active listener in their lives. Be compassionate and the best therapist you can be. Offer the best advice you can and act as a therapist. Below is a patient's message to you: {inb_msg}",
                })
            resp.message(output['text'])  





    return str(resp)

import requests

API_URL = "http://localhost:3000/api/v1/prediction/62d98067-d6d1-40d2-864f-1d5c67087096"

def query_therapist_otto(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    


API_URL_2 = "http://localhost:3000/api/v1/prediction/80efda77-aa4a-41ec-9a5a-12c97c4ab4f7"

def query_follow_up_otto(payload):
    response = requests.post(API_URL_2, json=payload)
    return response.json()
    


API_URL_3 = "http://localhost:3000/api/v1/prediction/fef78439-ecbe-4c4f-ad70-45b4cb6f21d5"

def summarize_or_analytics(payload):
    response = requests.post(API_URL_3, json=payload)
    return response.json()



if __name__ == "__main__":
    app.run(debug=True)

    
    
