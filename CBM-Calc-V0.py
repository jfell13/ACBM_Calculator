import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

!export DISPLAY=0.0
!xhost +

root = Tk()

#canvas = Canvas(root, height=500, width=500, bg="#263D42")
#canvas.grid()

# Top Row Text and UCD Logo
toplabel = Label(root, text="Animal Cell-Based Meat Cost Calculator",fg="red").grid(row=0,column=0)

image1 = Image.open("The_University_of_California_Davis.svg.png")
image1 = image1.resize((125, 125), Image.ANTIALIAS)
photo1 = ImageTk.PhotoImage(image1)
UCDLogo = Label(image=photo1)
UCDLogo.image = photo1
UCDLogo.grid(row=0,column=4)

# First 8 variables over "two" rows (rows 1-2 and 3-4)
ACCL = Label(root, text="Achievable Cell Concentration\n(units of x10^6 cells/mL)").grid(row=1,column=0)
ACC = Scale(root, from_=1.0, to=100.0, resolution=0.1, orient=HORIZONTAL)
ACC.set("1.0")
ACC.grid(row=2,column=0)

BWVL = Label(root, text="Bioreactor Working Volume\n(units of m^3)").grid(row=1,column=1)
BWV = Scale(root, from_=1, to=100, orient=HORIZONTAL)
BWV.set("20")
BWV.grid(row=2,column=1)

FGF2L = Label(root, text="Growth Factor Concentrations\n(units of x10^-5 g/L)").grid(row=1,column=2)
FGF2 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
FGF2.set("10")
FGF2.grid(row=2,column=2)


FGF2CL = Label(root, text="Growth Factor Cost\n(units of x10^6 USD/g)").grid(row=1,column=3)
FGF2C = Scale(root, from_=0.00, to=10.00, resolution=0.01, orient=HORIZONTAL)
FGF2C.set("4.01")
FGF2C.grid(row=2,column=3)

GCBML = Label(root, text="Glucose Concentration in Basal Media\n(units of x10^-2 mol/L)").grid(row=3,column=0)
GCBM = Scale(root, from_=0.00, to=5.00, resolution=0.01, orient=HORIZONTAL)
GCBM.set("1.78")
GCBM.grid(row=4,column=0)

GCoRPCL = Label(root, text="Glucose consumption rate per cell\n(units of x10^-14 mol/hr*cell)").grid(row=3,column=1)
GCoRPC = Scale(root, from_=1.00, to=100.00, resolution=0.01, orient=HORIZONTAL)
GCoRPC.set("41.3")
GCoRPC.grid(row=4,column=1)

HPDL = Label(root, text="Hours per cell doubling\n(units of hr)").grid(row=3,column=2)
HPD = Scale(root, from_=1, to=24, orient=HORIZONTAL)
HPD.set("24")
HPD.grid(row=4,column=2)

MaTL = Label(root, text="Maturation time\n(units of hr)").grid(row=3,column=3)
MaT = Scale(root, from_=1, to=240, orient=HORIZONTAL)
MaT.set("240")
MaT.grid(row=4,column=3)

# Cost Functions

def math1():
    #1st function to number crunch
    #math1l = Label(root, text="")
    #math1l.destroy()
    cost1 = int(ACC.get())*int(BWV.get())*int(FGF2.get())*int(FGF2C.get())*int(GCBM.get())*int(GCoRPC.get())*int(HPD.get())*int(MaT.get())
    math1l = Label(root, text="Test cost for now = " + str(cost1))
    math1l.grid(row=6,column=2)    
def math1clear():
    math1l.grid_forget()
    #math1l.destroy()
#math1b = Button(root, text="Test fake cost\n(Proof)", command=lambda:[math1clear,math1]).grid(row=5,column=2)
math1b = Button(root, text="Test fake cost\n(Proof)", command=math1).grid(row=5,column=2)
    
# Reset Variables for each scenario

def setVar1():
    ACC.set("1.0")
    BWV.set("20")
    FGF2.set("10.00")
    FGF2C.set("4.01")
    GCBM.set("1.78")
    GCoRPC.set("41.3")
    HPD.set("24")
    MaT.set("240")
    #root.destroy()
    #root = Tk()
    
def setVar2():
    ACC.set("9.5")
    BWV.set("20")
    FGF2.set("5.00")
    FGF2C.set("2.01")
    GCBM.set("2.67")
    GCoRPC.set("20.7")
    HPD.set("16")
    MaT.set("156")
    
def setVar3():
    ACC.set("20.0")
    BWV.set("20")
    FGF2.set("0.00")
    FGF2C.set("0.00")
    GCBM.set("3.56")
    GCoRPC.set("4.13")
    HPD.set("8")
    MaT.set("72")

    
setVar1b = Button(root, text="Set for Scenario 1 Variables", command=setVar1).grid(row=5,column=4)
setVar2b = Button(root, text="Set for Scenario 2 Variables", command=setVar2).grid(row=6,column=4)
setVar3b = Button(root, text="Set for Scenario 3 Variables", command=setVar3).grid(row=7,column=4)
root.mainloop()
