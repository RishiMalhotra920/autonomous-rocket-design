from tkinter import *
from tkinter import messagebox
import math,numpy, pandas
import subprocess
window = Tk()
window.title("Rocket User Interface")
window.geometry('600x400')


lbl = Label(window, text="Throat Radius:",font=("fixedsys", 20))
lbl.place(x=0,y=0)

txt = Entry(window,width=20)
txt.place(x = 230, y =10)

labl = Label(window, text="Your Throat Radius value will be shown here")
labl.place(x=0,y = 30)

def clicked():
    res = "The throat radius value is: " + txt.get()
    labl.configure(text= res)

Ent = Button(window, text = "Enter", bg = "blue", fg = "white",command = clicked)
Ent.place(x = 360,y = 5)


lbl = Label(window, text="Expansion ratio:",font=("fixedsys", 20))
lbl.place(x = 0, y = 100)

txt1 = Entry(window,width=20)
txt1.place(x = 270, y =110)

labl1 = Label(window, text="Your Expansion ratio value will be shown here")
labl1.place(x=0,y = 130)

def clicked1():
    res = "The Expansion Ratio value is: " + txt1.get()
    labl1.configure(text= res)

Ent1 = Button(window, text = "Enter", bg = "green", fg = "white",command = clicked1)
Ent1.place(x = 400,y = 105)



# Add a button for Submitting
def clicksub():
    sub = messagebox.askyesno('Submit','Would you like to submit these choices? You must hit enter for all 2 fields!')
    if sub == True:

        filename = '/Users/rishimalhotra/Applications/Autodesk Fusion 360.app'
        subprocess.run(['open', filename], check=True)

        window.quit()

Subm = Button(window, text = "Submit", bg = "red", fg = "white",height = 4, width = 13, command = clicksub)
Subm.place(x = 150, y = 300)


window.mainloop()

throatradius = float(txt.get())
Expansionratio = float(txt1.get())
print('The fields are',throatradius,Expansionratio)

#Function for x,y coordinates

def top(Rt,epsilon):

    theta_n = 43.55995 + (-326151.1 - 43.55995)/(1 + math.pow(epsilon/(1.025758*math.pow(10,-17)),0.2362785))
    theta_e = 5.778663 + (17428660 - 5.778663)/(1 + math.pow(epsilon/(1.217947*math.pow(10,-8)),0.7519347))

    theta_n = round(theta_n,1)
    theta_e = round(theta_e,1)
    delta_theta = 1
    delta_t = 0.1
    theta=numpy.arange(-135,theta_n-90 +delta_theta,delta_theta)
    thetar=numpy.copy(theta)
    for i in range(len(thetar)):
        thetar[i]=math.radians(thetar[i])

    t=numpy.arange(0,1+delta_t,delta_t)

    entrant=int(45/delta_theta)
    x=[]
    y=[]

    for i in range(entrant):
        x.append(1.5*Rt*math.cos(thetar[i]))
        y.append(1.5*Rt*math.sin(thetar[i])+1.5*Rt+Rt)
    exit=theta.size
    #throat exit
    for i in range(entrant,exit,1):
        x.append(0.382*Rt*math.cos(thetar[i]))
        y.append(0.382*Rt*math.sin(thetar[i])+0.382*Rt+Rt)
    #solves for the control points of the Bezier Curve
    Nx=0.382*Rt*math.cos(math.radians(theta_n-90))
    Ny=0.382*Rt*math.sin(math.radians(theta_n-90))+0.382*Rt+Rt
    Ex=(0.85*(math.pow(epsilon,0.5)-1)*Rt)/math.tan(math.radians(15))
    Ey=math.pow(epsilon,0.5)*Rt
    m1=math.tan(math.radians(theta_n))
    m2=math.tan(math.radians(theta_e))
    c1=Ny-m1*Nx
    c2=Ey-m2*Ex
    Qx=(c2-c1)/(m1-m2)
    Qy=(m1*c2-m2*c1)/(m1-m2)

    for i in range(t.size):
        wk=int((theta_n-90+135)/delta_theta)
        #x[i+1+wk]
        #print ("i+1+wk")
        #print(i+1+wk)

        x.append(math.pow((1-t[i]),2)*Nx+2*(1-t[i])*t[i]*Qx+math.pow(t[i],2)*Ex)
        y.append(math.pow((1-t[i]),2)*Ny+2*(1-t[i])*t[i]*Qy+math.pow(t[i],2)*Ey)

    zippedList =  list(zip(x, y,[0]*len(x)))
    df=pandas.DataFrame(zippedList)
    df.to_csv(r'/Users/rishimalhotra/Downloads/TOC_Coordinates.csv', header=False, index=False)
top(throatradius,Expansionratio)
