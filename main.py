from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import json
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    """
    Generates the password using letters, numbers and symbols by shuffling the collection of random characters
    """
    Pass.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list = []
    lettersP = [choice(letters) for char in range(nr_letters)]
    symbolsP = [choice(symbols) for char in range(nr_symbols)]
    numbersP = [choice(numbers) for char in range(nr_numbers)]
    password_list = lettersP + symbolsP + numbersP
    shuffle(password_list)

    password = ''.join(password_list)
    Pass.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add():
    """
    to add a password data to the json file
    """
    password = Pass.get()
    email = Email.get()
    web = website.get()
    new_data = {
        web: {
            "Email": email,
            "Password": password
        }
    }

    if len(web) == 0 or len(password) == 0:
        # pop-up window showing invalid entry into the entry boxes
        messagebox.showinfo(title="Oops!", message="Invalid entry, please try again")
    else:
        try:
            # opens json file
            with open("passwords.json", mode='r') as file:
                # reading old data
                data = json.load(file)
                # adding new data to the existing data
                data.update(new_data)

        except FileNotFoundError:
            # if the file isn't found, it creates one
            with open("passwords.json", mode='w') as file:
                json.dump(new_data, file, indent=4)

            # and then reads it
            with open("passwords.json", mode='r') as file:
                # reading old data
                data = json.load(file)
                # adding new data to the existing data
                data.update(new_data)

        finally:
            # does this regardless of if file is found or not
            with open("passwords.json", mode='w') as file:
                # opening it in write mode allows to overwrite the existing data

                # writing the new data + existing data into the file
                json.dump(data, file, indent=4)

                # pop=up window showing completion of adding data
                messagebox.showinfo(title="Complete!", message="Your entry has been successfully added")

                # deletes the existing text in the entry boxes to accept a new entry
                Pass.delete(0, END)
                website.delete(0, END)


def search():
    """
    opens the json file and searches for the site entered and gives out the data in a pop-up format
    """
    web = website.get()

    if len(web) == 0:
        # pop-up window showing website entry is empty
        messagebox.showinfo(title="Oops!", message="Empty website entry, please try again")
    else:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
            for site in data:
                if site == web:
                    mail = data[site]['Email']
                    password = data[site]["Password"]
                    messagebox.showinfo(title=site, message=f"Email: {mail}\n"
                                                            f"Password: {password}")
                    break
            else:
                messagebox.showinfo(title="Not Found", message="Data isn't available.\n Please enter data")

        except FileNotFoundError:
            messagebox.showinfo(title="Error!", message="File not found, please enter data first.")


# ---------------------------- UI SETUP ------------------------------- #

# creates the interactive gui window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# printing the logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# text boxes and labels
website_txt = Label(text='Website: ')
website_txt.grid(row=1, column=0)

website = Entry(width=24)
website.grid(row=1, column=1)
website.focus()

Email_txt = Label(text="Email/Username: ")
Email_txt.grid(row=2, column=0)

Email = Entry(width=36)
Email.grid(row=2, column=1, columnspan=2)
Email.insert(0, "hello@gmail.com")

Pass_txt = Label(text="Password: ")
Pass_txt.grid(row=3, column=0)
Pass = Entry(width=24)
Pass.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2)

generate_pass_button = Button(text="Generate Password", command=generate_pass)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=add)
add_button.grid(row=4, column=1, columnspan=2)




window.mainloop()
