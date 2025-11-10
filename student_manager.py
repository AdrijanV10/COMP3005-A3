import psycopg2
from psycopg2 import sql

class StudentManager:
    def __init__(self):
        # Initialize database connection.
        self.connection = None
        # Database connection parameters.
        self.db_params = {
            'host': 'localhost',
            'database': 'comp3005',
            'user': 'postgres',
            'password': 'postgres123',
            'port': '5432'
        }
    
    def connect(self):
        # Connect to PostgreSQL database using connection parameters
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("Successfully connected to the database!")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        # Close database connection if needed
        if self.connection:
            self.connection.close()

    def getAllStudents(self):
        # Get and then display all student records from database.
        try:
            cursor = self.connection.cursor()
            # Execute query to get all of the students ordered by ID
            cursor.execute("SELECT * FROM students ORDER BY student_id;")
            students = cursor.fetchall()
            
            # Display results in table
            print("\n" + "="*80)
            print("ALL STUDENTS:")
            print("="*80)
            # Table header
            print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<20}")
            print("-" * 80)
            
            # Display each student record.
            for student in students:
                # student[0]=id, [1]=first_name, [2]=last_name, [3]=email, [4]=enrollment_date
                print(f"{student[0]:<5} {student[1]:<15} {student[2]:<15} {student[3]:<30} {str(student[4]):<20}")
            
            print(f"\nTotal students: {len(students)}")
            cursor.close()
        except Exception as e:
            print(f"Error retrieving students: {e}")

    def addStudent(self, first_name, last_name, email, enrollment_date):
        # Insert a new student record to the database
        try:
            cursor = self.connection.cursor()
            # Insert query with parameterized values.
            cursor.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, enrollment_date)
            )
            # Commit transaction to save changes.
            self.connection.commit()
            print(f"Successfully added student: {first_name} {last_name}")
            cursor.close()
        except Exception as e:
            print(f"Error adding student: {e}")

    def updateStudentEmail(self, student_id, new_email):
        # Update a students email address
        try:
            cursor = self.connection.cursor()
            # use update query to change email
            cursor.execute(
                "UPDATE students SET email = %s WHERE student_id = %s",
                (new_email, student_id)
            )
            # Commit transaction to save edits.
            self.connection.commit()
            print(f"Updated email for student ID {student_id} to: {new_email}")
            cursor.close()
        except Exception as e:
            print(f"Error updating email: {e}")

    def deleteStudent(self, student_id):
        # Delete a student from the database.
        try:
            cursor = self.connection.cursor()
            # Use delete query to remove student.
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            # Commit transaction to save the changes.
            self.connection.commit()
            print(f"Deleted student with ID: {student_id}")
            cursor.close()
        except Exception as e:
            print(f"Error deleting student: {e}")

def main():
    manager = StudentManager()
    manager.connect()
    
    # Main program loop.
    while True:
        # Printing menu options.
        print("\n" + "="*50)
        print("STUDENT MANAGEMENT SYSTEM")
        print("="*50)
        print("1. View all students")
        print("2. Add new student")
        print("3. Update student email")
        print("4. Delete student")
        print("5. Exit")
        
        # Get user input
        choice = input("\nEnter your choice (1-5): ").strip()
        
        # Menu choices
        if choice == '1':
            # get all students.
            manager.getAllStudents()

        elif choice == '2':
            # Add new student and get input from user
            print("\nAdd New Student:")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment Date (YYYY-MM-DD): ").strip()
            manager.addStudent(first_name, last_name, email, enrollment_date)

        elif choice == '3':
            # Update student email and get input from the user.
            print("\nUpdate Student Email:")
            student_id = input("Student ID: ").strip()
            new_email = input("New Email: ").strip()
            manager.updateStudentEmail(student_id, new_email)

        elif choice == '4':
            # Delete student and then get input from the user.
            print("\nDelete Student:")
            student_id = input("Student ID to delete: ").strip()
            manager.deleteStudent(student_id)

        elif choice == '5':
            # Exit
            print("Goodbye!")
            break
        else:
            # Invalid input/
            print("Invalid choice! Please enter 1-5.")
        
        # Print before showing menu again.
        input("\nPress Enter to continue...")
    
    # Disconnect from database when done.
    manager.disconnect()

if __name__ == "__main__":
    # Entry point
    main()