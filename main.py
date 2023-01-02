from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
YOUR_EMAIL = ""  # type your email id here for autofill

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search():
    ws = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            if ws in data:
                show_email = data[ws]["email"]
                show_pw = data[ws]["password"]
                pyperclip.copy(show_pw)
                messagebox.showinfo(message=f"E-mail: {show_email}\nPassword: {show_pw}")
            else:
                messagebox.showinfo(title="Error", message="No details found")
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message=" No records found")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def pw_generate():
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "J",
               "M", "N", "O", "P", "Q", "R", "S", "T", "V", "X", "Y", "Z"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "@", "#", "%", "&", "(", ")", "*", "+"]

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    digits_list = [choice(digits) for _ in range(randint(2, 4))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = letters_list + digits_list + symbol_list
    shuffle(password_list)
    my_password = "".join(password_list)
    pyperclip.copy(my_password)
    password_entry.delete(0, END)
    password_entry.insert(0, my_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pw():
    website_name = website_entry.get()
    user_name = email_entry.get()
    user_pw = password_entry.get()
    new_data = {
        website_name: {
            "email": user_name,
            "password": user_pw,
        }
    }

    if len(website_name) == 0 or len(user_name) == 0 or len(user_pw) == 0:
        messagebox.showinfo(title="opps", message="Please don't leave any fields empty.")

    else:
        is_okay = messagebox.askokcancel(title=website_name, message=f"These are the details entered: \n"
                                                                     f"Email: {user_name}\nPassword: {user_pw}")
        if is_okay:
            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("MyPass")
window.minsize(width=500, height=400)
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website:")
website.grid(column=0, row=1)
website.config(pady=3)
email = Label(text="Email/Username:")
email.grid(column=0, row=2)
email.config(pady=3)
password = Label(text="Password:")
password.grid(column=0, row=3)
password.config(pady=3)

# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2)
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

website_entry.focus()
email_entry.insert(0, YOUR_EMAIL)

# Buttons
search_btn = Button(text="search", width=11, command=search)
search_btn.grid(column=2, row=1)
generate_password = Button(text="    Generate     ", command=pw_generate)
generate_password.grid(row=3, column=2)
add_bth = Button(text="add", width=36, command=save_pw)
add_bth.grid(column=1, row=4, columnspan=2)

window.mainloop()
