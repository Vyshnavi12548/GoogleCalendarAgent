import os
import json
from flask import Flask, request, render_template, session, redirect, url_for
import google.generativeai as genai
from pypdf import PdfReader
import docx
from PIL import Image
import pytesseract

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Get API keys and credentials from the .env file
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID")

# Initialize Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# --- Core Application Logic ---

def extract_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        try:
            reader = PdfReader(file_path)
            text = "".join(page.extract_text() for page in reader.pages)
            return text
        except Exception as e:
            return f"Error extracting text from PDF: {e}"
    elif file_extension == '.docx':
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text)
        except Exception as e:
            return f"Error extracting text from DOCX: {e}"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        try:
            text = pytesseract.image_to_string(Image.open(file_path))
            return text
        except Exception as e:
            return f"Error performing OCR on image: {e}. Make sure Tesseract is installed and in your PATH."
    return ""

def analyze_text_with_ai(text):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Extract all important dates, times, and event descriptions from the following text.
    If no events are found, return an empty JSON array: [].
    Do not include any other text or conversational phrases in your response.
    Return the information as a JSON array of objects. Each object must have a 'summary', 'start_time', and 'end_time' key.
    The time format should be 'YYYY-MM-DDTHH:MM:SSZ'. If no specific time is mentioned, use noon (12:00:00).
    Text: \"\"\"{text}\"\"\"
    """
    try:
        response = model.generate_content(prompt)

        # Robust JSON extraction
        response_text = response.text.strip()
        
        if response_text.startswith('[') and response_text.endswith(']'):
            return response_text
        
        return f"Error from AI analysis: AI did not return a valid JSON array. Response was: {response_text}"
    except Exception as e:
        return f"Error from AI analysis: {e}"

def create_calendar_events(events_json, creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        num_events = 0
        events_list = json.loads(events_json)

        if not events_list:
            return "Success! No events were found in your document, so no events were created."
        
        for event in events_list:
            event_body = {
                'summary': event['summary'],
                'start': {'dateTime': event['start_time']},
                'end': {'dateTime': event['end_time']},
            }
            service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event_body).execute()
            num_events += 1

        return f"Success! Created {num_events} events in your Google Calendar."
    except json.JSONDecodeError as e:
        return f"Error parsing AI response to JSON: {e}"
    except Exception as e:
        return f"Error creating calendar event: {e}"

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    # --- HARDCODED CREDENTIALS FOR HACKATHON DEMO ---
    # In a real app, you would not hardcode these.
    # You would get them from an OAuth flow.
    credentials_data = {
        'token': 'YOUR_ACCESS_TOKEN_HERE',
        'refresh_token': 'YOUR_REFRESH_TOKEN_HERE',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
        'client_secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
        'scopes': ['https://www.googleapis.com/auth/calendar.events']
    }
    creds = Credentials.from_authorized_user_info(credentials_data)
    # --- END HARDCODED CREDENTIALS ---

    if request.method == 'POST':
        file = request.files.get('file')

        if not file:
            return "No file part", 400
        
        # Save the uploaded file
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Extract text from the file
        document_text = extract_text(file_path)
        os.remove(file_path)

        if document_text.startswith("Error"):
            return document_text, 500
        
        # Analyze text with AI
        extracted_events = analyze_text_with_ai(document_text)
        if extracted_events.startswith("Error"):
            return extracted_events, 500

        # Create calendar events and get the result message
        result_message = create_calendar_events(extracted_events, creds)
        
        return result_message

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
