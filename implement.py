import os
import mysql.connector
import curses
import time
from curses import wrapper
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="damn"
)
except Exception:
    print("couldn't connect to database")
    exit()

cursor = mydb.cursor()
cursor.execute("show databases")
db = cursor.fetchall()

if 'hk_ntpd' not in db:
    try:
        cursor.execute("create database hk_ntpd")
    except Exception as e:
        pass
cursor.execute("use hk_ntpd")
cursor.execute("show tables")
table = cursor.fetchall()

if 'data' not in table:
    try:
        cursor.execute("""
CREATE TABLE data (
    name VARCHAR(50),
    path VARCHAR(200)
);
""")
    except Exception as e:
        pass
filepath = input("Enter filepath :")
def create(y):
    y.addstr(0, 0, "Press any key to start the Text Editor \nPress F2 to exit", curses.A_BOLD | curses.A_UNDERLINE)  # Specify the coordinates for the string
    y.refresh()  # if I remove this, 'hello' will not print
    y.getch()
    y.clear()
    y.refresh()
    time.sleep(0.3)

    max_y, max_x = y.getmaxyx()

    global text
    text = " "
    while True:
        key = y.getch()
        yy, x = y.getyx()
        try:
            if key == curses.KEY_F2:
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                if x > 0:
                    y.addch(yy, x - 1, ' ')
                    y.move(yy, x - 1)
                    y.refresh()
                elif x == 0 and yy > 0:
                    y.move(yy - 1, len(text))
                    y.refresh()
            elif key == curses.KEY_UP:
                if yy > 0:
                    y.move(yy - 1, x)
                    y.refresh()
            elif key == curses.KEY_DOWN:
                if yy < max_y - 1:
                    y.move(yy + 1, x)
                    y.refresh()
            elif key == curses.KEY_LEFT:
                if x > 0:
                    y.move(yy, x - 1)
                    y.refresh()
                elif x == 0 and yy > 0:
                    y.move(yy - 1, len(text))
                    y.refresh()
            elif key == curses.KEY_RIGHT:
                if x < max_x - 1:
                    y.move(yy, x + 1)
                    y.refresh()
                elif x == max_x - 1 and yy < max_y - 1:
                    y.move(yy + 1, 0)
                    y.refresh()
            else:
                text += chr(key)
                try:
                    y.addch(key)
                except:
                    pass
                y.refresh()
        except:
            pass
def edit(y):
    y.addstr(0, 0, "Press any key to start the Text Editor \nPress F2 to exit", curses.A_BOLD | curses.A_UNDERLINE)  # Specify the coordinates for the string
    y.refresh()  # if I remove this, 'hello' will not print

    time.sleep(0.3)
    global text2
    with open(filepath,"r") as f:
        text2 = f.read()
    y.getch()
    y.clear()
    y.refresh()
    max_y, max_x = y.getmaxyx()
    key = y.addstr(text2)
    while True:
        key = y.getch()
        yy, x = y.getyx()
        try:
            if key == curses.KEY_F2:
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                if x > 0:
                    y.addch(yy, x - 1, ' ')
                    y.move(yy, x - 1)
                    y.refresh()
                if len(text2)>0:
                    text2 = text2[:-1]
                elif x == 0 and yy > 0:
                    y.move(yy - 1, max_x-1)
                    y.refresh()
            elif key == curses.KEY_UP:
                if yy > 0:
                    y.move(yy - 1, x)
                    y.refresh()
            elif key == curses.KEY_DOWN:
                if yy < max_y - 1:
                    y.move(yy + 1, x)
                    y.refresh()
            elif key == curses.KEY_LEFT:
                if x > 0:
                    y.move(yy, x - 1)
                    y.refresh()
                elif x == 0 and yy > 0:
                    y.move(yy - 1, max_x - 1)
                    y.refresh()
            elif key == curses.KEY_RIGHT:
                if x < max_x - 1:
                    y.move(yy, x + 1)
                    y.refresh()
                elif x == max_x - 1 and yy < max_y - 1:
                    y.move(yy + 1, 0)
                    y.refresh()
            else:
                text2 += chr(key)
                try:
                    y.addch(key)
                except:
                    pass
                y.refresh()
        except:
            pass
cursor.execute("select * from data")
detail = cursor.fetchall()
def save_and_edit_file():
    cursor.execute("select * from data")
    detail = cursor.fetchall()
    wrapper(create)
    try:
        global filepath
        print(filepath)
        print(detail)
        time.sleep(1)
        if detail != []:
            print("its not")
            if (filepath in detail[-1][-1]):
                print("already exist")
                print(detail)
        else:
            cursor.execute("INSERT INTO data (name, path) VALUES (%s, %s)", (os.path.basename(filepath.rsplit("/")[-1]), filepath))
            mydb.commit()
            print("succesfully inserted INNIT !!")
    except Exception as e:
        print(e)
    with open(filepath,"w") as f:
        f.write(text)
def edit_and_save():
    if os.path.exists(filepath):
        wrapper(edit)
        with open(filepath,"w")as f:
            f.write(text2)
    else:
        save_and_edit_file()
def delete_file():
    global filepath
    cursor.execute("select * from data")
    detail = cursor.fetchall()
    if os.path.exists(filepath):
        os.remove(filepath)
        print("first one was done")
        print(filepath,detail,sep="\n")
        if (filepath in detail[-1][-1]):
            cursor.execute("delete from data where path = %s",(filepath,))
            mydb.commit()
            print("File is successfully Deleted !!")
    else:
        print("File Doesn't Exist")
while True:
    choice = input("Enter 1. Create and write in file \n2.Edit existing file \n3.Delete file\n'e' for exit :")
    match choice:
        case '1':
            save_and_edit_file()
            print("\nFile Has Successfully Created and Saved !!")
        case '2':
            edit_and_save()
            print("File has been successfully edited !!")
        case '3':
            delete_file()
            
        case 'e':
            exit()
        case _:
            print("Invalid Input Please Try Again !!!")