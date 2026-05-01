import os
import smtplib
import datetime
from email.message import EmailMessage
from flask import Flask, render_template, request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

CONTACT_RECIPIENT = os.environ.get('CONTACT_RECIPIENT', 'anisharawat324@gmail.com')


def send_contact_email(name, sender_email, subject, message_text):
    recipient = CONTACT_RECIPIENT
    email_message = EmailMessage()
    email_message['Subject'] = f'ExamSarthi Contact: {subject}'
    email_message['From'] = os.environ.get('SMTP_USER', sender_email)
    email_message['To'] = recipient
    email_message['Reply-To'] = sender_email
    email_message.set_content(
        f'Name: {name}\nEmail: {sender_email}\nSubject: {subject}\n\nMessage:\n{message_text}'
    )

    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    use_ssl = os.environ.get('SMTP_USE_SSL', 'false').lower() in ('1', 'true', 'yes')

    placeholder_credentials = (
        smtp_user is None
        or smtp_password is None
        or smtp_user.startswith('your-')
        or smtp_password == 'your-app-password'
    )

    if smtp_server and smtp_user and smtp_password and not placeholder_credentials:
        if use_ssl or smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(email_message)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(email_message)
    else:
        raise RuntimeError('SMTP credentials are not configured.')


def save_contact_message(name, sender_email, subject, message_text):
    log_file = os.path.join(os.path.dirname(__file__), 'contact_messages.log')
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    with open(log_file, 'a', encoding='utf-8') as log_handle:
        log_handle.write('---\n')
        log_handle.write(f'Time: {timestamp}\n')
        log_handle.write(f'Name: {name}\n')
        log_handle.write(f'Email: {sender_email}\n')
        log_handle.write(f'Subject: {subject}\n')
        log_handle.write('Message:\n')
        log_handle.write(message_text.strip() + '\n')
        log_handle.write('\n')

# Mock data for playlists: year -> semester -> subject -> list of YouTube playlist URLs
playlists_data = {
    '1': {
        '1': {
            'Mathematics': ['https://www.youtube.com/playlist?list=PL1', 'https://www.youtube.com/playlist?list=PL2'],
            'Physics': ['https://www.youtube.com/playlist?list=PL3'],
            'Chemistry': ['https://www.youtube.com/playlist?list=PL4']
        },
        '2': {
            'Mathematics': ['https://www.youtube.com/playlist?list=PL5'],
            'Programming': ['https://www.youtube.com/playlist?list=PL6']
        }
    },
    '2': {
        '3': {
            'Data Structures': ['https://www.youtube.com/playlist?list=PL7'],
            'Algorithms': ['https://www.youtube.com/playlist?list=PL8']
        },
        '4': {
            'Database': ['https://www.youtube.com/playlist?list=PL9']
        }
    },
    '3': {
        '5': {
            'Operating Systems': ['https://www.youtube.com/playlist?list=PL10'],
            'Computer Networks': ['https://www.youtube.com/playlist?list=PL11']
        },
        '6': {
            'Software Engineering': ['https://www.youtube.com/playlist?list=PL12']
        }
    },
    '4': {
        '7': {
            'Machine Learning': ['https://www.youtube.com/playlist?list=PL13'],
            'AI': ['https://www.youtube.com/playlist?list=PL14']
        },
        '8': {
            'Project Management': ['https://www.youtube.com/playlist?list=PL15']
        }
    }
}

# Mock data for websites: year -> semester -> subject -> list of website URLs for notes
websites_data = {
    '1': {
        '1': {
            'Mathematics': ['https://example.com/math-notes1', 'https://example.com/math-notes2'],
            'Physics': ['https://example.com/phys-notes'],
            'Chemistry': ['https://example.com/chem-notes']
        },
        '2': {
            'Mathematics': ['https://example.com/math-notes3'],
            'Programming': ['https://example.com/prog-notes']
        }
    },
    '2': {
        '3': {
            'Data Structures': ['https://example.com/ds-notes'],
            'Algorithms': ['https://example.com/algo-notes']
        },
        '4': {
            'Database': ['https://example.com/db-notes']
        }
    },
    '3': {
        '5': {
            'Operating Systems': ['https://example.com/os-notes'],
            'Computer Networks': ['https://example.com/cn-notes']
        },
        '6': {
            'Software Engineering': ['https://example.com/se-notes']
        }
    },
    '4': {
        '7': {
            'Machine Learning': ['https://example.com/ml-notes'],
            'AI': ['https://example.com/ai-notes']
        },
        '8': {
            'Project Management': ['https://example.com/pm-notes']
        }
    }
}

# Mock data for PYQ: year -> subject -> list of question paper URLs
pyq_data = {
    '1': {
        'Mathematics': ['https://example.com/pyq/math1.pdf', 'https://example.com/pyq/math2.pdf'],
        'Physics': ['https://example.com/pyq/phys1.pdf'],
        'Chemistry': ['https://example.com/pyq/chem1.pdf']
    },
    '2': {
        'Data Structures': ['https://example.com/pyq/ds1.pdf'],
        'Algorithms': ['https://example.com/pyq/algo1.pdf']
    },
    '3': {
        'Operating Systems': ['https://example.com/pyq/os1.pdf'],
        'Computer Networks': ['https://example.com/pyq/cn1.pdf']
    },
    '4': {
        'Machine Learning': ['https://example.com/pyq/ml1.pdf'],
        'AI': ['https://example.com/pyq/ai1.pdf']
    }
}

def get_playlists(year, sem, subj):
    try:
        return playlists_data[year][sem][subj]
    except KeyError:
        return []

def get_websites(year, sem, subj):
    try:
        return websites_data[year][sem][subj]
    except KeyError:
        return []

def get_pyq(year, subj):
    try:
        return pyq_data[year][subj]
    except KeyError:
        return []

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/study-material', methods=['GET', 'POST'])
def study_material():
    playlists = []
    websites = []
    year = ''
    sem = ''
    subj = ''
    if request.method == 'POST':
        year = request.form.get('year')
        sem = request.form.get('sem')
        subj = request.form.get('subj')
        playlists = get_playlists(year, sem, subj)
        websites = get_websites(year, sem, subj)
    return render_template('study_material.html', playlists=playlists, websites=websites, year=year, sem=sem, subj=subj)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    message_sent = False
    error_text = ''
    fallback_saved = False
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        subject = request.form.get('subject', 'Contact request')
        message = request.form.get('message', '')
        try:
            send_contact_email(name, email, subject, message)
            message_sent = True
        except RuntimeError as exc:
            if 'SMTP credentials are not configured' in str(exc):
                save_contact_message(name, email, subject, message)
                message_sent = True
                fallback_saved = True
            else:
                save_contact_message(name, email, subject, message)
                message_sent = True
                fallback_saved = True
                print('Email send failed (saved locally):', exc)
        except Exception as exc:
            save_contact_message(name, email, subject, message)
            message_sent = True
            fallback_saved = True
            print('Email send failed (saved locally):', exc)
    return render_template(
        'contact.html',
        message_sent=message_sent,
        error_text=error_text,
        fallback_saved=fallback_saved
    )

@app.route('/our-progress')
def our_progress():
    stats = {
        'visits': 1280,
        'downloads_last_week': 420,
        'downloads_this_week': 640,
        'downloads_last_month': 1750,
        'download_sources': {
            'Web': 55,
            'Direct': 25,
            'Social': 20
        }
    }
    return render_template('our_progress.html', stats=stats)

@app.route('/pyq', methods=['GET', 'POST'])
def pyq():
    papers = []
    if request.method == 'POST':
        year = request.form.get('year')
        subj = request.form.get('subj')
        papers = get_pyq(year, subj)
    return render_template('pyq.html', papers=papers)

if __name__ == '__main__':
    app.run(debug=True)