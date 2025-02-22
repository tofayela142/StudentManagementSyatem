from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
from datetime import datetime
from fpdf import FPDF  # Import FPDF for PDF generation

# Global variables for database connection
mycursor = None
con = None


# Functionality Part

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,
                             columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date',
                                      'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    def perform_search():
        id_val = idEntry.get()
        name_val = nameEntry.get()
        email_val = emailEntry.get()
        phone_val = phoneEntry.get()
        address_val = addressEntry.get()
        gender_val = genderEntry.get()
        dob_val = dobEntry.get()

        # Create search conditions using LIKE for substring matching
        query = "SELECT * FROM student WHERE"
        conditions = []
        args = []

        if id_val:
            conditions.append(" id LIKE %s")
            args.append(f"%{id_val}%")  # Use LIKE with wildcards
        if name_val:
            conditions.append(" name LIKE %s")
            args.append(f"%{name_val}%")
        if email_val:
            conditions.append(" email LIKE %s")
            args.append(f"%{email_val}%")
        if phone_val:
            conditions.append(" mobile LIKE %s")
            args.append(f"%{phone_val}%")
        if address_val:
            conditions.append(" address LIKE %s")
            args.append(f"%{address_val}%")
        if gender_val:
            conditions.append(" gender LIKE %s")
            args.append(f"%{gender_val}%")
        if dob_val:
            conditions.append(" dob LIKE %s")
            args.append(f"%{dob_val}%")

        # Join the conditions with OR if they are not empty
        if conditions:
            query += " OR ".join(conditions)
        else:
            query = query.replace("WHERE", "")  # If no conditions, return all data

        # Execute the query with the correct number of arguments
        mycursor.execute(query, tuple(args))  # Pass the tuple of arguments

        # Clear the table and insert the fetched data
        studentTable.delete(*studentTable.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('', END, values=data)

        search_window.destroy()

    # Create a new window for search
    search_window = Toplevel()
    search_window.title("Search Student")
    search_window.grab_set()
    search_window.resizable(False, False)

    # Create entry fields for search criteria
    Label(search_window, text='Id', font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
    idEntry = Entry(search_window)
    idEntry.grid(row=0, column=1, padx=10, pady=5)

    Label(search_window, text='Name', font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=10, pady=5)
    nameEntry = Entry(search_window)
    nameEntry.grid(row=1, column=1, padx=10, pady=5)

    Label(search_window, text='Email', font=('Arial', 12, 'bold')).grid(row=2, column=0, padx=10, pady=5)
    emailEntry = Entry(search_window)
    emailEntry.grid(row=2, column=1, padx=10, pady=5)

    Label(search_window, text='Phone', font=('Arial', 12, 'bold')).grid(row=3, column=0, padx=10, pady=5)
    phoneEntry = Entry(search_window)
    phoneEntry.grid(row=3, column=1, padx=10, pady=5)

    Label(search_window, text='Address', font=('Arial', 12, 'bold')).grid(row=4, column=0, padx=10, pady=5)
    addressEntry = Entry(search_window)
    addressEntry.grid(row=4, column=1, padx=10, pady=5)

    Label(search_window, text='Gender', font=('Arial', 12, 'bold')).grid(row=5, column=0, padx=10, pady=5)
    genderEntry = Entry(search_window)
    genderEntry.grid(row=5, column=1, padx=10, pady=5)

    Label(search_window, text='D.O.B', font=('Arial', 12, 'bold')).grid(row=6, column=0, padx=10, pady=5)
    dobEntry = Entry(search_window)
    dobEntry.grid(row=6, column=1, padx=10, pady=5)

    search_button = ttk.Button(search_window, text='Search', command=perform_search)
    search_button.grid(row=7, columnspan=2, pady=10)


def connect_database():
    def connect():
        global mycursor, con
        try:
            # Connect to the database using default host
            con = pymysql.connect(host='localhost', user='root', password='1411468703', database='SMS')  # Default host
            mycursor = con.cursor()
        except Exception as e:
            messagebox.showerror('Error', f'Invalid Details: {str(e)}', parent=connectWindow)
            return

        try:
            query = 'create database IF NOT EXISTS SMS'
            mycursor.execute(query)

            query = 'use SMS'
            mycursor.execute(query)

            query = '''create table IF NOT EXISTS student(
                id varchar(50) not null primary key, 
                name varchar(100) not null, 
                mobile varchar(15) not null, 
                email varchar(100) not null, 
                address text not null, 
                gender enum('Male', 'Female', 'Other') not null, 
                dob date not null, 
                date varchar(50), 
                time varchar(50)
            )'''
            mycursor.execute(query)

            query = '''create table IF NOT EXISTS Taken(
                StudentID varchar(50) not null,
                CourseID varchar(50) not null,
                Credit INT,
                primary key (StudentID, CourseID)
            )'''
            mycursor.execute(query)

        except Exception as e:
            query = 'use SMS'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        searchstudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('173x97+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=0, columnspan=2)


count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


# Save Results Functionality
def save_results(result_tree):
    url = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
    if url:
        with open(url, 'w') as file:
            for item in result_tree.get_children():
                row = result_tree.item(item)['values']
                file.write(" | ".join(str(i) if i is not None else "N/A" for i in row) + "\n")
        messagebox.showinfo("Success", "Results saved successfully!")


def save_results_as_pdf(result_tree):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 10, txt="Student Results", ln=True, align='C')

    # Add column headers
    columns = ["Course Name", "Credit", "Grade", "Grade Point"]  # Removed "Student Name"
    pdf.set_font("Arial", 'B', size=12)
    for col in columns:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()

    # Add data from the Treeview
    pdf.set_font("Arial", size=12)
    for item in result_tree.get_children():
        row = result_tree.item(item)['values']
        for value in row:
            pdf.cell(40, 10, str(value), border=1)
        pdf.ln()

    # Save the PDF
    pdf_file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        pdf.output(pdf_file_path)
        messagebox.showinfo("Success", "Results saved as PDF successfully!")


def show_result():
    def execute_query():
        user_id = user_id_entry.get()
        password = password_entry.get()

        # SQL query to execute
        query = """
        WITH UserAuth AS (
            SELECT ID, Name
            FROM User
            WHERE ID = %s AND Password = %s
        ),
        StudentCourses AS (
            SELECT 
                m.StudentID,
                m.CourseName, 
                m.Credit, 
                m.Grade,
                CASE 
                    WHEN m.Grade = 'A' THEN 4.00
                    WHEN m.Grade = 'B' THEN 3.00
                    WHEN m.Grade = 'C' THEN 2.00
                    WHEN m.Grade = 'D' THEN 1.00
                    WHEN m.Grade = 'F' THEN 0.00
                    ELSE NULL 
                END AS GradePoint
            FROM Mark m
            WHERE m.StudentID = %s
        ),
        TotalCreditsAndCGPA AS (
            SELECT 
                SUM(m.Credit) AS TotalCredits,
                SUM(CASE 
                        WHEN m.Grade = 'A' THEN 4.00
                        WHEN m.Grade = 'B' THEN 3.00
                        WHEN m.Grade = 'C' THEN 2.00
                        WHEN m.Grade = 'D' THEN 1.00
                        WHEN m.Grade = 'F' THEN 0.00
                        ELSE NULL 
                    END * m.Credit) / SUM(m.Credit) AS CGPA
            FROM Mark m
            WHERE m.StudentID = %s
        )
        SELECT 
            sc.CourseName,
            sc.Credit,
            sc.Grade,
            sc.GradePoint
        FROM UserAuth ua
        JOIN StudentCourses sc ON ua.ID = sc.StudentID

        UNION ALL

        SELECT 
            'Total' AS CourseName,
            tca.TotalCredits,
            NULL AS Grade,
            tca.CGPA
        FROM TotalCreditsAndCGPA tca;
        """

        try:
            mycursor.execute(query, (user_id, password, user_id, user_id))
            fetched_data = mycursor.fetchall()

            # Clear the Treeview and insert the results
            result_tree.delete(*result_tree.get_children())  # Clear previous results
            for data in fetched_data:
                result_tree.insert('', END, values=data)

            # Get the name of the user for display
            name_query = "SELECT Name FROM User WHERE ID = %s"
            mycursor.execute(name_query, (user_id,))
            name_result = mycursor.fetchone()
            if name_result:
                name_label.config(text=f"Name: {name_result[0]}")  # Update the name label

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create a new window for user input
    result_window = Toplevel()
    result_window.title("Show Result")
    result_window.geometry("1000x800")  # Increased size for the result window
    result_window.resizable(True, True)

    Label(result_window, text='User   ID', font=('Arial', 12, 'bold')).pack(pady=5)
    user_id_entry = Entry(result_window)
    user_id_entry.pack(pady=5)

    Label(result_window, text='Password', font=('Arial', 12, 'bold')).pack(pady=5)
    password_entry = Entry(result_window, show='*')
    password_entry.pack(pady=5)

    show_result_button = ttk.Button(result_window, text='Show Result', command=execute_query)
    show_result_button.pack(pady=10)

    # Create a Label for displaying the name
    name_label = Label(result_window, text='', font=('Arial', 14, 'bold'), anchor='e')  # Right-aligned
    name_label.pack(fill=X, padx=10)

    # Create a Treeview widget for displaying results
    columns = ("Course Name", "Credit", "Grade", "Grade Point")  # Removed "Student Name"
    result_tree = ttk.Treeview(result_window, columns=columns, show='headings')

    # Define headings
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, anchor=CENTER)

    result_tree.pack(expand=True, fill=BOTH)

    # Add a button to save results as PDF
    pdf_button = ttk.Button(result_window, text='Save Results as PDF', command=lambda: save_results_as_pdf(result_tree))
    pdf_button.pack(pady=5)

    # Add a button to save results as text
    save_button = ttk.Button(result_window, text='Save Results', command=lambda: save_results(result_tree))
    save_button.pack(pady=5)


# New function to show allocated courses based on User ID
def show_allocated_course():
    def save_allocated_course(course_info):
        url = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
        if url:
            with open(url, 'w') as file:
                file.write(course_info)
            messagebox.showinfo("Success", "Allocated course information saved successfully!")

    # Create a new window for user input
    course_window = Toplevel()
    course_window.title("Your Allocated Course")
    course_window.geometry("300x200")
    course_window.resizable(False, False)

    Label(course_window, text='Enter User ID:', font=('Arial', 12, 'bold')).pack(pady=10)
    user_id_entry = Entry(course_window)
    user_id_entry.pack(pady=5)

    def fetch_courses():
        user_id = user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "User  ID cannot be empty.")
            return

        query = "SELECT CourseID FROM Taken WHERE StudentID = %s"
        mycursor.execute(query, (user_id,))
        allocated_courses = mycursor.fetchall()

        if not allocated_courses:
            messagebox.showinfo("Allocated Course", "No allocated courses found for this User ID.")
            return

        course_info = f"Allocated Courses for User ID {user_id}:\n"
        for course in allocated_courses:
            course_info += f"- {course[0]}\n"

        # Create a new window to display the results
        result_window = Toplevel()
        result_window.title("Allocated Courses")
        result_window.geometry("500x400")
        result_window.resizable(False, False)

        # Create a Text widget for displaying results
        result_text_widget = Text(result_window, wrap='word', height=20, width=60)
        result_text_widget.pack(pady=10)

        # Insert the course information into the Text widget
        result_text_widget.insert(END, course_info)

        # Add a button to save results
        save_button = ttk.Button(result_window, text='Save Results', command=lambda: save_allocated_course(course_info))
        save_button.pack(pady=5)

    fetch_button = ttk.Button(course_window, text='Fetch Allocated Courses', command=fetch_courses)
    fetch_button.pack(pady=10)


# New Course Registration Functionality
def course_registration():
    def submit_registration():
        student_id = student_id_entry.get()
        course_id = course_id_entry.get()
        credit = credit_entry.get()

        if not student_id or not course_id or not credit:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            credit = int(credit)  # Ensure credit is an integer
            query = "INSERT INTO Taken (StudentID, CourseID, Credit) VALUES (%s, %s, %s)"
            mycursor.execute(query, (student_id, course_id, credit))
            con.commit()
            messagebox.showinfo("Success", "Course registration successful!")
            registration_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create a new window for course registration
    registration_window = Toplevel()
    registration_window.title("Course Registration")
    registration_window.geometry("400x300")
    registration_window.resizable(False, False)

    Label(registration_window, text='Student ID', font=('Arial', 12, 'bold')).pack(pady=5)
    student_id_entry = Entry(registration_window)
    student_id_entry.pack(pady=5)

    Label(registration_window, text='Course ID', font=('Arial', 12, 'bold')).pack(pady=5)
    course_id_entry = Entry(registration_window)
    course_id_entry.pack(pady=5)

    Label(registration_window, text='Credit', font=('Arial', 12, 'bold')).pack(pady=5)
    credit_entry = Entry(registration_window)
    credit_entry.pack(pady=5)

    submit_button = ttk.Button(registration_window, text='Submit', command=submit_registration)
    submit_button.pack(pady=10)


# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

# Set the main window background color to a light purple shade
root.configure(bg='#E6E6FA')  # Light purple color

# Date and Time Label
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'), bg='#E6E6FA')
datetimeLabel.place(x=5, y=5)
clock()

s = 'SMS:Student Section'
sliderLabel = Label(root, font=('times new roman', 32, 'bold'), width=30, bg='#E6E6FA')
sliderLabel.place(x=200, y=0)
slider()

leftFrame = Frame(root, bg='#E6E6FA')
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student1.png')  # Ensure you have this image in the same directory
logo_Label = Label(leftFrame, image=logo_image, bg='#E6E6FA')
logo_Label.grid(row=0, column=0)

# Define styles for buttons with unique colors and 3D effect
style = ttk.Style()
style.configure('SearchButton.TButton', background='#2196F3', foreground='black', font=('Arial', 12, 'bold'),
                relief='raised')
style.configure('ShowButton.TButton', background='#FFEB3B', foreground='black', font=('Arial', 12, 'bold'),
                relief='raised')
style.configure('ExportButton.TButton', background='#FF5722', foreground='black', font=('Arial', 12, 'bold'),
                relief='raised')
style.configure('ExitButton.TButton', background='#9E9E9E', foreground='black', font=('Arial', 12, 'bold'),
                relief='raised')
style.configure('ConnectButton.TButton', background='#4CAF50', foreground='black', font=('Arial', 12, 'bold'),
                relief='raised')

# Button Colors
connectButton = ttk.Button(leftFrame, text='Connect to Database', width=25, command=connect_database,
                           style='ConnectButton.TButton')
connectButton.grid(row=1, column=0, pady=5)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,
                                 command=search_data, style='SearchButton.TButton')
searchstudentButton.grid(row=2, column=0, pady=5)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student,
                               style='ShowButton.TButton')
showstudentButton.grid(row=3, column=0, pady=5)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, state=DISABLED, command=export_data,
                                 style='ExportButton.TButton')
exportstudentButton.grid(row=4, column=0, pady=5)

showResultButton = ttk.Button(leftFrame, text='Show Result', width=25, command=show_result, style='ShowButton.TButton')
showResultButton.grid(row=5, column=0, pady=5)

courseRegistrationButton = ttk.Button(leftFrame, text='Course Registration', width=25, command=course_registration,
                                      style='ShowButton.TButton')
courseRegistrationButton.grid(row=6, column=0, pady=5)

allocatedCourseButton = ttk.Button(leftFrame, text='Your Allocated Course', width=25, command=show_allocated_course,
                                   style='ShowButton.TButton')
allocatedCourseButton.grid(row=7, column=0, pady=5)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit, style='ExitButton.TButton')
exitButton.grid(row=8, column=0, pady=5)

rightFrame = Frame(root, bg='#E6E6FA')
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender',
                                                 'D.O.B', 'Added Date', 'Added Time', 'Grade', 'GradePoint'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')
studentTable.heading('Grade', text='Grade')
studentTable.heading('GradePoint', text='Grade Point')

studentTable.column('Id', width=200, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)
studentTable.column('Grade', width=100, anchor=CENTER)
studentTable.column('GradePoint', width=100, anchor=CENTER)

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white', )
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()