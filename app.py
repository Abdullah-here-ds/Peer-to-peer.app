import streamlit as st

# Base Class
class User:
    def __init__(self, name, skill):
        self.__name = name
        self.__skill = skill

    def get_name(self):
        return self.__name

    def get_skill(self):
        return self.__skill

    def introduce(self):
        return f"Hi, I am {self.__name} and skilled in {self.__skill}."


# Child Classes
class Student(User):
    def introduce(self):
        return f"I am student {self.get_name()}, looking to learn {self.get_skill()}."


class Mentor(User):
    def introduce(self):
        return f"I am mentor {self.get_name()}, and I can teach {self.get_skill()}."


# Learning Platform Class
class LearningPlatform:
    def __init__(self):
        self.users = []

    def register_user(self, user):
        self.users.append(user)

    def get_all_users(self):
        return self.users


# App Code
platform = LearningPlatform()

st.title("🎓 Peer-to-Peer Learning Platform")

st.sidebar.title("Register")
role = st.sidebar.selectbox("Are you a Student or Mentor?", ["Student", "Mentor"])
name = st.sidebar.text_input("Enter your name")
skill = st.sidebar.text_input("Enter your skill")

if st.sidebar.button("Register"):
    if name and skill:
        if role == "Student":
            user = Student(name, skill)
        else:
            user = Mentor(name, skill)
        platform.register_user(user)
        st.sidebar.success("Registered Successfully!")
    else:
        st.sidebar.error("Please fill all fields.")

st.subheader("📋 Registered Users")

if platform.get_all_users():
    for user in platform.get_all_users():
        st.write(user.introduce())
else:
    st.info("No users registered yet.")
