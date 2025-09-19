from tkinter import Text, Tk, Button, Entry, END, Scrollbar, TOP, LEFT, RIGHT, BOTH

from tkinter import ttk
import subprocess
import json
import customtkinter
ctk = customtkinter.CTk()
import signal
import sys
import os
import threading
AI_response = ["No previous response"]
input = ["No previous input"]
ctk.geometry("600x500")
ctk.title("lingsa Chat Girl")

# Allow Ctrl+C to close the window gracefully
def _signal_handler(sig, frame):
    ctk.destroy()
    sys.exit(0)

signal.signal(signal.SIGINT, _signal_handler)
currentfolder = os.path.dirname(os.path.abspath(__file__))
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Black = '\033[90m'
    RED = '\033[91m'
    
    
def Send_Message():
    
    
    text_widget.tag_config("red", foreground="red")
    text_widget.tag_config("white", foreground="white")
    
    
    entry = inputer.get()
    if(entry == ""):
        return
    input.append(entry)
    inputer.delete(0,"end")
    
    print(bcolors.Black + "User : "+ bcolors.ENDC ,entry)

    text_widget.insert("end",f'You : ',"red")
    text_widget.insert("end",f'{entry}\n',"white")
    text_widget.see("end")

    data = json.dumps({
        "input_previous": input[-2],
        "input": input[-1],
        "AI_response": AI_response[-1] 
    })
    

    def run_php_and_update():
            run_php = subprocess.Popen(
                ["php", currentfolder + "/mistral.php"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = run_php.communicate(input=data)
            AI_response.append(stdout)
            print(stderr)
            print(bcolors.RED + "Lingsa : " + bcolors.ENDC,stdout)
            text_widget.after(0, lambda: (
                text_widget.insert("end",f'lingsa : ',"red"),
                text_widget.insert("end",f'{stdout}\n',"white"),
                text_widget.see("end")
            ))

    threading.Thread(target=run_php_and_update, daemon=True).start()

text_widget =  customtkinter.CTkTextbox(ctk,wrap="word",height=20,width=70)
text_widget.pack(side="top",expand=True,fill="both" ,pady=10,padx=10)

scrol_command = customtkinter.CTkScrollbar(ctk,command=text_widget.yview)
scrol_command.pack(side="right",fill="both")

text_widget.configure(yscrollcommand=scrol_command.set)

inputer = customtkinter.CTkEntry(ctk)
inputer.pack(side="left",expand=True,fill="both" ,pady=100,padx=10)

inputer.bind("<Return>", lambda event: Send_Message())

customtkinter.CTkButton(ctk,text="send",command=Send_Message).pack(side="right",pady=10,padx=10)



ctk.mainloop()