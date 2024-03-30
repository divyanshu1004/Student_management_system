import mysql.connector

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='your_host',
            user='your_usernamee',
            password='your_password',
            database='Your_database_name'
        )
        print("Connection to MySQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")



def view_data(connection):
    table_name = input("Enter the table name to view its data: ")
    view_choice = input("Do you want to view the whole table or a specific part? (whole/part): ").lower()
    
    if view_choice == "whole":
        query = f"SELECT * FROM {table_name};"
    elif view_choice == "part":
        column_name = input("Enter the column name you want to filter by: ")
        value = input(f"Enter the value of {column_name} to filter by: ")
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s;"
        execute_query(connection, query, (value,))
        return
    else:
        print("Invalid choice. Please enter 'whole' or 'part'.")
        return
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if not results:
            print("The table is empty.")
        else:
            for row in results:
                print(row)
    except Exception as e:
        print(f"The error '{e}' occurred")



def insert_data(connection):
    print("\nSelect the table you want to insert data into:")
    print("1. Students")
    print("2. Teachers")
    print("3. Subjects")
    print("4. Classes")
    print("5. Classrooms")
    print("6. Enrollments")
    print("7. Grades")
    print("8. Attendances")
    print("9. Parents")
    choice = input("Enter your choice (1-9): ")

    if choice == '1':
        id = input("Enter student's Id: ")
        name = input("Enter student's name: ")
        grade = input("Enter student's grade: ")
        email = input("Enter student's email: ")
        parent_id=input("Enter  parent's ID: ")
        data = (id, name, grade, email, parent_id)
        query = "INSERT INTO students (id, name, grade, email, parent_id) VALUES (%s, %s, %s, %s, %s);"
        execute_query(connection, query, data)

    elif choice == '2':
        id = input("Enter teacher's Id: ")
        name = input("Enter teacher's name: ")
        subject_id = input("Enter teacher's subject_id: ")
        email = input("Enter teacher's email: ")
        data = (name, subject_id, email)
        query = "INSERT INTO teachers (id,name, subject_id, email) VALUES (%s, %s, %s, %s);"
        execute_query(connection, query, data)

    elif choice =='3':
        id =  input('Subject ID :')
        name = input("Enter subject name: ")
        dept_id = input("Enter Department id: ")
        data=(id,name,dept_id)
        query="insert into subjects (id, name, department_id) values(%s,%s,%s);"
        execute_query(connection,query,data)
    
    elif choice =='4':
        id = input("Enter  class id: ")
        class_name = input("Enter Class Name: ")
        teacher_id =input("Enter teacher Id: ")
        classroom_id =input("Enter Classroom Id: ")
        data = (id, class_name, teacher_id, classroom_id)
        query = "insert into classes (id, name, teacher_id, classroom_id) values(%s,%s,%s,%s);"
        execute_query(connection, query, data)
        
    elif choice=='5':
        id = input("Enter Classroom ID: ")
        room_no = input( "Enter Room Number: ")
        capacity = input( "Enter Capacity: ")
        data = (id, room_no, capacity)
        query = "insert into classrooms (id, room_number, capacity) values(%s,%s,%s);"
        execute_query(connection,query,data)
    
    elif choice=='6':
        student_id = input("Enter Student ID: ")
        class_id = input("Enter Class Id: ")
        data = (student_id, class_id)
        query = "insert into enrollments (student_id, class_id) values(%s,%s);"
        execute_query(connection,query,data)
    
    elif choice=='7':
        student_id = input("Enter Student Id:")
        class_id=input("Enter Class Id:")
        grade = input("Enter grade: ")
        data=(student_id,class_id, grade)
        query="Insert Into grades (student_id, class_id, grade) values(%s, %s, %s); "
        execute_query(connection,query,data)
    
    elif  choice=="8":
        student_id =  input("Enter Student Id: ")
        class_id =  input("Enter Class Id: ")
        date = input("Enter Date: ")
        status=input("Enter Status [Present/Absent]: ")
        data =  (student_id,class_id,date,status )
        query ="INSERT INTO attendance (student_id, class_id, date , status) VALUES(%s,%s,%s,%s);"
        execute_query(connection,query,data)
    
    elif choice=='9':
        id = input( "Enter the ID : ")
        name = input("Enter Name of Parent: ")
        phone = input("Phone number: ")
        email = input( "Email Address: ")
        data =(id, name,phone,email)
        query = "Insert Into parents (id, name,phone, email) values(%s,%s,%s,%s);"
        execute_query(connection,query,data)


    else:
        print("Invalid choice. Please enter a number between 1 and 9.")



def update_record(connection, table_name, column_to_update, new_value, condition_column, condition_value):
    query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition_column} = %s;"
    data = (new_value, condition_value)
    execute_query(connection, query, data)


def modify_table_attributes(connection, table_name, operation, column_name, data_type=None):
    if operation == 'add' and data_type is not None:
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
    elif operation == 'drop':
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
    else:
        print("Invalid operation or missing data type for adding a column.")
        return
    execute_query(connection, query)

# Helper function to handle SQL queries
def show_menu():
    print("\nSchool Management System")
    print("1. View data from a table")
    print("2. Insert data into a table")
    print("3. Update a record")
    print("4. Modify table attributes (add/drop column)")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")
    return choice


def main():
    connection = create_connection()
    while True:
        choice = show_menu()
        if choice == '1':
            view_data(connection)
        elif choice == '2':
            insert_data(connection)
        elif choice == '3':
            table_name = input("Enter the table name: ")
            column_to_update = input("Enter the column to update: ")
            new_value = input("Enter the new value: ")
            condition_column = input("Enter the condition column name: ")
            condition_value = input("Enter the condition value: ")
            update_record(connection, table_name, column_to_update, new_value, condition_column, condition_value)
        elif choice == '4':
            table_name = input("Enter the table name: ")
            operation = input("Do you want to 'add' or 'drop' a column? (add/drop): ")
            column_name = input("Enter the column name: ")
            if operation == 'add':
                data_type = input("Enter the data type for the new column: ")
                modify_table_attributes(connection, table_name, operation, column_name, data_type)
            else:
                modify_table_attributes(connection, table_name, operation, column_name)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")



if __name__ == "__main__":
    main()

