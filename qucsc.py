import mysql.connector as ms

# Connect to the MySQL databaseon
connection = ms.connect(host="localhost",username="root",password="hello",database="QUIZ")

# Create a cursor object to interact with the database
cursor = connection.cursor()


def insert_question_and_choices(quizz_name, question, choices, correct_answer):
    # SQL query to insert a new multiple-choice question into a new table
    new= "create table quizz_name (id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, choice_a TEXT, choice_b TEXT, choice_c TEXT, choice_d TEXT, correct_answer CHAR(1))"
    sql = "INSERT INTO quizz_name (question, choice_a, choice_b, choice_c, choice_d, correct_answer) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (question, choices[0], choices[1], choices[2], choices[3], correct_answer)

    try:
        cursor.execute(new)
        cursor.execute(sql, values)
        connection.commit()
        print("Question and choices inserted successfully!")
    except ms.Error as err:
        print("Error:", err)
        connection.rollback()


# Accept multiple-choice questions from the user until they choose to exit
def NEWQUIZZ():
    quizz_name=input("Enter name of the quizz:")
    while True:
        question = input("Enter a multiple-choice question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        choices = []
        for i in range(4):
            print("Enter choice ", chr(ord('A') + i), end=":")
            choice = input()
            choices.append(choice)

        correct_answer = input("Enter the letter of the correct answer (A, B, C, or D): ").upper()

        insert_question_and_choices(quizz_name, question, choices, correct_answer)



# Close the cursor and connection
cursor.close()
connection.close()
