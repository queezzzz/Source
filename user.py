import mysql.connector
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hello",
    database="myapp"
)

cursor = connection.cursor()

def SIGN_UP(username, password):
    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists. Please choose a different one.")
        return False

    # Insert the new user into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    print("User created successfully!")
    cursor.execute("create database username;")
    connection.commit()
    return True

def SIGN_IN(username, password):
    # Check if the username and password match
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome, {username}!")
    else:
        print("Login failed. Please check your username and password.")



print("1. Sign up")
print("2. Sign in")
print("3. Quit")

choice = input("Select an option: ")
if choice=='1':
    username=input("enter user name:")
    password=input("enter password:")
    SIGN_UP(username, password)
elif choice=='2':
    username = input("enter username")
    while True:
        password = input("enter password")
        confirm_password =input("reenter your password")
        if password==confirm_password:
            break
        else:
            print("enter matching passwords")
    SIGN_IN(username, password)
else:
    print("The option entered is wrong")