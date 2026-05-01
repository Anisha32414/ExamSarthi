# ExamSarthi

An amazing website for engineering students to help with exam preparation.

## Features

- **Home Page**: Filter by year, semester, and subject to find YouTube playlists and websites for notes.
- **PYQ Section**: Search for previous year question papers by year and subject.
- **Theme**: Dark blue, teal, and white color scheme.

## Technologies

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)

## Setup

1. Ensure Python is installed.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install Flask: `pip install flask`
6. (Optional) Install dotenv support: `pip install python-dotenv`
7. Create a `.env` file using `.env.example` and set your SMTP credentials.
8. Run the app: `python app.py`
9. Open http://127.0.0.1:5000 in your browser.

## SMTP setup

To enable the Contact page, add the following values to `.env`:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_SSL=true
CONTACT_RECIPIENT=your-email@gmail.com
```

`SMTP_USER` and `SMTP_PASSWORD` are the sender account used by the website itself. Visitors do not enter email passwords on the contact form. The form only collects:
- your name
- your email address
- the subject
- the message

`CONTACT_RECIPIENT` is the address that receives the website messages.

If SMTP is not configured, contact submissions are still saved locally to `contact_messages.log` so they are not lost.

For Gmail, use an app password and keep `SMTP_USE_SSL=true`.

## Usage

- Navigate to Home to search for resources.
- Go to PYQ to find question papers.

Enjoy studying!