from __future__ import print_function
from tkinter import *
import os, os.path, sys
from collections import OrderedDict
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pickle
from helpers.ColorGuesser import ColorGuesser

data_file = 'helpers/scan_regions.dat'
snap_loc = 'temp/test_snap.jpg'
marked_snap_loc = 'temp/test_snap_marked.jpg'
regions = {}
entries = []
guessed_labels = []
color_guesser = ColorGuesser()

fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
fnt2 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)

def get_cc(region):
    return color_guesser.get_contrasted_color(color_guesser.guess(region))

def update_cam():
    
    camera.capture(snap_loc)
    im = Image.open(snap_loc)
    draw = ImageDraw.Draw(im)
    
    #draw grid
    x = 100
    while x<1920:
        draw.line([(x, 0), (x, 1079)], fill=(255, 255, 255, 128))
        draw.text((x, 0), str(x), font=fnt2, fill=(255, 255, 255, 128))
        x+=100
    
    y = 100
    while y<1080:
        draw.line([(0, y), (1919, y)], fill=(255, 255, 255, 128))
        draw.text((0,y), str(y), font=fnt2, fill=(255, 255, 255, 128))
        y+=100
    
    for regi in range(1, 7):
        reg = regions[regi]
        regim = im.crop(reg)
        
        #enhance        
        regim_marked = regim.point(lambda i: i*2)
        im.paste(regim_marked, reg)   
        
        gc = color_guesser.guess(regim)
        cc = color_guesser.get_contrasted_color(gc)        
        draw.text((reg[0]+5, reg[1]+5), str(regi), font=fnt, fill=cc)
        draw.rectangle(reg, outline=cc)
        
        guessed_labels[regi-1].config(text=gc)
            
    im.save(marked_snap_loc)
    #del im
     
    im = Image.open(marked_snap_loc)
    im = im.resize((800, 450), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    cam_panel.config(image = img)
    cam_panel.image = img
    root.after(1000, update_cam)


def update_regions():
    
    for i in range(6):
        error = False
        
        x = entries[i][0].get()
        y = entries[i][1].get()
        w = entries[i][2].get()
        h = entries[i][3].get()
        
        if x<0 or y<0 or w<=0 or h <=0:
            error = True
        if (x + w) >= 1920 or (y + h) >=1080:
            error = True
        
        if not error:
            regions[i+1] = [x, y, x+w, y+h]
            
def save_regions():
    outfile = open(data_file,'wb')
    pickle.dump(regions,outfile)
    print("Region data saved")
    outfile.close()

if not os.path.exists(data_file):
    points = [(950, 120), (950, 420), (950, 750), (1170, 120), (1170, 420), (1170, 750)]
    size_x = 50
    size_y = 50
    
    for i in range(6):
        regions[i+1] = [points[i][0], points[i][1], points[i][0] + size_x, points[i][1] + size_y]
else:
    infile = open(data_file,'rb')
    regions = pickle.load(infile)
    infile.close()
    
print(regions)

root = Tk()
root.resizable(width=False, height=False)
root.geometry("1100x450+50+100")
root.title("Camera Positioner")

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 15

cam_panel = Label(root, background='red', width=800, height=450)
cam_panel.pack(side = "left")

button_panel = Frame(root)
button_panel.pack(side = "left", fill=BOTH, expand = True, padx=10)

header = Label(button_panel, text="Scan regions:", font=("Arial", 14, "bold"))
header.grid(row=0, column=0, columnspan = 4, sticky=W, pady=10)

xl = Label(button_panel, text="X").grid(row=1, column=1, sticky = W)
yl = Label(button_panel, text="Y").grid(row=1, column=2, sticky = W)
wl = Label(button_panel, text="W").grid(row=1, column=3, sticky = W)
hl = Label(button_panel, text="H").grid(row=1, column=4, sticky = W)

for r in range(6):
    header_reg = Label(button_panel, text="Region %d:  " % (r+1), font=("Arial", 10, "bold")).grid(row=2+r, column=0, ipady=3, sticky = W)

    x0 = regions[r+1][0]
    y0 = regions[r+1][1]
    x1 = regions[r+1][2]
    y1 = regions[r+1][3]

    exv = IntVar()
    exv.set(x0)
    ex = Entry(button_panel, width=4, textvariable = exv)
    ex.grid(row=2+r, column=1)
    
    eyv = IntVar()
    eyv.set(y0)
    ey = Entry(button_panel, width=4, textvariable = eyv)
    ey.grid(row=2+r, column=2)
    
    ewv = IntVar()
    ewv.set(x1-x0)
    ew = Entry(button_panel, width=4, textvariable = ewv)
    ew.grid(row=2+r, column=3)
    
    ehv = IntVar()
    ehv.set(y1-y0)
    eh = Entry(button_panel, width=4, textvariable = ehv)
    eh.grid(row=2+r, column=4)
    
    entries.append([exv, eyv, ewv, ehv])
    
    gl = Label(button_panel, text=" ")
    gl.grid(row=2+r, column=5, sticky = W)
    guessed_labels.append(gl)

btn_update = Button(button_panel, text="Update", command=update_regions).grid(row=8, column=1, columnspan=2)
btn_save   = Button(button_panel, text="Save", command=save_regions).grid(row=8, column=3, columnspan = 2)

     

root.after(10, update_cam)
root.mainloop()

