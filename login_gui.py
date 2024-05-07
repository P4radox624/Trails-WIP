import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import db_connection
import bcrypt as hash
import re
import media
from media import *

# Functions for password visibility toggling and user registration
def login_toggle_password_visibility():
    if entry_password_login.cget("show") == "":
        entry_password_login.config(show="*")
        eye_button_login.config(bg="#D0D0D0")
    else:
        entry_password_login.config(show="")
        eye_button_login.config(bg="#F0F0F0")

def register_toggle_password_visibility():
    if entry_password_register.cget("show") == "":
        entry_password_register.config(show="*")
        entry_password_register2.config(show="*")
        eye_button_register.config(bg="#D0D0D0")
    else:
        entry_password_register.config(show="")
        entry_password_register2.config(show="")
        eye_button_register.config(bg="#F0F0F0")

def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def send_verification_email(email):
    # WIP: Sending Verification Email
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

    if password != password2:
        show_error("Passwords don't match.")
        return

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

        # Switch to the login screen
        show_login_screen()

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
            home_screen.show_home_screen(username, root)
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

# Main window
root = tk.Tk()
root.title("Login")

# Eye icon image
img = Image.open(eye_logo)
img = img.resize((25, 15))
eye_img = ImageTk.PhotoImage(img)

# Calculate width based on desired height
height_pixels = int(16 * 96 / 2.54)
width_pixels = int(height_pixels * 11 / 16)
root.geometry(f"{width_pixels}x{height_pixels}")

# Login and register frames
login_frame = tk.Frame(root)
register_frame = tk.Frame(root)

# Common padding configuration
padding_y = (10, 5)

# Logo
logo_image = tk.PhotoImage(file=media.sp_logo)
logo_image_resized = logo_image.subsample(20)
logo_label = tk.Label(login_frame, image=logo_image_resized)
logo_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="w")

# Title Label
lbl_title = tk.Label(login_frame, text="TRAILS", font=("yu gothic ui", 20, "bold"), width=25, bd=0)
lbl_title.grid(row=0, column=1, pady=(0, 5), sticky="ew")

# Username and Password Container Frame
login_entry_frame = tk.Frame(login_frame)
login_entry_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Username Label and Entry
lbl_username_login = tk.Label(login_entry_frame, text="Username:", font=("yu gothic ui", 12))
lbl_username_login.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=padding_y)
entry_username_login = tk.Entry(login_entry_frame, highlightthickness=0, fg="#6b6a69", font=("yu gothic ui ", 12), insertbackground="#6b6a69")
entry_username_login.grid(row=0, column=1, padx=(0, 10), pady=padding_y)

# Password Label, Entry, and Eye Button
lbl_password_login = tk.Label(login_entry_frame, text="Password:", font=("yu gothic ui", 12))
lbl_password_login.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=padding_y)
entry_password_login = tk.Entry(login_entry_frame, show="*", highlightthickness=0, fg="#6b6a69", font=("yu gothic ui", 12), insertbackground="#6b6a69")
entry_password_login.grid(row=1, column=1, padx=(0, 10), pady=padding_y, sticky="ew")
eye_button_login = tk.Button(login_entry_frame, image=eye_img, state="active", command=login_toggle_password_visibility)
eye_button_login.grid(row=1, column=2, padx=(0, 5), pady=padding_y, sticky="w")

# Login Button
btn_login = tk.Button(login_entry_frame, text="LOGIN", command=lambda: login(entry_username_login.get(), entry_password_login.get()), font=("yu gothic ui", 13, "bold"),
                      width=25, bd=0, bg='#e21818', cursor='hand2', activebackground='#e21818', fg='white')
btn_login.grid(row=2, column=0, columnspan=3, pady=(15, 0), padx=10)

# "Don't have an account?" Label and "SIGN UP NOW" Button
lbl_register = tk.Label(login_frame, text="Don't have an account?", font=("yu gothic ui", 12))
lbl_register.grid(row=2, column=0, columnspan=4, pady=padding_y)
btn_register = tk.Button(login_frame, text="SIGN UP NOW", command=show_register_screen, font=("yu gothic ui", 13, "bold"),
                      width=25, bd=0, bg='#e21818', cursor='hand2', activebackground='#e21818', fg='white')
btn_register.grid(row=3, column=0, columnspan=4, pady=(0, 10), padx=10)

# Register Frame

# Title Label
lbl_title_register = tk.Label(register_frame, text="TRAILS", font=("yu gothic ui", 20, "bold"), width=25, bd=0)
lbl_title_register.grid(row=0, column=1, pady=(0, 5), sticky="ew")

# Ensure proper row configuration to adjust row height
register_frame.grid_rowconfigure(1, weight=1)  # Allow row to expand vertically

# Center the title label horizontally
register_frame.grid_columnconfigure(1, weight=1)  # Allow column to expand

# Username Label and Entry
lbl_username_register = tk.Label(register_frame, text="Username:", font=("yu gothic ui", 12))
lbl_username_register.grid(row=2, column=0, padx=5, pady=padding_y)
entry_username_register = tk.Entry(register_frame)
entry_username_register.grid(row=2, column=1, padx=5, pady=padding_y)

# Email Label and Entry
lbl_email_register = tk.Label(register_frame, text="Email:", font=("yu gothic ui", 12))
lbl_email_register.grid(row=3, column=0, padx=5, pady=padding_y)
entry_email_register = tk.Entry(register_frame)
entry_email_register.grid(row=3, column=1, padx=5, pady=padding_y)

# Password Label and Entry
lbl_password_register = tk.Label(register_frame, text="Password:", font=("yu gothic ui", 12))
lbl_password_register.grid(row=4, column=0, padx=5, pady=padding_y)
entry_password_register = tk.Entry(register_frame, show="*")
entry_password_register.grid(row=4, column=1, padx=5, pady=padding_y)

# Confirm Password Label and Entry
lbl_password_register2 = tk.Label(register_frame, text="Confirm Password:", font=("yu gothic ui", 12))
lbl_password_register2.grid(row=5, column=0, padx=5, pady=padding_y)
entry_password_register2 = tk.Entry(register_frame, show="*")
entry_password_register2.grid(row=5, column=1, padx=5, pady=padding_y)

# Eye Button for Password
eye_button_register = tk.Button(register_frame, image=eye_img, state="active", command=register_toggle_password_visibility)
eye_button_register.grid(row=4, column=2, padx=5, pady=padding_y, sticky="w")

# Eye Button for Confirm Password
eye_button_register = tk.Button(register_frame, image=eye_img, state="active", command=register_toggle_password_visibility)
eye_button_register.grid(row=5, column=2, padx=5, pady=padding_y, sticky="w")

# Register Button
btn_register = tk.Button(register_frame, text="SIGN UP", command=lambda: register(entry_username_register.get(), entry_password_register.get(), entry_password_register2.get(), entry_email_register.get()), font=("yu gothic ui", 13, "bold"),
                          width=25, bd=0, bg='#e21818', cursor='hand2', activebackground='#e21818', fg='white')
btn_register.grid(row=6, column=0, columnspan=4, pady=(15, 0), padx=10)

# "Already have an account?" Label
lbl_login = tk.Label(register_frame, text="Already have an account?", font=("yu gothic ui", 12))
lbl_login.grid(row=7, column=0, columnspan=4, pady=padding_y)

# "LOGIN" Button
btn_login = tk.Button(register_frame, text="LOGIN", command=show_login_screen, font=("yu gothic ui", 13, "bold"),
                      width=25, bd=0, bg='#e21818', cursor='hand2', activebackground='#e21818', fg='white')
btn_login.grid(row=8, column=0, columnspan=4, pady=(0, 10), padx=10)

show_login_screen()  # Show login screen by default

root.update()
center_window(root)
root.mainloop()
