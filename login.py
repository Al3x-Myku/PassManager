import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace with your authentication logic
        if username == "admin" and password == "password":
            self.root.destroy()  # Close the login window
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
