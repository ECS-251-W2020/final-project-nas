# import tkinter module 
from tkinter import Tk
from tkinter import Entry
from tkinter import PhotoImage
from tkinter import Label
import sys
import sys
import os
import subprocess
#import tkMessageBox
  
# creating main tkinter window/toplevel 
master = Tk() 
  
# this will create a label widget 
l1 = Label(master, text = "IP address") 
l2 = Label(master, text = "Port Number") 
master.geometry('300x100')
  
# grid method to arrange labels in respective 
# rows and columns as specified 
#l1.grid(row = 0, column = 0, sticky = W, pady = 2)
l1.grid(row = 0, column = 0, pady = 2) 
#l2.grid(row = 1, column = 0, sticky = W, pady = 2) 
l2.grid(row = 1, column = 0, pady = 2) 

# entry widgets, used to take entry from user 
e1 = Entry(master) 
e2 = Entry(master) 
  
# this will arrange entry widgets 
e1.grid(row = 0, column = 1, pady = 2) 
e2.grid(row = 1, column = 1, pady = 2) 
  
# checkbutton widget 
#c1 = Checkbutton(master, text = "Preserve") 
#c1.grid(row = 2, column = 0, sticky = W, columnspan = 2) 
#c1.grid(row = 2, column = 0, columnspan = 2) 

  
# adding image (remember image should be PNG and not JPG) 
#img = PhotoImage(file = r"") 
#img1 = img.subsample(2, 2) 
  
# setting image with the help of label 
#Label(master, image = img1).grid(row = 0, column = 2, 
#       columnspan = 2, rowspan = 2, padx = 5, pady = 5) 

def onClick():
    print('Submitted!!')
    
def helloCallBack():
    file = 'p1.py'
    os.system("python3 p1.py")
    print("Hey")
    #subprocess.call(['python','p1.py'])
    
# button widget 
b1 = Button(master, text = "Submit",command= helloCallBack,bg = 'green') 
#Exit button
Exit_Button = Button(master, text = "Exit",command= master.quit,bg = 'red') 
Exit_Button.grid(row = 2, column=0)

#b2 = Button(master, text = "Zoom out") 
  
# arranging button widgets 
#b1.grid(row = 2, column = 2, sticky = E) 
b1.grid(row = 2, column = 2) 
#b2.grid(row = 2, column = 3, sticky = E)
#b2.grid(row = 2, column = 3)




#B=Button(master,text="hello",command= helloCallBack)
#B.pack()
#B.grid(row = 3, column = 4) 

  
# infinite loop which can be terminated  
# by keyboard or mouse interrupt 
master.mainloop() 