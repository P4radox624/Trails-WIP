import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import db_connection
import bcrypt as hash
import re


def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def send_verification_email(email):
    #WIP: Sending Verification Email
    print(f"Verification email sent to {email}. Please check your inbox.")

def show_error(message):
    messagebox.showerror("Error", message)

def register(username, password, password2, email):
    if not username or not password or not email:
        show_error("Please fill in all fields.")
        return

    if not is_valid_email(email):
        show_error("Please enter a valid email address.")
        return

    send_verification_email(email)

    if(password != password2):
        show_error("Passwords doesn't match.")
        return

    # Hash the password using sha256
    hashed_password = hash.hashpw(password.encode(), hash.gensalt())

    try:
        conn = db_connection.connect()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password, email, type) VALUES (%s, %s, %s, 'user')"
        data = (username, hashed_password, email)
        cursor.execute(query, data)

        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        
        # Clear the entry fields
        entry_username_register.delete(0, tk.END)
        entry_password_register.delete(0, tk.END)
        entry_password_register2.delete(0, tk.END)
        entry_email_register.delete(0, tk.END)

    except db_connection.mysql.connector.Error as err:
        messagebox.showerror("Error", err)

    finally:
        cursor.close()
        conn.close()


def login(username, password):
    try:
        conn = db_connection.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and hash.checkpw(password.encode(), user[2].encode()):
            messagebox.showinfo("Success", f"Welcome, {user[1]}!")
            # Close the login window
            root.withdraw()
            # Open the home screen window
            import home_screen
            home_screen.show_home_screen(username,root)
        else:
            show_error("Invalid username or password!")

    except db_connection.mysql.connector.Error as err:
        show_error(err)

    finally:
        cursor.close()
        conn.close()

def show_login_screen():
    register_frame.pack_forget()
    login_frame.pack()

def show_register_screen():
    login_frame.pack_forget()
    register_frame.pack()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Login System")


width_pixels = int(9 * 96 / 2.54)
height_pixels = int(7 * 96 / 2.54)
root.geometry(f"{width_pixels}x{height_pixels}")

login_frame = tk.Frame(root)
register_frame = tk.Frame(root)

# Login Frame
lbl_username_login = tk.Label(login_frame, text="Username:")
lbl_username_login.pack()
entry_username_login = tk.Entry(login_frame)
entry_username_login.pack()

lbl_password_login = tk.Label(login_frame, text="Password:")
lbl_password_login.pack()
entry_password_login = tk.Entry(login_frame, show="*")
entry_password_login.pack()

btn_login = tk.Button(login_frame, text="Login", command=lambda: login(entry_username_login.get(), entry_password_login.get()))
btn_login.pack()

lbl_register = tk.Label(login_frame, text="Don't have an account?")
lbl_register.pack()
btn_register = tk.Button(login_frame, text="Register", command=show_register_screen)
btn_register.pack()

# Register Frame
lbl_username_register = tk.Label(register_frame, text="Username:")
lbl_username_register.pack()
entry_username_register = tk.Entry(register_frame)
entry_username_register.pack()

lbl_email_register = tk.Label(register_frame, text="Email:")
lbl_email_register.pack()
entry_email_register = tk.Entry(register_frame)
entry_email_register.pack()

lbl_password_register = tk.Label(register_frame, text="Password:")
lbl_password_register.pack()
entry_password_register = tk.Entry(register_frame, show="*")
entry_password_register.pack()

lbl_password_register2 = tk.Label(register_frame, text="Confirm Password:")
lbl_password_register2.pack()
entry_password_register2 = tk.Entry(register_frame, show="*")
entry_password_register2.pack()

btn_register = tk.Button(register_frame, text="Register", command=lambda: register(entry_username_register.get(), entry_password_register.get(), entry_password_register2.get(), entry_email_register.get()))
btn_register.pack()

lbl_login = tk.Label(register_frame, text="Already have an account?")
lbl_login.pack()
btn_login = tk.Button(register_frame, text="Login", command=show_login_screen)
btn_login.pack()

show_login_screen()  # Show login screen by default

root.update()
center_window(root)
root.mainloop()
