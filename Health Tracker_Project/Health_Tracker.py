import tkinter
from tkinter import messagebox
from tkinter import *
import sqlite3

# Create or connect to the database
conn = sqlite3.connect('user_credentials.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, age INTEGER, weight REAL, height REAL)''')
conn.commit()

window = tkinter.Tk()
window.title("Health_Tracker")
window.geometry('370x720')
window.configure(bg='#2A2A6C')
window.resizable(False, False)
frame = Frame(bg='#2A2A6C')

# Declare StringVars for entry fields
username_var = StringVar()
password_var = StringVar()
password_confirm_var = StringVar()
age_var = StringVar()
weight_var = StringVar()
height_var = StringVar()


def login(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user and user[1] == password:  # Check if username exists and password matches
        show_profile(username)
    else:
        messagebox.showerror(title="Error", message="Invalid login.")


def show_profile(username):
    global frame
    frame.destroy()  # Destroy previous frame
    frame = Frame(window, bg='#2A2A6C')
    frame.pack()

    profile_label = Label(frame, image=img1, bg='#2A2A6C')
    profile_label.grid(row=0, column=0, columnspan=2, pady=30)

    # Retrieve user data from the database
    c.execute("SELECT age, weight, height FROM users WHERE username=?", (username,))
    user_data = c.fetchone()
    if user_data:
        age, weight, height = user_data

        # Display username
        username_label = Label(frame, text="Username:", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        username_entry = Label(frame, text=username, bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        username_label.grid(row=1, column=0, pady=10, padx=10, sticky=W)
        username_entry.grid(row=1, column=1, pady=10, padx=10, sticky=W)

        # Display age
        age_label = Label(frame, text="Age:", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        age_entry = Label(frame, text=age, bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        age_label.grid(row=2, column=0, pady=10, padx=10, sticky=W)
        age_entry.grid(row=2, column=1, pady=10, padx=10, sticky=W)

       # Display height
        height_label = Label(frame, text="Height (cm):", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        height_entry = Label(frame, text=height, bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        height_label.grid(row=3, column=0, pady=10, padx=10, sticky=W)
        height_entry.grid(row=3, column=1, pady=10, padx=10, sticky=W)
        
        # Display weight
        weight_label = Label(frame, text="Weight (kg):", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        weight_entry = Label(frame, text=weight, bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        weight_label.grid(row=4, column=0, pady=10, padx=10, sticky=W)
        weight_entry.grid(row=4, column=1, pady=10, padx=10, sticky=W)

        # Calculate and display old BMI
        old_bmi = calculate_bmi(weight, height)
        old_bmi_label = Label(frame, text="Old BMI:", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        old_bmi_entry = Label(frame, text=f"{old_bmi:.2f}", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        old_bmi_label.grid(row=5, column=0, pady=10, padx=10, sticky=W)
        old_bmi_entry.grid(row=5, column=1, pady=10, padx=10, sticky=W)

        # Entry fields for updating height and weight
        new_height_label = Label(frame, text="New Height (cm):", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        new_height_entry = Entry(frame, textvariable=height_var, font=("Arial", 12))
        new_weight_label = Label(frame, text="New Weight (kg):", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
        new_weight_entry = Entry(frame, textvariable=weight_var, font=("Arial", 12))

        new_height_label.grid(row=6, column=0, pady=10, padx=10, sticky=W)
        new_height_entry.grid(row=6, column=1, pady=10, padx=10, sticky=W)
        new_weight_label.grid(row=7, column=0, pady=10, padx=10, sticky=W)
        new_weight_entry.grid(row=7, column=1, pady=10, padx=10, sticky=W)

        # Button to update height and weight
        update_button = Button(frame, text="Update", bg="#0E46A3", fg="#E1F7F5", font=("Arial", 12),
                               command=lambda: save_new_data(username, new_height_entry.get(), new_weight_entry.get()))
        update_button.grid(row=8, column=0, columnspan=2, pady=20)

        # Button to logout
        logout_button = Button(frame, text="Logout", bg="#9AC8CD", font=("Arial", 12), width=20, command=logout)
        logout_button.grid(row=9, column=0, columnspan=2, pady=20)

        # Button to exit
        exit_button = Button(frame, text="Exit", bg="#E5584C", font=("Arial", 12), width=20, command=exit)
        exit_button.grid(row=10, column=0, columnspan=2, pady=20)
    else:
        messagebox.showerror(title="Error", message="User data not found.")

        
def exit():
    confirm=messagebox.askokcancel("Exit","Exit!!!!!!!!!")
    if confirm == TRUE:
        quit()

def calculate_bmi(weight, height):
    """
    Function to calculate BMI (Body Mass Index).
    Formula: BMI = weight (kg) / (height (m) ** 2)
    """
    height_in_meters = height / 100  # Convert height from cm to meters
    return weight / (height_in_meters ** 2)


def save_new_data(username, new_height, new_weight):
    try:
        c.execute("SELECT height, weight FROM users WHERE username=?", (username,))
        old_height, old_weight = c.fetchone()

        # Update height and weight in the database
        c.execute("UPDATE users SET height=?, weight=? WHERE username=?", (new_height, new_weight, username))
        conn.commit()

        # Calculate old and new BMI
        old_bmi = calculate_bmi(old_weight, old_height)
        new_bmi = calculate_bmi(float(new_weight), float(new_height))

        # Compare old and new BMI
        if new_bmi > old_bmi:
            comparison = "higher"
        elif new_bmi < old_bmi:
            comparison = "lower"
        else:
            comparison = "equal"

        # Show BMI comparison message
        messagebox.showinfo(title="BMI Comparison",
                             message=f"Old BMI: {old_bmi:.2f}\nNew BMI: {new_bmi:.2f}\nYour new BMI is {comparison} than your old BMI.")

        # Show new profile data
        show_profile(username)

    except Exception as e:
        messagebox.showerror(title="Error", message="Failed to update profile.")
        print("SQLite error:", e)


def register():
    global frame
    frame.destroy()  # Destroy previous frame
    registerpage()


def registerpage():
    global frame
    frame = Frame(window, bg='#2A2A6C')
    frame.pack()
    
    profile_label = Label(frame, image=img1, bg='#2A2A6C')
    profile_label.grid(row=0, column=0, columnspan=2, pady=30)
    register_label = Label(frame, text="Register", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 20))

    username_label = Label(frame, text="Username", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    username_entry = Entry(frame, textvariable=username_var, font=("Arial", 16))

    age_label = Label(frame, text="Age", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    age_entry = Entry(frame, textvariable=age_var, font=("Arial", 16))

    password_label = Label(frame, text="Password", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    password_entry = Entry(frame, show="*", textvariable=password_var, font=("Arial", 16))

    password_confirm_label = Label(frame, text="Confirm Password", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    password_confirm_entry = Entry(frame, show="*", textvariable=password_confirm_var, font=("Arial", 16))

    register_button = Button(frame, text="Register", bg="#0E46A3", fg="#E1F7F5", width=20, font=("Arial", 12),
                             command=lambda: register_user(username_var, password_var, password_confirm_var, age_var))

    back_button = Button(frame, text="Back", bg="#9AC8CD", font=("Arial", 12), width=20, command=loginlayout)

    register_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)
    username_label.grid(row=2, column=0, sticky=W, pady=10)
    username_entry.grid(row=3, column=0)
    age_label.grid(row=4, column=0, sticky=W, pady=10)
    age_entry.grid(row=5, column=0)
    password_label.grid(row=6, column=0, sticky=W, pady=10)
    password_entry.grid(row=7, column=0)
    password_confirm_label.grid(row=8, column=0, sticky=W, pady=10)
    password_confirm_entry.grid(row=9, column=0)
    register_button.grid(row=10, column=0, columnspan=2,pady=40)
    back_button.grid(row=11, column=0, columnspan=2, pady=10)


def register_user(username_var, password_var, password_confirm_var, age_var):
    username = username_var.get()
    password = password_var.get()
    password_confirm = password_confirm_var.get()
    age = age_var.get()

    # Check if passwords match
    if password == password_confirm:
        try:
            c.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", (username, password, age))
            conn.commit()
            messagebox.showinfo(title="Registration Success", message="You have been registered successfully.")
            loginlayout()  # Go back to login layout after successful registration
        except sqlite3.IntegrityError:
            messagebox.showerror(title="Error", message="Username already exists.")
    else:
        messagebox.showerror(title="Error", message="Passwords do not match. Please try again.")


def loginlayout():
    global frame
    frame.destroy()  # Destroy previous frame
    frame = Frame(window, bg='#2A2A6C')
    frame.pack()

    profile_label = Label(frame, image=img1, bg='#2A2A6C')
    profile_label.grid(row=0, column=0, columnspan=2, pady=30)

    login_label = Label(frame, text="Login", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 20))

    username_label = Label(frame, text="Username", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    username_entry = Entry(frame, textvariable=username_var, font=("Arial", 16))

    password_label = Label(frame, text="Password", bg='#2A2A6C', fg="#E1F7F5", font=("Arial", 12))
    password_entry = Entry(frame, show="*", textvariable=password_var, font=("Arial", 16))

    login_button = Button(frame, text="Login", bg="#0E46A3", fg="#E1F7F5", width=20, font=("Arial", 12),
                          command=lambda: login(username_entry, password_entry))

    ortext = Label(frame, text="or", bg="#2A2A6C", fg="#E1F7F5", font=("Arial", 12))
    register_button = Button(frame, text="Register", bg="#9AC8CD", font=("Arial", 12), width=20, command=register)

    login_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)
    username_label.grid(row=2, column=0, sticky=W)
    username_entry.grid(row=3, column=0, pady=10)
    password_label.grid(row=4, column=0, sticky=W)
    password_entry.grid(row=5, column=0, pady=10)
    login_button.grid(row=6, column=0, columnspan=2, pady=20)
    ortext.grid(row=7, column=0, columnspan=2)
    register_button.grid(row=8, column=0, columnspan=2, pady=20)

    # Button to exit
    exit_button = Button(frame, text="Exit", bg="#E5584C", font=("Arial", 12), width=20, command=exit)
    exit_button.grid(row=9, column=0, columnspan=2, pady=20)


def logout():
    global frame
    frame.destroy()  # Destroy previous frame
    loginlayout()


img1 = PhotoImage(file="img/profile.png")
loginlayout()

window.mainloop()
