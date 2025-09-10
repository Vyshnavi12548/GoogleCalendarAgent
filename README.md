AI Calendar Agent
Problem: We often receive important dates and deadlines buried in documents like meeting minutes, project plans, or memos. Manually adding each of these to a digital calendar is a repetitive and time-consuming task, leading to missed appointments and scheduling errors.

Solution: The AI Calendar Agent is an intelligent tool that automates this entire workflow. By simply uploading a document, the agent uses generative AI to find all relevant event details—like subjects, dates, and times—and instantly creates new events in your Google Calendar. This solution saves valuable time, reduces human error, and allows users to focus on more important tasks.

Key Features
Intelligent Text Analysis: Leverages a powerful generative AI model to parse unstructured text from various document types (PDF, DOCX, and images) and extract key event details.

Automated Event Creation: Directly integrates with the Google Calendar API to create new events with the correct subject, date, and time.

Intuitive User Interface: A clean, modern, and responsive web interface built with Flask and styled with Tailwind CSS, making it easy for any user to upload a file and get started.

Secure Authentication: Utilizes Google's standard OAuth 2.0 flow to securely connect to a user's calendar without ever handling or storing their credentials.

Technology Stack
Backend:

Python

Flask (Web Framework)

Google Generative AI (AI model for text analysis)

Google Calendar API (for event creation)

Libraries: pypdf, python-docx, Pillow, pytesseract

Frontend:

HTML

Tailwind CSS

Authentication:

Google OAuth 2.0 (managed with google-auth-oauthlib)

Setup and Installation
Follow these steps to get a local copy of the project up and running for development and demonstration.

1. Clone the Repository

git clone [https://github.com/Vyshnavi12548/GoogleCalendarAgent.git](https://github.com/Vyshnavi12548/GoogleCalendarAgent.git)
cd GoogleCalendarAgent

2. Set Up a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3. Install Dependencies
Install the required Python packages.

pip install Flask python-dotenv google-generativeai pypdf python-docx Pillow pytesseract google-api-python-client google-auth-oauthlib google-auth

(Note: You will also need to install the Tesseract OCR engine on your system to process images. See the pytesseract documentation for instructions.)

4. Configure Google Cloud Credentials
The application uses Google OAuth 2.0 to access the Google Calendar API.

Go to the Google Cloud Console.

Create a new project and enable the Google Calendar API.

Navigate to APIs & Services > Credentials and create an OAuth 2.0 Client ID for a web application.

Download the client_secret.json file and place it in the root of your project directory.

5. Set Up Environment Variables
Create a file named .env in the root directory of your project with the following keys.

FLASK_SECRET_KEY=your_long_random_secret_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CALENDAR_ID=primary
(Note: To get your FLASK_SECRET_KEY, you can run python -c "import secrets; print(secrets.token_hex(16))".)

6. Run the Application
Start the Flask development server.

python app.py

Open your web browser and navigate to http://127.0.0.1:5000 to start using the AI Calendar Agent. The first time you visit the page, you will be redirected to Google to grant the application access to your calendar.
