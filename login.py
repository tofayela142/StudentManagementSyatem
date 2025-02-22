from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector

def on_enter(e):
    e.widget['background'] = 'lightcoral'  # Change color on hover

def on_leave(e):
    e.widget['background'] = 'lightpink'  # Revert color when not hovering

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    else:
        user_type = user_type_var.get()
        # Connect to the database and check credentials
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1411468703",
            database="SMS"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE ID = %s AND Password = %s AND UserType = %s",
                       (usernameEntry.get(), passwordEntry.get(), user_type))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo('Success', f'Welcome {user[2]}')  # user[2] is Name
            window.destroy()

            # Redirect to the appropriate page based on user type
            if user_type == "Teacher":
                import Teacher  # Redirect to Teacher.py
            elif user_type == "Student":
                import Student  # Redirect to Student.py
        else:
            messagebox.showerror('Error', 'Invalid ID, password, or user type')

def open_registration_window():
    def register():
        user_id = reg_usernameEntry.get()
        name = reg_nameEntry.get()
        password = reg_passwordEntry.get()
        user_type = user_type_var.get()  # Correctly fetch the selected user type

        if user_id == '' or name == '' or password == '' or user_type == '':
            messagebox.showerror('Error', 'All fields are required')
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1411468703",
            database="SMS"
        )
        cursor = conn.cursor()

        try:
            # Check if the Student ID exists in the Student table
            cursor.execute("SELECT ID FROM Student WHERE ID = %s", (user_id,))
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student ID not found in the database. Please add the student first.")
                return

            # Insert into User table
            cursor.execute(
                "INSERT INTO User (ID, Password, Name, UserType) VALUES (%s, %s, %s, %s)",
                (user_id, password, name, user_type)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful")
            reg_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            conn.close()

    reg_window = Toplevel(window)
    reg_window.geometry('500x500')
    reg_window.title('Register New User')

    global user_type_var
    user_type_var = StringVar()
    user_type_label = Label(reg_window, text="Select User Type", font=('times new roman', 16, 'bold'))  # Increased font size and made it bold
    user_type_label.pack(pady=10)

    student_radio = Radiobutton(reg_window, text="Student", variable=user_type_var, value="Student",
                                font=('times new roman', 18))
    student_radio.pack(pady=5)

    teacher_radio = Radiobutton(reg_window, text="Teacher", variable=user_type_var, value="Teacher",
                                font=('times new roman', 18))
    teacher_radio.pack(pady=5)

    reg_usernameLabel = Label(reg_window, text="StudentID or TeacherID", font=('times new roman', 18))
    reg_usernameLabel.pack(pady=10)
    reg_usernameEntry = Entry(reg_window, font=('times new roman', 18))
    reg_usernameEntry.pack(pady=5)

    reg_nameLabel = Label(reg_window, text="Name", font=('times new roman', 18))
    reg_nameLabel.pack(pady=10)
    reg_nameEntry = Entry(reg_window, font=('times new roman', 18))
    reg_nameEntry.pack(pady=5)

    reg_passwordLabel = Label(reg_window, text="Password", font=('times new roman', 18))
    reg_passwordLabel.pack(pady=10)
    reg_passwordEntry = Entry(reg_window, font=('times new roman', 18), show="*")
    reg_passwordEntry.pack(pady=5)

    registerButton = Button(reg_window, text="Register", font=('times new roman', 18), command=register, bg='lightpink', fg='black', relief=RAISED)
    registerButton.pack(pady=20)

# Main login window
window = Tk()
window.geometry('1200x700+0+0')
window.title('Login System of Student Management System')
window.resizable(False, False)

background = ImageTk.PhotoImage(file='bg1.jpg')  # Replace with your background image path
bgLabel = Label(window, image=background)
bgLabel.place(x=0, y=0)

# Create a login frame with a 3D border effect
loginFrame = Frame(window, bg='purple', bd=5, relief=RAISED)  # Set background to purple
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the frame

logoImage = PhotoImage(file='logo.png')  # Replace with your logo image path
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage = PhotoImage(file='user.png')  # Replace with your username icon path
usernameLabel = Label(loginFrame, image=usernameImage, text='Student ID', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='purple')  # Set background to purple
usernameLabel.grid(row=1, column=0, pady=10, padx=20)
usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage = PhotoImage(file='password.png')  # Replace with your password icon path
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='purple')  # Set background to purple
passwordLabel.grid(row=2, column=0, pady=10, padx=20)
passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue', show="*")
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

# Add user type selection
user_type_var = StringVar(value="Student")
user_type_label = Label(loginFrame, text="         Select User Type:", font=('times new roman', 20, 'bold'), bg='purple')  # Set background to purple
user_type_label.grid(row=3, column=0, pady=10, padx=20)

user_type_menu = OptionMenu(loginFrame, user_type_var, "Student", "Teacher")
user_type_menu.config(font=('times new roman', 14), bd=5, bg='lightpink')  # Set background to light pink
user_type_menu.grid(row=3, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 15, 'bold'), width=15, fg='black',
                     bg='lightpink', activebackground='lightcoral', activeforeground='black', cursor='hand2',
                     command=login, relief=RAISED)  # Set background to light pink and 3D effect
loginButton.grid(row=4, column=1, pady=10)
loginButton.bind("<Enter>", on_enter)
loginButton.bind("<Leave>", on_leave)

# Add registration button
registrationButton = Button(loginFrame, text='Register', font=('times new roman', 15, 'bold'), width=15, fg='black',
                            bg='lightpink', activebackground='lightcoral', activeforeground='black',
                            cursor='hand2', command=open_registration_window, relief=RAISED)  # Set background to light pink and 3D effect
registrationButton.grid(row=5, column=1, pady=10)
registrationButton.bind("<Enter>", on_enter)
registrationButton.bind("<Leave>", on_leave)

window.mainloop()