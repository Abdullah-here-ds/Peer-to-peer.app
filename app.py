import streamlit as st
import sqlite3

# ----------------- DATABASE SETUP -----------------
conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    skill TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
conn.commit()

# ----------------- CLASSES -----------------
class User:
    def __init__(self, name, skill):
        self._name = name
        self._skill = skill

    def get_name(self):
        return self._name

    def get_skill(self):
        return self._skill

    def introduce(self):
        return f"Hi, I am {self._name} and skilled in {self._skill}."


class Student(User):
    def introduce(self):
        return f"🎓 I am student {self.get_name()}, looking to learn {self.get_skill()}."


class Mentor(User):
    def introduce(self):
        return f"🧑‍🏫 I am mentor {self.get_name()}, and I can teach {self.get_skill()}."


# ----------------- DATABASE FUNCTIONS -----------------
def register_user_to_db(name, skill, role):
    c.execute("INSERT INTO users (name, skill, role) VALUES (?, ?, ?)", (name, skill, role))
    conn.commit()


def get_all_users_from_db():
    c.execute("SELECT name, skill, role FROM users")
    return c.fetchall()


# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="Peer Learning Platform", layout="wide")

st.title("🤝 Peer-to-Peer Learning Platform")

with st.sidebar:
    st.header("Register Here")
    role = st.selectbox("Your Role", ["Student", "Mentor"])
    name = st.text_input("Your Name")
    skill = st.text_input("Your Skill")

    if st.button("Register"):
        if name and skill:
            register_user_to_db(name, skill, role)
            st.success("✅ Registered Successfully!")
        else:
            st.error("❗ Please fill in all fields.")

st.subheader("📋 Registered Users")
users = get_all_users_from_db()

if users:
    student_col, mentor_col = st.columns(2)

    with student_col:
        st.markdown("### 🎓 Students")
        for user in users:
            if user[2] == "Student":
                st.info(f"**{user[0]}** wants to learn **{user[1]}**.")

    with mentor_col:
        st.markdown("### 🧑‍🏫 Mentors")
        for user in users:
            if user[2] == "Mentor":
                st.success(f"**{user[0]}** can teach **{user[1]}**.")
else:
    st.warning("No users registered yet.")
