import tkinter as tk
import os
import json
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import simpledialog

# Global list to store tasks
#tasks = []
TASKS_FILE = "tasks.json"

# Function to load tasks from file
def load():
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

# Function to save tasks to file
def save():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Call load function when the application starts
load()

def add_task():
    # Create a new window for adding tasks
    add_task_window = tk.Toplevel()
    add_task_window.title("Create Task")

    # Label and entry for task name
    lbl_task_name = tk.Label(add_task_window, text="Task:")
    lbl_task_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_task_name = tk.Entry(add_task_window)
    entry_task_name.grid(row=0, column=1, padx=10, pady=5)

    # Calendar for selecting due date
    lbl_due_date = tk.Label(add_task_window, text="Set Date:")
    lbl_due_date.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    cal_due_date = Calendar(add_task_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal_due_date.grid(row=1, column=1, padx=10, pady=5)

    # Function to save the task with name and due date
    def save_task():
        task_name = entry_task_name.get()
        due_date = cal_due_date.get_date()
        # Save the task to the global list
        tasks.append({"name": task_name, "due_date": due_date, "notes": ""})  # Initialize notes as empty string
        save()
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()

    # Button to save the task
    btn_save = tk.Button(add_task_window, text="Save", command=save_task)
    btn_save.grid(row=2, column=0, columnspan=2, pady=10)

def delete_task(tree):
    # Function to delete selected task
    selected_item = tree.selection()
    if not selected_item:
        show_error("Please select a task to delete.")
        return

    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected task?")
    if not confirmed:
        return

    for item in selected_item:
        task_name = tree.item(item, "values")[0]
        for task in tasks:
            if task["name"] == task_name:
                tasks.remove(task)
                save()
                tree.delete(item)

def check_due_dates():
    # Get the current date
    current_date = datetime.now().date()

    # List to store tasks with matching deadlines
    matching_tasks = []

    # Iterate through tasks
    for task in tasks:
        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        if due_date == current_date + timedelta(days=1):
            matching_tasks.append(task["name"])

    # If there are matching tasks, display them in a single messagebox
    if matching_tasks:
        messagebox.showinfo("Reminder", f"The following tasks are due tomorrow:\n\n{', '.join(matching_tasks)}")

def view_tasks():
    # Create a new window for viewing tasks
    view_tasks_window = tk.Toplevel()
    view_tasks_window.title("View Tasks")

    # Create a label to display instructions
    lbl_instructions = tk.Label(view_tasks_window, text="List of Tasks:")
    lbl_instructions.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create a treeview widget to display tasks
    tree = ttk.Treeview(view_tasks_window, columns=("Task Name", "Due Date"), show="headings")
    tree.heading("Task Name", text="Task Name")
    tree.heading("Due Date", text="Due Date")
    tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # Add tasks to the treeview
    for task in tasks:
        tree.insert("", "end", values=(task["name"], task["due_date"]))

    # Add scrollbar to the treeview
    scrollbar = ttk.Scrollbar(view_tasks_window, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Create a text widget for notepad
    txt_notepad = tk.Text(view_tasks_window, wrap="word")
    txt_notepad.grid(row=1, column=2, rowspan=4, padx=10, pady=5, sticky="nsew")  # Adjust rowspan as needed

    # Function to load notes for selected task
    def load_notes():
        selected_item = tree.selection()
        if selected_item:
            task_name = tree.item(selected_item, "values")[0]
            for task in tasks:
                if task["name"] == task_name:
                    if "notes" in task:
                        txt_notepad.delete("1.0", tk.END)  # Clear existing notes
                        txt_notepad.insert(tk.END, task["notes"])  # Load notes for selected task
                        return  # Exit function if notes are found
        # Clear text widget if no notes found
        txt_notepad.delete("1.0", tk.END)

    # Bind treeview selection to load notes
    tree.bind("<<TreeviewSelect>>", lambda event: load_notes())

    # Function to save notes for selected task
    def save_notes():
        selected_item = tree.selection()
        if selected_item:
            task_name = tree.item(selected_item, "values")[0]
            for task in tasks:
                if task["name"] == task_name:
                    task["notes"] = txt_notepad.get("1.0", tk.END)  # Save notes for selected task
                    save()
                    messagebox.showinfo("Success", "Notes saved successfully!")

    # Add a button to save notes
    btn_save_notes = tk.Button(view_tasks_window, text="Save Notes", command=save_notes)
    btn_save_notes.grid(row=5, column=2, pady=10, sticky="e")

    # Add Edit Task Due Date button
    btn_edit_due_date = tk.Button(view_tasks_window, text="Edit Due Date", command=lambda: edit_task_due_date(tree, view_tasks_window), font=("yu gothic ui", 10))
    btn_edit_due_date.grid(row=6, column=0, columnspan=2, pady=10)

    # Add delete button
    btn_delete_task = tk.Button(view_tasks_window, text="Delete Task", command=lambda: delete_task(tree), font=("yu gothic ui", 10))
    btn_delete_task.grid(row=7, column=0, columnspan=2, pady=10)

def show_error(message):
    messagebox.showerror("Error", message)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def logout(home_window, login_window):
    save()
    home_window.destroy()
    login_window.deiconify()

def show_home_screen(username, login_window):
    home_window = tk.Tk()
    home_window.title("Trails")

    # Set the dimensions of the home window to be the same as the login window
    width_pixels = int(login_window.winfo_width())
    height_pixels = int(login_window.winfo_height())
    home_window.geometry(f"{width_pixels}x{height_pixels}")

    # Center the window
    center_window(home_window)

    # Create a header frame
    header_frame = tk.Frame(home_window, bg="#e21818")  # Set background color to empty string for transparency
    header_frame.pack(fill="x")

    # Create a label to display the username in the header
    lbl_username = tk.Label(header_frame, text=f"{username}'s Trails!", font=("yu gothic ui", 12, "bold"), bg="#e21818", fg="white", padx=10, pady=5)
    lbl_username.pack(side="left")

    # Function to toggle the menu
    def toggle_menu():
        if menu.winfo_ismapped():
            menu.unpost()
        else:
            menu.post(btn_hamburger.winfo_rootx(), btn_hamburger.winfo_rooty() + btn_hamburger.winfo_height())

    # Create a menu
    menu = tk.Menu(home_window, tearoff=0)
    menu.add_command(label="Logout", command=lambda: logout(home_window, login_window))
    menu.add_separator()
    menu.add_command(label="Close", command=home_window.quit)

    # Create a hamburger button
    btn_hamburger = tk.Button(header_frame, text="\u2630", command=toggle_menu, font=("Arial", 12), bg="#e21818", fg="white", bd=0)
    btn_hamburger.pack(side="right", padx=10, pady=5)

    # Create a main frame for content
    main_frame = tk.Frame(home_window)
    main_frame.pack(expand=True, fill="both")

     # Button to add task
    btn_add_task = tk.Button(main_frame, text="+", font=("Helvetica", 24), command=add_task, bg="red", fg="white")
    btn_add_task.place(relx=1, rely=1, anchor="se", x=-20, y=-20)  # Placing the button at the bottom right with some padding

    # Add a button to view tasks
    btn_view_tasks = tk.Button(main_frame, text="View Tasks", command=view_tasks, font=("yu gothic ui", 10))
    btn_view_tasks.grid(row=1, column=0, columnspan=2, pady=10)  # Center the button horizontally

    # Button to manually check for upcoming due dates
    btn_check_due_dates = tk.Button(main_frame, text="Check Due Dates", command=check_due_dates, font=("yu gothic ui", 10))
    btn_check_due_dates.grid(row=2, column=0, columnspan=2, pady=10)  # Center the button horizontally

    home_window.mainloop()

def edit_task_due_date(tree, parent_window):
    selected_item = tree.selection()
    if not selected_item:
        show_error("Please select a task to edit.")
        return

    # Assuming the task name is in the first column
    task_name = tree.item(selected_item[0], "values")[0]

    # Create a new window for editing the due date
    edit_due_date_window = tk.Toplevel(parent_window)
    edit_due_date_window.title("Edit Due Date")

    # Function to update the due date in real-time
    def update_due_date(event):
        new_due_date = cal_new_due_date.get_date()
        # Update the task in the global tasks list
        for task in tasks:
            if task["name"] == task_name:
                task["due_date"] = new_due_date
                tree.item(selected_item, values=(task["name"], task["due_date"]))  # Update the due date in the treeview
                save()
                break

    # Calendar for selecting new due date
    cal_new_due_date = Calendar(edit_due_date_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal_new_due_date.pack(padx=10, pady=10)

    # Bind calendar selection event to update_due_date function
    cal_new_due_date.bind("<<CalendarSelected>>", update_due_date)

    # Function to save the new due date
    def save_new_due_date():
        new_due_date = cal_new_due_date.get_date()
        # Update the task in the global tasks list
        for task in tasks:
            if task["name"] == task_name:
                task["due_date"] = new_due_date
                save()
                messagebox.showinfo("Success", "Due date updated successfully!")
                edit_due_date_window.destroy()
                return

    # Button to save the new due date
    btn_save_new_due_date = tk.Button(edit_due_date_window, text="Save", command=save_new_due_date)
    btn_save_new_due_date.pack(pady=10)

# For testing purposes
# show_home_screen("John", None)