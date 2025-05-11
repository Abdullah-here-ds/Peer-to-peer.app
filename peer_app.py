
import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- OOP CLASSES ----------
class User:
    def __init__(self, name, skill, email):
        self.__name = name
        self.__skill = skill
        self.__email = email

    def get_name(self):
        return self.__name

    def get_skill(self):
        return self.__skill

    def get_email(self):
        return self.__email

    def introduce(self):
        return f"Hi, I am {self.__name}, skilled in {self.__skill}."

class Student(User):
    def introduce(self):
        return f"I am {self.get_name()}, and I want to learn {self.get_skill()}."

class Mentor(User):
    def introduce(self):
        return f"I am {self.get_name()}, and I can teach {self.get_skill()}."

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            email TEXT,
            learn_skill TEXT,
            teach_skill TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, email, learn_skill, teach_skill):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (name, email, learn_skill, teach_skill))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# ---------- EMAIL FUNCTION ----------
def send_match_email(user1_name, user1_email, user2_name, user2_email, skill1, skill2):
    sender_email = "rosemary1234567898@gmail.com"
    sender_password = "nfiviqtzasfjbxmn"

    subject = "You have a new skill match!"

    body = f'''
Hi {user1_name} and {user2_name},

Great news! You've been matched on the Peer-to-Peer Learning Platform.

{user1_name} wants to learn {skill1} and can teach {skill2}.
{user2_name} wants to learn {skill2} and can teach {skill1}.

Feel free to reach out and start learning from each other!

Cheers,
Peer-to-Peer Learning Platform
'''

    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)

        for email in [user1_email, user2_email]:
            message['To'] = email
            server.sendmail(sender_email, email, message.as_string())

        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# ---------- MATCHING FUNCTION ----------
def find_matches(new_user):
    all_users = get_all_users()
    matches = []
    for u in all_users:
        if u[0] == new_user.get_name() and u[1] == new_user.get_email():
            continue
        if new_user.get_skill().lower() == u[3].lower() and new_user.get_email() != u[1]:
            matches.append(u)
    return matches

# ---------- STREAMLIT APP UI ----------
st.set_page_config(page_title="Skill Exchange Platform", layout="wide")
st.title("🤝 Peer-to-Peer Skill Exchange")

init_db()

st.sidebar.title("📋 Register")
name = st.sidebar.text_input("Your Name")
email = st.sidebar.text_input("Your Email")
learn_skill = st.sidebar.text_input("Skill You Want to Learn")
teach_skill = st.sidebar.text_input("Skill You Can Teach")

if st.sidebar.button("Register"):
    if name and email and learn_skill and teach_skill:
        student = Student(name, learn_skill, email)
        mentor = Mentor(name, teach_skill, email)
        add_user(name, email, learn_skill, teach_skill)
        st.sidebar.success("🎉 Registered successfully!")

        # Check for matches
        matches = find_matches(mentor)
        for m in matches:
            send_match_email(name, email, m[0], m[1], learn_skill, teach_skill)
    else:
        st.sidebar.error("Please fill out all fields.")

st.subheader("👥 Registered Users")
users = get_all_users()

for u in users:
    col1, col2 = st.columns(2)
    student = Student(u[0], u[2], u[1])
    mentor = Mentor(u[0], u[3], u[1])

    with col1:
        st.info(student.introduce())
    with col2:
        st.success(mentor.introduce())
