import streamlit as st
import streamlit_authenticator as stauth
from dependencies import sign_up, fetch_users, create_connection, close_connection

# Update the following with your PostgreSQL credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "Tub@0415"
DB_NAME = "postgres"

# Connect to PostgreSQL
conn = create_connection()
cursor = conn.cursor()

st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')

try:
    users = fetch_users(cursor)
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up(cursor, conn)

    if username:
        if username in usernames:
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.subheader('This is the home page')
                st.markdown(
                    """
                    ---
                    Created with ❤️ by SnakeByte
                    
                    """
                )

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
finally:
    # Close the database connection
    close_connection(conn, cursor)
