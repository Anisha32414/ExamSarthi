import os
import json
import threading
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

PROGRESS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'progress_data.json')
PROGRESS_LOCK = threading.Lock()
DEFAULT_PROGRESS_DATA = {
    'base_visits': 1280,
    'current_visits': 0,
    'downloads': {
        'base_this_week': 420,
        'base_last_week': 380,
        'base_last_month': 1700,
        'current_this_week': 0,
        'current_last_week': 0,
        'current_last_month': 0
    },
    'download_sources': {
        'Web': 55,
        'Direct': 25,
        'Social': 20
    },
    'subject_traffic': {
        'Mathematics': 28,
        'Physics': 22,
        'Chemistry': 18,
        'Programming': 15,
        'Other': 17
    },
    'weekly_progress': [
        {'label': 'Week 1', 'downloads': 320},
        {'label': 'Week 2', 'downloads': 350},
        {'label': 'Week 3', 'downloads': 380},
        {'label': 'Week 4', 'downloads': 420},
        {'label': 'Week 5', 'downloads': 450},
        {'label': 'Week 6', 'downloads': 480},
        {'label': 'Week 7', 'downloads': 500},
        {'label': 'This Week', 'downloads': 520}
    ]
}

def load_progress_data():
    try:
        with open(PROGRESS_DATA_FILE, 'r', encoding='utf-8') as progress_file:
            return json.load(progress_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            'base_visits': DEFAULT_PROGRESS_DATA['base_visits'],
            'current_visits': 0,
            'downloads': DEFAULT_PROGRESS_DATA['downloads'].copy(),
            'download_sources': DEFAULT_PROGRESS_DATA['download_sources'].copy(),
            'subject_traffic': DEFAULT_PROGRESS_DATA['subject_traffic'].copy(),
            'weekly_progress': [item.copy() for item in DEFAULT_PROGRESS_DATA['weekly_progress']]
        }
        save_progress_data(data)
        return data


def save_progress_data(data):
    with PROGRESS_LOCK:
        temp_file = PROGRESS_DATA_FILE + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as progress_file:
            json.dump(data, progress_file, indent=2)
        os.replace(temp_file, PROGRESS_DATA_FILE)


@app.before_request
def track_visitor():
    if request.method != 'GET':
        return
    endpoint = request.endpoint
    if endpoint is None or endpoint == 'static':
        return
    try:
        data = load_progress_data()
        data['current_visits'] = data.get('current_visits', 0) + 1
        save_progress_data(data)
    except Exception:
        pass


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
    data = load_progress_data()
    downloads = data.get('downloads', {})
    stats = {
        'visits': data.get('base_visits', 0) + data.get('current_visits', 0),
        'downloads_this_week': downloads.get('base_this_week', 0) + downloads.get('current_this_week', 0),
        'downloads_last_week': downloads.get('base_last_week', 0) + downloads.get('current_last_week', 0),
        'downloads_last_month': downloads.get('base_last_month', 0) + downloads.get('current_last_month', 0),
        'download_sources': data.get('download_sources', DEFAULT_PROGRESS_DATA['download_sources']),
        'subject_traffic': data.get('subject_traffic', DEFAULT_PROGRESS_DATA['subject_traffic']),
        'weekly_progress': data.get('weekly_progress', DEFAULT_PROGRESS_DATA['weekly_progress'])
    }
    weekly_labels = [week.get('label', '') for week in stats['weekly_progress']]
    weekly_values = [week.get('downloads', 0) for week in stats['weekly_progress']]
    subject_labels = list(stats['subject_traffic'].keys())
    subject_values = list(stats['subject_traffic'].values())
    return render_template(
        'our_progress.html',
        stats=stats,
        weekly_labels=weekly_labels,
        weekly_values=weekly_values,
        subject_labels=subject_labels,
        subject_values=subject_values
    )

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