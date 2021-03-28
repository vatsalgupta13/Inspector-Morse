from tkinter import *
import webbrowser

def callback():
    webbrowser.open_new(r"Exploratory Data Analysis.py")
def callback2():
    webbrowser.open_new(r"Clustering-Chicago.py")
def callback3():
    webbrowser.open_new(r"forapriori.py")
def callback4():
    webbrowser.open_new(r"FP-Growth.py")
def callback5():
    webbrowser.open_new(r"C:\Vatsal\Minor Project\QGIS - Chicago\Emerging Hotspots.qgs")
def callback6():
    webbrowser.open_new(r"C:\Vatsal\Minor Project\QGIS - Chicago\Chicago.qgs")
    
    
    

root = Tk()
w = Label(root, bg = 'green', fg='white', text='Minor Project of Vatsal, Ananya and Arjav') 
w.pack() 

w1 = Canvas(root, width=40, height=60) 
w1.pack() 
canvas_height=65
canvas_width=200
y = int(canvas_height / 2) 
w1.create_line(0, y, canvas_width, y )


ourMessage ='Welcome! \nKindly select the functionality that you want to view.'
messageVar = Message(text = ourMessage) 
messageVar.config(fg = 'white', bg = 'gray') 
messageVar.pack( )

w2 = Canvas(root, width=40, height=60) 
w2.pack() 
canvas_height=65
canvas_width=200
y = int(canvas_height / 2) 
w2.create_line(0, y, canvas_width, y )

link1 = Label(root, text="1. Exploratory Data Analysis", fg="blue", cursor="hand2")
link1.pack()
link1.bind("<Button-1>", lambda e: callback())

link2 = Label(root, text="2. Clustering", fg="blue", cursor="hand2")
link2.pack()
link2.bind("<Button-1>", lambda e: callback2())

link3 = Label(root, text="3. Apriori", fg="blue", cursor="hand2")
link3.pack()
link3.bind("<Button-1>", lambda e: callback3())

link4 = Label(root, text="4. FP Growth", fg="blue", cursor="hand2")
link4.pack()
link4.bind("<Button-1>", lambda e: callback4())

link5 = Label(root, text="5. Hotspot and Time Series Analysis - QGIS", fg="blue", cursor="hand2")
link5.pack()
link5.bind("<Button-1>", lambda e: callback5())

link6 = Label(root, text="6. Crime Count Analysis - QGIS", fg="blue", cursor="hand2")
link6.pack()
link6.bind("<Button-1>", lambda e: callback6())
 

root.mainloop()