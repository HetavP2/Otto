# Otto SMS Therapy Bot

## Introduction

Otto is an AI-powered SMS therapy assistant designed to help users reflect, journal, and receive compassionate support via text messaging. Users interact with Otto by sending SMS commands, journaling entries, and requesting summaries or analytics. Otto leverages AI models for personalized responses, follow-up questions, and emotional analytics, while storing user data securely in Airtable and sending summaries via email.

---

## ✨ Features

- **AI-Powered SMS Therapy**
  - Users send journal entries and receive reflective follow-up questions.
  - Otto responds compassionately as a virtual therapist.

- **Journaling & Reflection**
  - Journal entries are stored and tracked per user.
  - AI-generated follow-up questions encourage deeper reflection.

- **Analytics & Summaries**
  - Users can request emotional analytics and summaries of their journaling history.
  - Otto analyzes and summarizes topics, emotions, and trends.

- **Email Summaries**
  - Users can request summaries to be sent to their email.

- **Airtable Integration**
  - All journal entries, follow-ups, and user data are stored in Airtable for persistence.

- **Command-Based SMS Interaction**
  - `/j`: Journal entry
  - `/a`: Analytics
  - `/s`: Summary
  - `/e`: Email summary

---

## 🛠️ Tech Stack

- **Backend**
  - Python 3.x
  - Flask: Web framework for routing and request handling
  - Requests: HTTP requests to APIs and Airtable
  - Flask-Mail: Email sending (via Resend API)
  - Twilio: SMS webhook integration
  - OpenAI: AI-powered responses (optional, for advanced features)
  - Resend: Email delivery service
  - Airtable: Cloud database for storing user data

- **APIs**
  - Custom AI endpoints for therapist, follow-up, and analytics responses

---

## 📝 Project Structure

```
otto/
│   app.py                # Main Flask application and SMS webhook
│
├── requirements.txt      # Python dependencies
```

---

## 🚀 How to Run

1. **Install Python**  
   Ensure Python 3.x is installed.

2. **Install dependencies**  
   In the project directory, run:
   ```
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**  
   - `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
   - `RESEND_API_KEY`: Your Resend API key

4. **Configure Airtable**  
   Update `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, and `TABLE_NAME` in `app.py` with your Airtable credentials.

5. **Run the Flask App**  
   ```
   python app.py
   ```

6. **Expose Flask Endpoint for Twilio**  
   Use [ngrok](https://ngrok.com/) or similar to expose your local server for Twilio SMS webhook.

7. **Configure Twilio Webhook**  
   Set your Twilio SMS webhook to point to `http://<your-ngrok-url>/sms`.

---

## 📱 SMS Commands

- `/j <entry>`: Journal entry (stores entry, receives follow-up)
- `/a`: Get analytics on your entries
- `/s`: Get summary of your entries
- `/e <email>`: Email summary to your address
- Any other message: Otto responds as a compassionate therapist

---
