import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import csv


usernames = []
passwords = []

font1 = 'Arial, 22'
font2 = 'Arial, 18'

def opening_to_read():
    global usernames, passwords
    usernames , passwords = [], []
    with open('login_details.csv', newline='') as file:
        file_reader = csv.reader(file, delimiter=',')
        for row in file_reader:
            if len(row) >= 2:
                usernames.append(row[0])
                passwords.append(row[1])



window = tk.Tk()
window.configure(bg='black')
window.columnconfigure((0,1,3,4), weight=1, minsize=100)
window.columnconfigure(2, weight=1, minsize=250)

bg_img = ImageTk.PhotoImage(Image.open(r"assets\chessBackground.jpg"))
img_lbl = tk.Label(image=bg_img, master=window)
img_lbl.place(x=0, y=0)

def lgn_btn_top(): #what happens when the button at the top to log in is pressed. Changes form sign in to log in screen.
    opening_to_read()
    login_button.grid(row=4, column=2, pady=20)
    signup_btn.grid_remove()
    error_msg2.grid_remove()
    error_msg3.grid_remove()

def sup_btn_top(): #changes from login to sign in screen.
    login_button.grid_remove()
    signup_btn.grid(row=4, column=2, pady=20)
    error_msg1.grid_remove()

error_msg1 = tk.Label(text='Username or password incorrect', fg='red')
error_msg2 = tk.Label(text='Username taken', fg='red')
error_msg3 = tk.Label(text="Password/Username can't be empty", fg='red')

login_btn_top = tk.Button(
    font = font2,
    text = "Log In",
    bg = 'grey',
    fg = 'black', #changes the colour of the text (foreground). background = '' (or can use bg instead) to change the colour of the background.
    width = 10, #defined in terms of height and width of 0
    height = 1,
    command = lgn_btn_top)

signup_btn_top = tk.Button(
    font = font2,
    bg = 'grey',
    text = "Sign Up",
    fg = 'black', #changes the colour of the text (foreground). background = '' (or can use bg instead) to change the colour of the background.
    width = 10, #defined in terms of height and width of 0
    height = 1,
    command = sup_btn_top)

user_inp = tk.Entry(
    width = 20,
    font = font1,
    borderwidth = 5,
    relief = tk.SUNKEN)

passw_inp = tk.Entry(
    width = 20,
    font = font1,
    borderwidth = 5,
    relief = tk.SUNKEN,
    show = '*')
#when the login button is pressed it searches through the database and checks if the username and pasword match.
#error message is displayed on the screen otherwisde chess is loaded.
def pressing_login_btn():
    print('button pressed')
    username = user_inp.get()
    password = passw_inp.get()
    if username in usernames:
        username_index = usernames.index(username)
        if passwords[username_index] == password:
            print('logged in')
            import starterScreen
    error_msg1.grid(row=3,column=2)

login_button = tk.Button(
    font = font2,
    text = 'Log in',
    width = 10,
    height = 1,
    borderwidth = 5,
    relief = tk.RAISED,
    command = pressing_login_btn)

def pressing_signup_btn():
    error_msg2.grid_remove()
    error_msg3.grid_remove()
    username = user_inp.get()
    password = passw_inp.get()
    if username in usernames:
        error_msg2.grid(row=3,column=2)
    elif len(username) == 0 or len(password) == 0:
        error_msg3.grid(row=3,column=2)
    else:
        with open('login_details.csv', 'a', newline='') as file:
            file_writer = csv.writer(file, delimiter = ',')
            logindetails = [username, password]
            file_writer.writerow(logindetails)
            import starterScreen
            return

signup_btn = tk.Button(
    font = font2,
    text = 'Sign up',
    width = 10,
    height = 1,
    borderwidth = 5,
    relief = tk.RAISED,
    command = pressing_signup_btn)

login_btn_top.grid(row=0, column=2,sticky='w', pady=20)
signup_btn_top.grid(row=0, column=2, sticky='e')
tk.Label(text = 'Username:', font=font2).grid(row=1, column=1, sticky='e', pady=20)
user_inp.grid(row=1, column=2, sticky='ew')
tk.Label(text = 'Password:', font=font2).grid(row=2, column=1, sticky='e', pady=20)
passw_inp.grid(row=2, column=2, sticky='ew')

lgn_btn_top()
print(passwords, usernames)
window.mainloop()
