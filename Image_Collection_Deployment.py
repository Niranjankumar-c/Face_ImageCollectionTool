
def browse_button():
    global filename
    filename = filedialog.askdirectory()
    


def ensure_dir(file_path,person_name):
    filepath=file_path+"/"+person_name+"/"
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
# function for choosing camera

def sel():
    
    global cam_value
    cam_value =   int(cam_var.get())
   
    if cam_value==2:
        entry2.configure({"background": "snow"})
        entry2['state']='normal'
        
    if cam_value==1:
        entry2.configure({"background": "gray74"})
        entry2['state']='disabled'
        
    

def changeImage():
   
    global tkpi #need global so that the image does not get derefrenced out of function

    #gets list of file names in certain directory. In this case, the directory it is in
    dirlist = os.listdir('emojis')

    #get random image
    randInt = random.randint(1,6)
    image = Image.open("emojis\\"+dirlist[randInt])
    image = image.resize((100, 100), Image.ANTIALIAS)

    #Creates a Tkinter compatible photo image
    tkpi = ImageTk.PhotoImage(image)

    #Put image in a label and place it
    label_image = tk.Label(topframe, image=tkpi,bg='gray1')
    label_image.grid(row=0,column=0)#width=image.size[0],height=image.size[1])

    # call this function again in 3 seconds
    topframe.after(1800, changeImage)


# this function is used to retrieve the value from text box; diabling and enabling the record button basing on the input

def myfunction():  
    global name,dur,ipadd
    ipadd=entry2.get()   
    
    if filename=='':
        dummy='PLEASE CHOOSE DIRECTORY !! '
        messagelbl.config(text=dummy,fg='red')
        return ''
    if cam_value==0: 
        dummy=' PLEASE CHOOSE CAMERA !!'
        messagelbl.config(text=dummy,fg='red')
        return ''
    name=entry.get()
    if len(name)<=0:
        dummy=' PLEASE ENTER NAME !!'
        messagelbl.config(text=dummy,fg='red')
        return ''    
    
    if len(name)>0:
        greenBtn.config(state='normal')
    else:
        greenBtn.config(state='disabled')

    dur=tkvar1.get()
    ensure_dir(filename,name) 
    dummy='Message box'
    messagelbl.config(text=dummy,fg='gray74')
    
def show_vid():
    # global variables declaration
    global topframe,lmain,sampleNum,flag,frame,start_time
   
    # clearing the UI inputs
    entry.delete(0, END)
    entry.update()   
    greenBtn.config(state='disabled')
  
    if not cap.isOpened():                             #checks for the opening of camera
        print("cant open the camera")
   
    if start_time ==0:
        start_time=time.time()
    flag, frame = cap.read()
    
    # Images capturing for time duration
    
    faces = detector.detectMultiScale(frame, 1.3, 5)
    
    for (a,b,c,d) in faces:
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite(filename+"/"+name+"/"+name+'.'+ str(sampleNum) + ".jpg", frame[b:b+d+20,a:a+c+20]) #
        
    
    # real time video show for the users
    frame = cv2.flip(frame, 1)
    if flag is None:
        print("Major error!")
    elif flag:
        global last_frame
        last_frame = frame.copy()

    pic = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)     #we can change the display color of the frame gray,black&white here
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img,)
    lmain = tk.Label(master=root,width=int(ws/2),height=int(hs/2))
    lmain.grid(row=2, column=0, padx=20, pady=10,rowspan=1,columnspan=2)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    
    # time duration implemenation
    end_time=time.time()
    elapsed=end_time-start_time
    
    if elapsed<int(dur)*10:
        lmain.after(10, show_vid) 
    elif elapsed>int(dur)*10:
        cap.release()
        start_time=0
        lmain.grid_forget()
        lmain.pack_forget()
        lmain.destroy()
        lmain = tk.Label(master=root,width=int(ws/14),height=int(hs/30),bg='gray1',highlightthickness=2, highlightbackground="#111")
        lmain.grid(row=2, column=0, padx=20, pady=10,rowspan=3,columnspan=2)#,sticky=E+W+N+S)
    
        topframe.destroy()
        topframe = Frame(root, width=100, height = 100, bg="gray1", highlightthickness=2, highlightbackground="#111")
        topframe.grid(row=0, column=0,padx=20, pady=5, sticky=N+E)
        tk.Label(messageframe, text="            IMAGE COLLECTION SUCCESSFULL !!!  ",
                 font=('Times', '14','bold'),bg='Gray1',fg="green",justify=LEFT).grid(row = 0, column = 0)#,bg="RosyBrown1



def camera_open():
    global cap   
    
    if(cam_value==2):
        cap = cv2.VideoCapture("https://"+str(ipadd)+"/video")
        
    else:
        cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(ws/2));
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(hs/2));
    changeImage()
    show_vid()


# In[3]:


from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import cv2
import os, random
import numpy as np
from multiprocessing import Process, Queue
import time
from tkinter import filedialog

root = Tk() 

w = 1170 # width for the Tk root
h = 780 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/20) - (h/20)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))


task = Queue()
root.geometry()
root.resizable(0,0)
root.wm_title("Image Collection") #Makes the title that will appear in the top left
root.config(bg = "gray1")

# frame for heading
image_start = tk.PhotoImage(file='Images/start.png')

global topframe,filename,cam_value,ipadd,name,dur,last_frame,cap, flag,frame,detector,sampleNum,start_time,lmain
sampleNum=0 
start_time=0
detector= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
last_frame = np.zeros((1600, 900, 3), dtype=np.uint8)
namename=''
filnamee=''
cam_value=0
ipadd=0

Mainframe=Frame(root,width=900,height=60 ,bg="gray1", highlightthickness=2, highlightbackground="snow")
Mainframe.grid(row=0, column=0,padx=20, pady=5,columnspan=3)

topframe = Frame(root, width=100, height = 100, bg="gray1")#, highlightthickness=2, highlightbackground="#111")
topframe.grid(row=1, column=0,padx=20, pady=5, sticky=N+E)

bottomFrame = Frame(root, width=100, height = 100, bg="gray1")#, highlightthickness=2, highlightbackground="#111")
bottomFrame.grid(row=5, column=0,padx=5, pady=5, sticky=N+E)

rightframe= Frame(root, width=200, height = 500, bg="gray1", highlightthickness=2, highlightbackground="snow")
rightframe.grid(row=2, column=2,padx=5, pady=5, sticky=N+E,rowspan=3,columnspan=1)

messageframe= Frame(root, width=100, height = 85, bg="snow", highlightthickness=2, highlightbackground="#111")
messageframe.grid(row=6, column=0,padx=1, pady=0,columnspan=2)


btnFrame = Frame(bottomFrame, width=150, height = 80, bg="gray1")
btnFrame.grid(row=0, column=2, padx=0, pady=0)


lmain = tk.Label(master=root,width=int(ws/14),height=int(hs/30),bg='gray1',highlightthickness=2, highlightbackground="#111")
lmain.grid(row=2, column=0, padx=20, pady=5,rowspan=3,columnspan=2)#,sticky=E+W+N+S)

#show_vid()

# label diplaying 'Heading'
tk.Label(Mainframe, text="Facial Image Collection Tool",font=('Times', '18','bold'),bg='Gray1',
         fg="snow",justify=LEFT).grid(row = 0, column = 0,padx=10,pady=5)#,bg="RosyBrown1

# label diplaying 'NAME'
tk.Label(rightframe, text="NAME                 ",font=('Times', '14','bold'),bg='Gray1',fg="RosyBrown1",
         justify=LEFT).grid(row = 0, column = 1,padx=10,pady=8)#,bg="RosyBrown1

# text box for name
entry = tk.Entry(rightframe, justify=LEFT,)
entry.grid(row=0 ,column=2,padx=10,pady=8)
entry.config(width=22)


# Create a Tkinter variable
tkvar1 = StringVar(root)
  
# Dictionary with options 
choices = { 1,2,3,4,5}
tkvar1.set(1) # set the default option

#label displaying DURATION
pop_duration = OptionMenu(rightframe, tkvar1, *choices)
Label(rightframe, text="DURATION         ",bg="gray1",font=('Times', '14','bold'),fg="RosyBrown1",
      justify=LEFT).grid(row = 2, column = 1,padx=10,pady=8,sticky=W+N)#,bg="RosyBrown1"
pop_duration.grid(row = 2, column =2)
pop_duration.config(width=5)

# for directory
# label diplaying 'Directory'
tk.Label(rightframe, text="DIRECTORY      ",font=('Times', '14','bold'),bg='Gray1',fg="RosyBrown1",
         justify=LEFT).grid(row = 3, column = 1,padx=10,pady=8)#,bg="RosyBrown1


dirBtn = tk.Button(rightframe, text='  Choose Directory   ', bd=0,command=lambda:browse_button(),
                   font=('Times', '11'),fg="black")
dirBtn.grid(row=3, column=2, padx=10,pady=8)


# radio button for camera
# label diplaying 'Camera'
tk.Label(rightframe, text="CAMERA            ",font=('Times', '14','bold'),bg='Gray1',fg="RosyBrown1",
         justify=LEFT).grid(row = 6, column = 1,padx=10,pady=8)#,bg="RosyBrown1

cam_var = IntVar()
R1 = Radiobutton(rightframe, text="  Web Camera    ", variable=cam_var, value=1,font=('Times', '11'),
                  command=sel)
R2 = Radiobutton(rightframe, text=" Phone Camera  ", variable=cam_var, value=2,font=('Times', '11'),
                  command=sel)
R1.grid(row=6,column=2,pady=8)
R2.grid(row=8,column=2,pady=8)

# label diplaying 'ipaddress'
tk.Label(rightframe, text="IP Address     ",font=('Times', '12','bold'),bg='Gray1',fg="snow",
         justify=LEFT).grid(row = 9, column = 2,padx=10,pady=8)#,bg="RosyBrown1


# input for ip address
entry2 = tk.Entry(rightframe, justify=LEFT,state=DISABLED,)
entry2.configure(disabledbackground='gray74',background='snow')
entry2.grid(row=10, column=2,padx=10,pady=8)

# ENTER button
Btn = tk.Button(rightframe, text='ENTER', bd=0,command=lambda:myfunction(),font=('Times', '12','bold'),fg="snow",bg='green')
Btn.grid(row=11, column=1, padx=10,pady=8,columnspan=2)


# record button
greenBtn = tk.Button(btnFrame, image=image_start, bd=0,bg="gray1",state=DISABLED,command=lambda:camera_open())
greenBtn.grid(row=0, column=1, padx=10,pady=15)

#message label
messagelbl=Label(messageframe, text="Message box",bg="gray86",font=('Times', '12','bold'),width=85,height=2,anchor='w',
      justify=LEFT,fg="gray75")
messagelbl.grid(row = 0, column = 0,columnspan=3)


root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly

#cap.release()

