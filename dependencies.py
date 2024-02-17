import datetime
import re
import streamlit as st
import streamlit_authenticator as stauth
import psycopg2

# Update the following with your PostgreSQL credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "Tub@0415"
DB_NAME = "postgres"

def create_connection():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

def fetch_users(cursor):
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_data = [{'key': user[1], 'username': user[2], 'password': user[3]} for user in users]
    return user_data

def sign_up(cursor, conn):
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails(cursor):
                    if validate_username(username):
                        if username not in get_usernames(cursor):
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        # Add User to DB
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(cursor, conn, email, username, hashed_password[0])
                                        st.success('Account created successfully!!')
                                        st.balloons()
                                    else:
                                        st.warning('Passwords Do Not Match')
                                else:
                                    st.warning('Password is too Short')
                            else:
                                st.warning('Username Too short')
                        else:
                            st.warning('Username Already Exists')

                    else:
                        st.warning('Invalid Username')
                else:
                    st.warning('Email Already exists!!')
            else:
                st.warning('Invalid Email')

        btn1, btn2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            if st.form_submit_button('Sign Up'):
                pass  # Add an empty pass statement to make the form complete

def get_user_emails(cursor):
    cursor.execute("SELECT email FROM users")
    emails = cursor.fetchall()
    return [email[0] for email in emails]

def get_usernames(cursor):
    cursor.execute("SELECT username FROM users")
    usernames = cursor.fetchall()
    return [username[0] for username in usernames]

def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return bool(re.match(pattern, email))

def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return bool(re.match(pattern, username))

def insert_user(cursor, conn, email, username, password):
    date_joined = str(datetime.datetime.now())
    cursor.execute("INSERT INTO users (email, username, password, date_joined) VALUES (%s, %s, %s, %s)",
                   (email, username, password, date_joined))
    conn.commit()
