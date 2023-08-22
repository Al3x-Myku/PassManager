import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from redis_manager import RedisManager

def add_row():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not site or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    redis_manager.add_entry(site, username, password)

    tree.insert("", "end", values=(site, username, "****"))
    site_entry.delete(0, "end")
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")

def show_password():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        site = item["values"][0]
        username = item["values"][1]
        password = redis_manager.get_password(site, username)
        if password:
            messagebox.showinfo("Password", f"The password for this entry is: {password}")
        else:
            messagebox.showinfo("Password", "Password not found in the database.")

def clear_database():
    result = messagebox.askyesno("Clear Database", "Are you sure you want to clear the database?")
    if result:
        redis_manager.clear_database()
        load_data_from_redis()

def load_data_from_redis(filter_site=None):
    tree.delete(*tree.get_children())
    keys = redis_manager.redis_client.keys()
    for key in keys:
        site = key
        if not filter_site or filter_site.lower() in site.lower():
            usernames_passwords = redis_manager.redis_client.hgetall(key)
            for username in usernames_passwords:
                tree.insert("", "end", values=(site, username, "****"))

root = tk.Tk()
root.title("Password Manager")

# Create Treeview widget
tree = ttk.Treeview(root, columns=("Site", "Username", "Password"), show="headings")
tree.heading("Site", text="Site")
tree.heading("Username", text="Username")
tree.heading("Password", text="Password")
tree.pack(padx=20, pady=20, expand=True, fill="both")

# Entry fields for adding rows
site_label = tk.Label(root, text="Site:")
site_label.pack(anchor="w", padx=20)
site_entry = tk.Entry(root)
site_entry.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

username_label = tk.Label(root, text="Username:")
username_label.pack(anchor="w", padx=20)
username_entry = tk.Entry(root)
username_entry.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

password_label = tk.Label(root, text="Password:")
password_label.pack(anchor="w", padx=20)
password_entry = tk.Entry(root, show="*")
password_entry.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

# Add Entry button
add_button = tk.Button(root, text="Add Entry", command=add_row)
add_button.pack(side="left", padx=20)

# Show Password button
show_password_button = tk.Button(root, text="Show Password", command=show_password)
show_password_button.pack(side="left", padx=20)

# Clear Database button
clear_button = tk.Button(root, text="Clear Database", command=clear_database)
clear_button.pack(side="left", padx=20)

# Search Site
search_label = tk.Label(root, text="Search Site:")
search_label.pack(anchor="w", padx=20)
search_entry = tk.Entry(root)
search_entry.pack(side="left", anchor="w", padx=20, pady=(0, 10), fill="x", expand=True)

# Search button
search_button = tk.Button(root, text="Search", command=load_data_from_redis)
search_button.pack(side="left", anchor="w", padx=(0, 10), pady=10)

# Create a RedisManager instance
redis_manager = RedisManager()

# Load data from Redis
load_data_from_redis()

root.mainloop()