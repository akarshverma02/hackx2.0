from tkinter import *
from tkinter import messagebox as popup
import json
import plagCheck

user = ""

THEME_COLOR = "#011C26"
BACKGROUND_COLOR = "#B1DDC6"
BUTTON_COLOR = "#D9D6A9"
TEXT_COLOR = "#D9D6A9"
BUTTON_TEXT_COLOR = "#D9D6A9"

window = Tk()
window.title("Plagiarism Checker")
window.config(padx= 200, pady= 250, bg= THEME_COLOR)

def clear_window():
  for children in window.winfo_children():
    children.destroy()

def login_window():
  clear_window()

  sign_up_button = Button(text= "Sign Up", padx=17, pady=2,bg= BUTTON_COLOR, font=("Arial", 14, "bold" ), command=signup_window)
  sign_up_button.grid(column=0, row=2, padx=5, pady=5)
  sign_in_button = Button(text= "Sign In", padx=17, pady=2, bg= BUTTON_COLOR, font=("Arial", 14, "bold" ), command=signin_window)
  sign_in_button.grid(column=1, row=2, padx=5, pady=5)

  sign_up_label= Label(text= "Plagiarism Detector", bg= THEME_COLOR, fg= TEXT_COLOR, font=("Arial", 35, "bold" ))
  sign_up_label.grid(column= 0, row= 0, columnspan=2)
  sign_up_label1= Label(text= "Let's get started.",bg= THEME_COLOR, fg= TEXT_COLOR, font=("Arial", 19, "normal" ))
  sign_up_label1.grid(column= 0, row= 1, columnspan=2, pady=5 )

def signup_window():
  clear_window()

  sign_up_label = Label(text = "Sign Up",font=("Jet", 35, "bold"), bg= THEME_COLOR, fg= TEXT_COLOR)
  sign_up_label.grid(column= 1, row= 0, padx= 35, pady= 20, columnspan=2)
  username_label1 = Label(text= "Username:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  username_label1.grid(column=0, row=1)
  email_label1= Label(text= "Email:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  email_label1.grid(column=0, row=2)
  password_label1= Label(text="Password:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  password_label1.grid(column=0, row= 3)
  password_confirm_label1= Label(text="Password Confirmation:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  password_confirm_label1.grid(column=0, row= 4)

  username_entry1= Entry(width = 45)
  username_entry1.grid(column=1, row=1)
  email_entry1 = Entry(width = 45)
  email_entry1.grid(column=1, row=2)
  password_entry1= Entry(width = 45)
  password_entry1.grid(column= 1, row = 3)
  password_confirm_entry1= Entry(width = 45)
  password_confirm_entry1.grid(column= 1, row = 4)

  sign_up_button= Button(text= "Sign Up", bg= "#6CD95B", width = 15, font=("Arial", 14, "bold" ), command=lambda: create_account(username_entry1.get(),email_entry1.get(),password_entry1.get(),password_confirm_entry1.get()))
  sign_up_button.grid(column = 1, row=5, columnspan=2, pady=5)

def create_account(username, email, password, confirm_password):
  if password!=confirm_password:
    popup.showerror(message="Password Doesnt Match")
  else:
    with open("Hackethon/user.json",'r') as user_file:
      data = json.load(user_file)
    if username in data.keys():
      popup.showerror(message="Username exits")
    else:
      data[username] = {'email':email,'pass':password}
      with open("Hackethon/user.json",'w') as user_file: 
        json.dump(data,user_file,indent=4)
      signin_window()
        
def signin_window():
  clear_window()

  sign_in_label = Label(text = "Sign In",font=("Arial", 35, "bold"), bg= THEME_COLOR, fg= TEXT_COLOR)
  sign_in_label.grid(column= 1, row= 0, padx= 35, pady= 20, columnspan=2)
  username_label = Label(text= "Username:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  username_label.grid(column=0, row=1)
  password_label= Label(text="Password:", fg= TEXT_COLOR, bg= THEME_COLOR, font=("Arial", 14, "normal" ))
  password_label.grid(column=0, row= 3)

  username_entry= Entry(width = 45)
  username_entry.grid(column=1, row=1)
  password_entry= Entry(width = 45)
  password_entry.grid(column= 1, row = 3)

  log_in_button= Button(text= "Log In", bg= "#6CD95B", width = 15, font=("Arial", 14, "bold"), command=lambda:check_info(username_entry.get(),password_entry.get()))
  log_in_button.grid(column =1, row=5, columnspan=2, pady=5)

def check_info(username,password):
  global user 

  with open("Hackethon/user.json",'r') as user_file:
      data = json.load(user_file)
  if username in data.keys():
    if data[username]['pass'] == password:
      user = username
      plag_window()
    else:
      popup.showerror(message="Wrong Password!")
  else:
    popup.showerror(message="Username does not exist!")

def plag_window():
  clear_window()

  enter_entry = Text(width=100, height=25, font=("Arial", 14, "normal" ))
  enter_entry.grid(row=0, column=0)

  enter_button = Button(text= "Check", bg= BUTTON_COLOR, padx= 15 , font=("Arial", 14, "bold"), command=lambda:check_plag(enter_entry.get("1.0",END)))
  enter_button.grid(row= 1, column=0, padx= 10, pady=2)

def check_plag(code1):
  global user

  with open("Hackethon/data.json",'r') as code_file:
    data = json.load(code_file)
  
  flag = 0

  for code2 in data.values():
    plag = plagCheck.plag_check(code1,code2)
    if not(plag):
      flag = 1
      break
  
  if flag == 0:
    popup.showinfo(message="Original Content")
    with open("Hackethon/data.json",'w') as code_file:
      data[f"code{int(list(data.keys())[-1][-1])+1}"] = code1
      json.dump(data,code_file,indent=4)
  else:
    popup.showinfo(message="PLAGRIARISM DETECTED")
    with open('Hackethon/flagged_users.json','r') as flagged_file:
      flagged_data = json.load(flagged_file)
    with open('Hackethon/flagged_users.json','w') as flagged_file:
      flagged_data['users'].append(user)
      json.dump(flagged_data,flagged_file,indent=4)

login_window()

window.mainloop()