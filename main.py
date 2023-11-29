import tkinter as tk
from cryptography.fernet import Fernet
import base64
import os
import string
import random
import json

class PasswordManager:
    def __init__(self):
        self.key_file = os.path.join(os.path.dirname(__file__), "password.key")
        self.load_or_generate_key()

        self.cipher_suite = Fernet(self.key)
        self.password_file = os.path.join(os.path.dirname(__file__), "password.json")
        self.windows = []

        self.root = tk.Tk()
        self.center_window(self.root, 500, 350)
        self.root.title("Password Manager")
        self.root.configure(bg="black")  # Set the background color to black    

        self.create_main_buttons()

    def center_window(self, window, window_width, window_height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        
    def load_or_generate_key(self): # done 
        # Load the encryption key from a file or generate a new one
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(self.key)

    def open_window(self, window_type):
        # Open specific windows for saving, retrieving, or updating passwords
        for window in self.windows:
            if window.winfo_exists():
                return  # Do not open a new window if one is already open

        if window_type == "save":
            self.show_save_password_window()
        elif window_type == "retrieve":
            self.show_retrieve_password_window()
        elif window_type == "update":
            self.show_update_password_window()

    def generate_password(self, password_entry):
        # Generate a random password and display it in the given entry field
        password_length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        generated_password = ''.join(random.choice(characters) for _ in range(password_length))
        password_entry.delete(0, 'end')
        password_entry.insert(0, generated_password)

    def create_main_buttons(self):
        # Create the main buttons for saving, retrieving, and updating passwords
        button_padding = 18
        welcome_label = tk.Label(self.root, text="Welcome to Password Manager", bg="black", fg="yellow", font=('Times New Roman', 20))  # Changed color
        welcome_label.pack()

        buttons = [
            ("Save Password", "save"),
            ("Retrieve Password", "retrieve"),
            ("Update Password", "update")
        ]

        for button_text, command in buttons:
            button = tk.Button(self.root, text=button_text, command=lambda cmd=command: self.open_window(cmd), width=20, height=2, bg="black", fg="yellow")  # Changed color
            button.pack(pady=button_padding)

        self.root.mainloop()

    def create_entry(self, window, row, column, pady=10, padx=10, show=None, readonly=False):
        # Create an entry field
        entry = tk.Entry(window, show=show, bg="black", fg="yellow")  # Changed color
        entry.grid(row=row, column=column, pady=pady, padx=padx)
        if readonly:
            entry.config(state='readonly')
        return entry

    def create_label(self, window, text, row, column):
        # Create a label
        label = tk.Label(window, text=text, fg="yellow", font=("Helvetica", "13"), bg="black", padx=7, pady=7)  # Changed color
        label.grid(row=row, column=column)
        return label

    def show_save_password_window(self):
        # Create a window for saving a password
        save_password_window = tk.Toplevel(self.root)
        self.windows.append(save_password_window)
        save_password_window.title("Save Password")
        save_password_window.geometry("450x300")
        self.center_window(save_password_window, 450, 300)
        save_password_window.configure(bg="black")  # Changed color

        labels = ["App Name:", "Username:", "Password:"]
        entries = [self.create_entry(save_password_window, i, 1, 10, 10, show="*") if i == 2 else self.create_entry(save_password_window, i, 1, 10, 10) for i in range(3)]

        for i, label_text in enumerate(labels):
            self.create_label(save_password_window, label_text, i, 0)

        show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(save_password_window, bg="black", text="Show Password", variable=show_password_var, command=lambda: self.toggle_password_visibility(entries[2], show_password_var), fg="yellow")
        show_password_checkbox.grid(row=3, column=0, pady=5)


        generate_password_button = tk.Button(save_password_window, text="Generate Password", bg="black", fg="yellow", command=lambda: self.generate_password(entries[2]))  # Changed color
        generate_password_button.grid(row=3, column=1)

        save_button = tk.Button(save_password_window, text="Save", bg="black", fg="yellow", command=lambda: self.save_password(entries[0], entries[1], entries[2], save_password_window))  # Changed color
        save_button.grid(row=4, column=1, pady=10, padx=20)

        back_button = tk.Button(save_password_window, text="Back", command=lambda: self.close_window(save_password_window), bg="black", fg="yellow", height=1, width=7)  # Changed color
        back_button.grid(row=4, column=0)

    def toggle_password_visibility(self, password_entry, show_password_var):
        # Toggle the visibility of the password in the entry field
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    def show_retrieve_password_window(self):
        # Create a window for retrieving a password
        retrieve_password_window = tk.Toplevel(self.root)
        self.windows.append(retrieve_password_window)
        retrieve_password_window.title("Retrieve Password")
        self.center_window(retrieve_password_window, 450, 300)
        retrieve_password_window.configure(bg="black")  # Changed color

        labels = ["App Name:", "Username:", "Your Password:"]
        # Set readonly=True for the password entry
        entries = [self.create_entry(retrieve_password_window, i, 1, 10, 10, readonly=(i == 2)) for i in range(3)]

        for i, label_text in enumerate(labels):
            self.create_label(retrieve_password_window, label_text, i, 0)

        retrieve_button = tk.Button(retrieve_password_window, text="Retrieve", bg="black", fg="yellow", command=lambda: self.retrieve_password(entries[0], entries[1], entries[2]))  # Changed color
        retrieve_button.grid(row=3, column=1)

        back_button = tk.Button(retrieve_password_window, text="Back", command=lambda: self.close_window(retrieve_password_window), bg="black", fg="yellow", height=1, width=7)  # Changed color
        back_button.grid(row=3, column=0)

    def show_update_password_window(self):
        # Create a window for updating a password
        update_password_window = tk.Toplevel(self.root)
        self.windows.append(update_password_window)
        update_password_window.title("Update Password")
        update_password_window.configure(bg="black")  # Changed color
        self.center_window(update_password_window, 450, 300)

        labels = ["App Name:", "Username:", "Old Password:", "New Password:"]
        entries = [self.create_entry(update_password_window, i, 1, 10, 10, show="*") if i in (2, 3) else self.create_entry(update_password_window, i, 1, 10, 10) for i in range(4)]

        for i, label_text in enumerate(labels):
            self.create_label(update_password_window, label_text, i, 0)

        show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(update_password_window, text="Show Password", variable=show_password_var, command=lambda: self.toggle_password_visibility(entries[3], show_password_var), bg="black", fg="yellow")
        show_password_checkbox.grid(row=4, column=0, pady=5)

        generate_password_button = tk.Button(update_password_window, text="Generate Password", command=lambda: self.generate_password(entries[3]), bg="black", fg="yellow")
        generate_password_button.grid(row=4, column=1)

        update_button = tk.Button(update_password_window, text="Update", bg="black", fg="yellow", command=lambda: self.update_password(entries[0], entries[1], entries[2], entries[3], update_password_window))  # Changed color
        update_button.grid(row=7, column=1, pady=10)

        back_button = tk.Button(update_password_window, text="Back", command=lambda: self.close_window(update_password_window), bg="black", fg="yellow", height=1, width=7)  # Changed color
        back_button.grid(row=7, column=0, pady=10)

    def show_info_label_window(self, message):
        # Create an informational window with a message
        info_label_window = tk.Toplevel(self.root)
        info_label_window.title("Info")
        info_label_window.geometry("300x100")
        info_label_window.configure(bg="black")  # Changed color

        info_label = self.create_label(info_label_window, message, 0, 0)

        quit_button = tk.Button(info_label_window, text="Quit", command=info_label_window.destroy, bg="black", fg="yellow", height=1, width=7)  # Changed color
        quit_button.grid(row=1, column=0, pady=10, padx=20)

    def close_window(self, window):
        # Close a window and remove it from the list of open windows
        self.windows.remove(window)
        window.destroy()

    def save_password(self, app_name_entry, username_entry, password_entry, window):
        # Save a password to a file
        app_name = app_name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if app_name and username and password:
            data = []

            if os.path.exists(self.password_file):
                with open(self.password_file, "r") as file:
                    try:
                        data = json.load(file)
                    except json.decoder.JSONDecodeError:
                        # File is empty or not valid JSON; continue with an empty list
                        pass

            encrypted_password = base64.b64encode(self.cipher_suite.encrypt(password.encode())).decode()

            data.append({"app_name": app_name, "username": username, "password": encrypted_password})

            with open(self.password_file, "w") as file:
                json.dump(data, file, indent=4)

            app_name_entry.delete(0, 'end')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

            self.close_window(window)
        else:
            self.show_info_label_window("Please fill in all fields")

    def retrieve_password(self, app_name_entry, username_entry, password_entry):
        # Retrieve a password from the file
        app_name = app_name_entry.get()
        username = username_entry.get()

        if app_name and username:
            with open(self.password_file, "r") as file:
                data = json.load(file)

            for entry in data:
                if entry["app_name"] == app_name and entry["username"] == username:
                    try:
                        decoded_password = base64.b64decode(entry["password"].encode())
                        decrypted_password = self.cipher_suite.decrypt(decoded_password).decode()
                        password_entry.config(state='normal')
                        password_entry.delete(0, 'end')
                        password_entry.insert(0, decrypted_password)
                        return
                    except Exception as e:
                        self.show_info_label_window("Error decrypting the password")
                        return
            self.show_info_label_window("Password not found")
        else:
            self.show_info_label_window("Please fill in all fields")

    def update_password(self, app_name_entry, username_entry, old_password_entry, new_password_entry, window):
        app_name = app_name_entry.get()
        username = username_entry.get()
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()

        if app_name and username and old_password and new_password:
            with open(self.password_file, "r") as file:
                data = json.load(file)

            found = False
            for entry in data:
                if entry["app_name"] == app_name and entry["username"] == username:
                    found = True
                    try:
                        decoded_password = base64.b64decode(entry["password"].encode())
                        decrypted_password = self.cipher_suite.decrypt(decoded_password).decode()
                        if decrypted_password == old_password:
                            entry["password"] = base64.b64encode(self.cipher_suite.encrypt(new_password.encode())).decode()
                        else:
                            self.show_info_label_window("Old password does not match")
                            return
                    except Exception as e:
                        self.show_info_label_window("Error decrypting the password")
                        return

            if found:
                with open(self.password_file, "w") as file:
                    json.dump(data, file, indent=4)

                app_name_entry.delete(0, 'end')
                username_entry.delete(0, 'end')
                old_password_entry.delete(0, 'end')
                new_password_entry.delete(0, 'end')

                self.close_window(window)
            else:
                self.show_info_label_window("App name or User Name not Found")
        else:
            self.show_info_label_window("Please fill in all fields")

if __name__ == "__main__":
    password_manager = PasswordManager()
