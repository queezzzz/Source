def insert_question_and_choices(quizz_name, question, choices, correct_answer):
    import mysql.connector as ms

    # Connect to the MySQL database
    connection = ms.connect(host="localhost", username="root", password="hello", database="QUIZ")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    # SQL query to insert a new multiple-choice question into a new table
    new = "create table {} (id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, choice_a TEXT, choice_b TEXT, choice_c TEXT, choice_d TEXT, correct_answer CHAR(1))".format(quizz_name)
    sql = "INSERT INTO {} (question, choice_a, choice_b, choice_c, choice_d, correct_answer) VALUES (%s, %s, %s, %s, %s, %s)".format(quizz_name)
    values = (question, choices[0], choices[1], choices[2], choices[3], correct_answer)

    try:
        cursor.execute(new)
        cursor.execute(sql, values)
        connection.commit()
        print("Question and choices inserted successfully!")
    except ms.Error as err:
        print("Error:", err)
        connection.rollback()

    # Close the cursor and connection
    cursor.close()
    connection.close()


# Accept multiple-choice questions from the user until they choose to exit
def NEWQUIZZ():
    quizz_name = input("Enter name of the quizz:")
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
        
        
def insert_question_and_answer(flashcard_set_name, question, answer):
    import mysql.connector as ms

    # Connect to the MySQL database
    connection = ms.connect(host="localhost", username="root", password="hello", database="FLASHCARD")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    # SQL query to insert a new question and answer into the QnA table

    sql = "INSERT INTO {} (question, answer) VALUES (%s, %s)".format(flashcard_set_name)
    values = (question, answer)

    try:

        cursor.execute(sql, values)
        connection.commit()
        print("Question and answer inserted successfully!")
    except ms.Error as err:
        print("Error", err)
        connection.rollback()

    cursor.close()
    connection.close()
    
    
# Accept questions and answers from the user until they choose to exit
def NEWFLASHCARD_SET():
    import mysql.connector as ms

    # Connect to the MySQL database
    connection = ms.connect(host="localhost", username="root", password="hello", database="FLASHCARD")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    flashcard_set_name = input("Enter name of new flashcard set:")
    new = "create table {} (id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, answer TEXT);".format(flashcard_set_name)
    try:
        cursor.execute(new)
    except ms.Error:
        print("table already exists")
    while True:
        question = input("Enter a question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        answer = input("Enter the answer: ")

        insert_question_and_answer(flashcard_set_name, question, answer)
        
        
def TAKE_A_QUIZ(connection, selected_table):
    import time
    cursor = connection.cursor()
    cursor.execute("SELECT question, choice_a, choice_b, choice_c, choice_d, correct_answer FROM {} ;".format(selected_table))
    question_data = cursor.fetchall()
    score = 0
    index = 0
    time_limit = int(input('enter time limit:'))
    while True:
        question_c = question_data[index]

        if question_c:
            question, choice_a, choice_b, choice_c, choice_d, correct_answer = question_c
            options = [choice_a,choice_b,choice_c,choice_d]

            print(question)

            # Display answer options
            for i, option in enumerate(options, start=1):
                print(f"{chr(ord('A') + i - 1)}. {option}")

            start_time = time.time()
            user_answer = input("Enter the option of your answer (A, B, C, or D): ").upper()
            end_time = time.time()

            elapsed_time = end_time - start_time

            # Check if the user's answer is correct and within the time limit
            if user_answer == correct_answer and elapsed_time <= time_limit:
                print("Correct!")
                score += 1
                index += 1

            elif user_answer == correct_answer and elapsed_time > time_limit:
                print("Time's up! but you were right.")
                index += 1
            elif elapsed_time > time_limit:
                print("Time up! and the answer you gave is wrong.")
                index += 1
            else:
                print("Incorrect!")
                choice_re = int(input("do you want to \n1.know the correct answer \nor\n2.retry the question"))
                if choice_re == 1:
                    print("The correct answer is", correct_answer)
                    index += 1
                elif choice_re == 2:
                    continue
                else:
                    print("invalid choice")
                    index += 1

            if index >= len(question_data):
                break

        else:
            print("Questions not found in the", selected_table)


def TEST_WITH_FLASHCARD(connection, selected_table):
    import time
    cursor = connection.cursor()
    cursor.execute("SELECT question, answer FROM {};".format(selected_table))
    questions_data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()
    if not questions_data:
        print("No questions found in the database.")
        return

    score = 0
    index = 0
    time_limit = int(input("Enter time limit for each question"))

    while True:
        question, correct_answer = questions_data[index]
        print(question)
        start_time = time.time()
        user_answer = input("Enter your answer: ").strip()
        end_time = time.time()

        elapsed_time = end_time - start_time

        if user_answer.lower() == correct_answer.lower() and elapsed_time > time_limit:
            print("Time's up! but you got the answer right.")
            index += 1
        elif user_answer.lower() == correct_answer.lower():
            print("Correct!")
            score += 1
            index += 1
        else:
            print("Incorrect!")
            choice_re = int(input("do you want to \n1.know the correct answer \nor\n2.retry the question"))
            if choice_re == 1:
                print("The correct answer is", correct_answer)
                index += 1
            elif choice_re == 2:
                continue
            else:
                print("invalid choice")
                index += 1
        if index >= len(questions_data):
            break





def LIST_QUIZZES(choice):
    import mysql.connector
    connection = mysql.connector.connect(host="localhost", username="root", password="hello", database=choice)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    if not tables:
        print("No", choice," found in the database.")
        return

    print(choice, "in the database:")
    for index, table in enumerate(tables, start=1):
        print(f"{index}. {table[0]}")

    # Ask the user to select a table
    print("Enter the number of the",choice," you want to select (or 'q' to quit): ",end="")
    ch = input()

    if ch.lower() == 'q':
        return

    try:
        ch = int(ch)
        if 1 <= ch <= len(tables):
            selected_table = tables[ch - 1][0]
            print(f"You selected table '{selected_table}'.")
            if choice.lower() == 'quiz':
                TAKE_A_QUIZ(connection, selected_table)
            elif choice.lower() == 'flashcard':
                TEST_WITH_FLASHCARD(connection, selected_table)

        else:
            print("Invalid choice. Please enter a valid table number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    cursor.close()
    connection.close()
