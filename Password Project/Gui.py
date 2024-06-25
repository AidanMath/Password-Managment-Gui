import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import os
from Password_Generator import generate_password
 
def load_or_generate_key():
    key_file = "secret.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
    return key


key = load_or_generate_key()
cipher = Fernet(key)

class NewPasswordDialog:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("New Password")
        
    
        self.min_length_label = tk.Label(self.top, text="Minimum Length:")
        self.min_length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.min_length_entry = tk.Entry(self.top)
        self.min_length_entry.grid(row=0, column=1, padx=10, pady=5)
        
     
        self.include_digits_var = tk.BooleanVar()
        self.include_special_var = tk.BooleanVar()
        self.include_digits_var.set(True)  
        self.include_special_var.set(True)  
        
        self.include_digits_checkbox = tk.Checkbutton(self.top, text="Include Digits", variable=self.include_digits_var)
        self.include_digits_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.include_special_checkbox = tk.Checkbutton(self.top, text="Include Special Characters", variable=self.include_special_var)
        self.include_special_checkbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
       
        self.generate_button = tk.Button(self.top, text="Generate Password", command=self.generate_new_password)
        self.generate_button.grid(row=2, columnspan=2, pady=10)
        
     
        self.password_label = tk.Label(self.top, text="")
        self.password_label.grid(row=3, columnspan=2, pady=5)
        
   
        self.copy_button = tk.Button(self.top, text="Copy Password", command=self.copy_password)
        self.copy_button.grid(row=4, columnspan=2, pady=5)

    def generate_new_password(self):
    
        min_length = int(self.min_length_entry.get())
        include_digits = self.include_digits_var.get()  
        include_special = self.include_special_var.get() 
        
      
        password = generate_password(min_length, include_digits, include_special)
        
        # Display the generated password
        self.password_label.config(text=f"Your new password is:\n{password}")
        
        # Save the generated password
        self.generated_password = password
        
    def copy_password(self):
        if hasattr(self, 'generated_password'):
            self.top.clipboard_clear()  
            self.top.clipboard_append(self.generated_password)  
            self.top.update()  
            messagebox.showinfo("Copy Password", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password generated yet!")

class ViewAddPasswordsDialog:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("View/Add Passwords")

        self.add_new_button = tk.Button(self.top, text="Add New Password", command=self.add_new_password)
        self.add_new_button.pack(pady=10)

        self.view_button = tk.Button(self.top, text="View Existing Passwords", command=self.view_existing_passwords)
        self.view_button.pack(pady=10)

    def add_new_password(self):
        account_name = simpledialog.askstring("Account Name", "Enter the account name:")
        if account_name:
            password = simpledialog.askstring("Password", "Enter the password:")
            if password:
                #Heres where i Encrypt the file
                encrypted_password = cipher.encrypt(password.encode()).decode()
                with open("encrypted_passwords.txt", "a") as file:
                    file.write(f"{account_name}: {encrypted_password}\n")
                    messagebox.showinfo("Password Added", "Password added successfully!")

    def view_existing_passwords(self):
        try:
            with open("encrypted_passwords.txt", "r") as file:
                passwords = file.readlines()
                if passwords:
                    decrypted_passwords = []
                    for line in passwords:
                        account, encrypted_password = line.strip().split(": ")
                        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
                        decrypted_passwords.append(f"{account}: {decrypted_password}")
                    messagebox.showinfo("View Passwords", "\n".join(decrypted_passwords))
                else:
                    messagebox.showinfo("View Passwords", "No passwords stored yet.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. No passwords stored yet.")

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x200")
        self.root.title("Password Manager")

        self.title_font = ('Arial', 24, 'bold')
        self.button_font = ('Arial', 14)

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        
        label = tk.Label(self.root, text="Welcome To Password Manager", font=self.title_font)
        label.pack(pady=(20, 10))  

        buttonframe = tk.Frame(self.root)
        buttonframe.pack(pady=(10, 20)) 

        btn1 = tk.Button(buttonframe, text="Generate New Password", font=self.button_font, width=20, command=self.show_new_password_dialog)
        btn1.grid(row=0, column=0, padx=10)  
        btn2 = tk.Button(buttonframe, text="View/Add Passwords", font=self.button_font, width=20, command=self.show_view_add_passwords_dialog)
        btn2.grid(row=0, column=1, padx=10)  

       
        self.root.eval('tk::PlaceWindow . center')
    
    def show_new_password_dialog(self):
        dialog = NewPasswordDialog(self.root)

    def show_view_add_passwords_dialog(self):
        dialog = ViewAddPasswordsDialog(self.root)

gui = MyGUI()
