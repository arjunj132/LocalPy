# Welcome!
# This is LocalPy
# a easy-to-use localhost creator
# and manager
# based purely on Python!
# Thanks for using LocalPy!

# Dependencies:
import os
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk
import http.server
import threading
import json
import easygui
from pathlib import Path
import shutil



mycwd = os.getcwd()


# Beginning screen
root = Tk()
root.title('LocalPy Dashboard')
logo = Label(root, text="LocalPy")
logoFont = Font(family="Helvetica", size=40)
logo.configure(font=logoFont, fg='green')
logo.pack()

def quit():
    root.destroy()


root.after(2000, quit)
root.mainloop()

# server code
def server_start(port):
    exec("""
class StoppableHTTPServer(http.server.HTTPServer):
    def run(self):
        os.chdir('ports')
        os.chdir('""" + str(port) + """')
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.server_close()
    """, globals())
    exec('global s' + str(port))
    exec("""s""" + str(port) + """ = StoppableHTTPServer(("127.0.0.1",""" + str(port) + """),
                             http.server.SimpleHTTPRequestHandler)""", globals())

    # Start processing requests
    exec('global t' + str(port))
    exec('t' +  str(port) + ' = threading.Thread(None, ' + 's' + str(port) + '.run)', globals())
    exec('t' + str(port) + '.start()')

def server_quit(port):
    exec('s' + str(port) + '.shutdown()')
    exec('t' + str(port) + '.join()')
    messagebox.showinfo(title='LocalPy', message='You have deleted your LocalPy server localhost:' + str(port))


# Open manager
root = Tk()
root.title('LocalPy')
root.geometry('400x400')

Label(root, text='LocalPy Dashboard').pack()

frame = Frame(root)
scroll = Scrollbar(frame, orient=VERTICAL)
sessions = Listbox(frame, yscrollcommand=scroll.set)
scroll.config(command=sessions.yview)
scroll.pack(side=RIGHT, fill=Y)
frame.pack()
sessions.pack(pady=15)

with open('data/servers.json') as f:
    f = json.loads(f.read())['data']
    for x in f:
        sessions.insert(END, x)
        server_start(x.split(':')[1])

end_index = sessions.index("end")
if end_index == 0:
    print("It looks like you don't have any localhosts. Lets start one!")


def add():
    os.chdir(mycwd)
    port_num = easygui.enterbox("Enter the port number of your server")
    Path("ports/" + port_num).mkdir(parents=True, exist_ok=True)
    server_start(port_num)
    sessions.insert(END, 'localhost:' + port_num)
    os.chdir(mycwd)
    with open('data/servers.json', 'r+') as f:
        y = json.loads(f.read())
        y['data'].append(sessions.get(ACTIVE))
        f.seek(0)
        f.write(json.dumps(y))
        f.truncate()



def delete():
    os.chdir(mycwd)
    os.chdir('ports')
    shutil.rmtree(sessions.get(ACTIVE).split(':')[1])
    server_quit(sessions.get(ACTIVE).split(':')[1])
    os.chdir(mycwd)
    with open('data/servers.json', 'r+') as f:
        y = json.loads(f.read())
        y['data'].remove(sessions.get(ACTIVE))
        f.seek(0)
        f.write(json.dumps(y))
        f.truncate()
    sessions.delete(ANCHOR)



delete_host = Button(root, text="Delete server", command=delete)
delete_host.pack()
start_host = Button(root, text="Add sever", command=add)
start_host.pack()
root.mainloop()


# This is the end of our code.
# (c) Arjun J