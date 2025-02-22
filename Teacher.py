from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
from datetime import datetime
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

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
                             columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'Added Date'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')

def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=5, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=5, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=5, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=5, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=5, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=5, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=5, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=5, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=5, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=5, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=5, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=5, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=6, columnspan=2, pady=10)

    if title == 'Update Student':
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])

def update_data():
    query = 'UPDATE student SET name=%s, mobile=%s, email=%s, address=%s, gender=%s WHERE id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')
    show_student()

def search_data():
    id_val = idEntry.get()
    name_val = nameEntry.get()
    email_val = emailEntry.get()
    phone_val = phoneEntry.get()
    address_val = addressEntry.get()
    gender_val = genderEntry.get()

    query = "SELECT * FROM student WHERE"
    conditions = []
    args = []

    if id_val:
        conditions.append(" id LIKE %s")
        args.append(f"%{id_val}%")
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

    if conditions:
        query += " OR ".join(conditions)
    else:
        query = query.replace("WHERE", "")

    mycursor.execute(query, tuple(args))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            check_query = 'SELECT * FROM student WHERE id=%s'
            mycursor.execute(check_query, (idEntry.get(),))
            existing_id = mycursor.fetchone()

            if existing_id:
                messagebox.showerror('Error', 'Id already exists. Please use a different Id.', parent=screen)
                return

            query = '''INSERT INTO student (ID, Name, Mobile, Email, Address, Gender) 
                       VALUES (%s, %s, %s, %s, %s, %s)'''

            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(),
                                     addressEntry.get(), genderEntry.get()))
            con.commit()

            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while adding data: {str(e)}', parent=screen)
            return

        show_student()

def update_grade():
    global gradeEntry, courseIDEntry, courseNameEntry, creditEntry, gradeScreen
    gradeScreen = Toplevel()
    gradeScreen.title("Update Grade")
    gradeScreen.grab_set()
    gradeScreen.resizable(False, False)

    studentIDLabel = Label(gradeScreen, text='Student ID', font=('times new roman', 20, 'bold'))
    studentIDLabel.grid(row=0, column=0, padx=30, pady=5, sticky=W)
    studentIDEntry = Entry(gradeScreen, font=('roman', 15, 'bold'), width=24)
    studentIDEntry.grid(row=0, column=1, pady=5, padx=10)

    courseIDLabel = Label(gradeScreen, text='Course ID', font=('times new roman', 20, 'bold'))
    courseIDLabel.grid(row=1, column=0, padx=30, pady=5, sticky=W)
    courseIDEntry = Entry(gradeScreen, font=('roman', 15, 'bold'), width=24)
    courseIDEntry.grid(row=1, column=1, pady=5, padx=10)

    courseNameLabel = Label(gradeScreen, text='Course Name', font=('times new roman', 20, 'bold'))
    courseNameLabel.grid(row=2, column=0, padx=30, pady=5, sticky=W)
    courseNameEntry = Entry(gradeScreen, font=('roman', 15, 'bold'), width=24)
    courseNameEntry.grid(row=2, column=1, pady=5, padx=10)

    creditLabel = Label(gradeScreen, text='Credit', font=('times new roman', 20, 'bold'))
    creditLabel.grid(row=3, column=0, padx=30, pady=5, sticky=W)
    creditEntry = Entry(gradeScreen, font=('roman', 15, 'bold'), width=24)
    creditEntry.grid(row=3, column=1, pady=5, padx=10)

    gradeLabel = Label(gradeScreen, text='Grade', font=('times new roman', 20, 'bold'))
    gradeLabel.grid(row=4, column=0, padx=30, pady=5, sticky=W)
    gradeEntry = Entry(gradeScreen, font=('roman', 15, 'bold'), width=24)
    gradeEntry.grid(row=4, column=1, pady=5, padx=10)

    updateButton = ttk.Button(gradeScreen, text='Update Grade', command=lambda: update_grade_in_db(studentIDEntry.get(), courseIDEntry.get(), courseNameEntry.get(), creditEntry.get(), gradeEntry.get()))
    updateButton.grid(row=5, columnspan=2, pady=10)

def update_grade_in_db(student_id, course_id, course_name, credit, grade):
    if not all([student_id, course_id, course_name, credit, grade]):
        messagebox.showerror('Error', 'All fields are required', parent=gradeScreen)
        return

    query = 'INSERT INTO Mark (StudentID, CourseID, CourseName, Credit, Grade) VALUES (%s, %s, %s, %s, %s)'
    mycursor.execute(query, (student_id, course_id, course_name, credit, grade))
    con.commit()
    messagebox.showinfo('Success', 'Grade updated successfully', parent=gradeScreen)
    gradeScreen.destroy()

def insert_course():
    if courseIDEntry.get() == '' or courseNameEntry.get() == '' or creditEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=courseScreen)
    else:
        try:
            query = 'INSERT INTO Course (CourseID, CourseName, Credit) VALUES (%s, %s, %s)'
            mycursor.execute(query, (courseIDEntry.get(), courseNameEntry.get(), creditEntry.get()))
            con.commit()
            messagebox.showinfo('Success', 'Course added successfully', parent=courseScreen)
            courseScreen.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while adding course: {str(e)}', parent=courseScreen)

def course_input_window():
    global courseIDEntry, courseNameEntry, creditEntry, courseScreen
    courseScreen = Toplevel()
    courseScreen.title("Add Course")
    courseScreen.grab_set()
    courseScreen.resizable(False, False)

    courseIDLabel = Label(courseScreen, text='Course ID', font=('times new roman', 20, 'bold'))
    courseIDLabel.grid(row=0, column=0, padx=30, pady=5, sticky=W)
    courseIDEntry = Entry(courseScreen, font=('roman', 15, 'bold'), width=24)
    courseIDEntry.grid(row=0, column=1, pady=5, padx=10)

    courseNameLabel = Label(courseScreen, text='Course Name', font=('times new roman', 20, 'bold'))
    courseNameLabel.grid(row=1, column=0, padx=30, pady=5, sticky=W)
    courseNameEntry = Entry(courseScreen, font=('roman', 15, 'bold'), width=24)
    courseNameEntry.grid(row=1, column=1, pady=5, padx=10)

    creditLabel = Label(courseScreen, text='Credit', font=('times new roman', 20, 'bold'))
    creditLabel.grid(row=2, column=0, padx=30, pady=5, sticky=W)
    creditEntry = Entry(courseScreen, font=('roman', 15, 'bold'), width=24)
    creditEntry.grid(row=2, column=1, pady=5, padx=10)

    addCourseButton = ttk.Button(courseScreen, text='Add Course', command=insert_course)
    addCourseButton.grid(row=3, columnspan=2, pady=10)

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='1411468703')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        try:
            query = 'create database SMS'
            mycursor.execute(query)

            query = 'use SMS'
            mycursor.execute(query)

            query = '''create table student(
                id varchar(50) not null primary key, 
                name varchar(100) not null, 
                mobile varchar(15) not null, 
                email varchar(100) not null, 
                address text not null, 
                gender enum('Male', 'Female', 'Other') not null
            )'''
            mycursor.execute(query)

            query = '''create table Mark(
                StudentID varchar(50), 
                CourseID varchar(30), 
                CourseName varchar(100), 
                Credit int, 
                Grade varchar(5)
            )'''
            mycursor.execute(query)

            query = '''create table Course(
                CourseID varchar(30) not null primary key, 
                CourseName varchar(100) not null, 
                Credit int not null
            )'''
            mycursor.execute(query)

        except:
            query = 'use SMS'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updateGradeButton.config(state=NORMAL)
        courseUpdateButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('188x97+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)

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

# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

# Set the main window background color to a white bluish shade
root.configure(bg='#E0F7FA')  # Light bluish color

# Date and Time Label
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'), bg='#E0F7FA')
datetimeLabel.place(x=5, y=5)
clock()

s = 'SMS:Teacher Section'
sliderLabel = Label(root, font=('times new roman', 32, 'bold'), width=30, bg='#E0F7FA')
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root, bg='#E0F7FA')
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image, bg='#E0F7FA')
logo_Label.grid(row=0, column=0)

# Define styles for buttons with unique colors and 3D effect
style = ttk.Style()
style.configure('AddButton.TButton', background='#4CAF50', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('SearchButton.TButton', background='#2196F3', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('DeleteButton.TButton', background='#F44336', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('UpdateButton.TButton', background='#FFC107', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('ShowButton.TButton', background='#FFEB3B', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('ExportButton.TButton', background='#FF5722', foreground='black', font=('Arial', 12, 'bold'), relief='raised')
style.configure('ExitButton.TButton', background='#9E9E9E', foreground='black', font=('Arial', 12, 'bold'), relief='raised')

# Button Colors
addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', add_data), style='AddButton.TButton')
addstudentButton.grid(row=1, column=0, pady=5)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'Search', search_data), style='SearchButton.TButton')
searchstudentButton.grid(row=2, column=0, pady=5)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student, style='DeleteButton.TButton')
deletestudentButton.grid(row=3, column=0, pady=5)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', update_data), style='UpdateButton.TButton')
updatestudentButton.grid(row=4, column=0, pady=5)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student, style='ShowButton.TButton')
showstudentButton.grid(row=5, column=0, pady=5)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, state=DISABLED, command=export_data, style='ExportButton.TButton')
exportstudentButton.grid(row=6, column=0, pady=5)

updateGradeButton = ttk.Button(leftFrame, text='Update Grade', width=25, state=DISABLED, command=update_grade, style='UpdateButton.TButton')
updateGradeButton.grid(row=7, column=0, pady=5)

courseUpdateButton = ttk.Button(leftFrame, text='Course Update', width=25, state=NORMAL,
                                 command=course_input_window, style='UpdateButton.TButton')
courseUpdateButton.grid(row=8, column=0, pady=5)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit, style='ExitButton.TButton')
exitButton.grid(row=9, column=0, pady=5)

rightFrame = Frame(root, bg='#E0F7FA')
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'Added Date'),
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
studentTable.heading('Added Date', text='Added Date')

studentTable.column('Id', width=200, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white', )
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()