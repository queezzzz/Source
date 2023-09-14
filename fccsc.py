import mysql.connector as ms

# Connect to the MySQL database
connection = ms.connect(host="localhost",username="root",password="hello",database="FLASHCARD")

# Create a cursor object to interact with the database
cursor = connection.cursor()


def insert_question_and_answer(flashcard_set_name, question, answer):
    # SQL query to insert a new question and answer into the QnA table
    new="create table flashcard_set_name (id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, answer TEXT);"
    sql = "INSERT INTO QnA (question, answer) VALUES (%s, %s)"
    values = (question, answer)

    try:
        cursor.execute(new)
        cursor.execute(sql, values)
        connection.commit()
        print("Question and answer inserted successfully!")
    except ms.Error as err:
        print("Error", err)
        connection.rollback()


# Accept questions and answers from the user until they choose to exit
def NEWFLASHCARD_SET():
    flashcard_set_name=input("Enter name of new flashcard set:")
    while True:
        question = input("Enter a question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        answer = input("Enter the answer: ")

        insert_question_and_answer(flashcard_set_name, question, answer)


# Close the cursor and connection
cursor.close()
connection.close()
