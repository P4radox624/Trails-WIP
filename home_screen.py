import tkinter as tk

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def logout(home_window, login_window):
    home_window.destroy()
    login_window.deiconify()

def show_home_screen(username, login_window):
    home_window = tk.Tk()
    home_window.title("Home Screen")

    # Set the dimensions of the home window to be the same as the login window
    width_pixels = int(login_window.winfo_width())
    height_pixels = int(login_window.winfo_height())
    home_window.geometry(f"{width_pixels}x{height_pixels}")

    # Center the window
    center_window(home_window)

    # Create a label to display the welcome message
    welcome_label = tk.Label(home_window, text=f"Welcome, {username}!")
    welcome_label.pack(pady=20)

    # Create a logout button
    btn_logout = tk.Button(home_window, text="Logout", command=lambda: logout(home_window, login_window))
    btn_logout.pack(side=tk.BOTTOM, pady=10)

    home_window.mainloop()
