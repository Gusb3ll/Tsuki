# Feb 2020 - Nathan Cueto
# Attempt to remove screentones from input images (png) using blurring and sharpening
# 
# import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages')
# import cv2
from cv2 import GaussianBlur, bilateralFilter, filter2D, imread, imwrite
import numpy as np
from tkinter import *
# from tkinter import ttk
# from matplotlib import pyplot as plt
from tkinter import filedialog
from os import listdir

from cmyui import log, Ansi

versionNumber = '1.6'

log('----- ToneRemover modified by Gusbell -----', Ansi.CYAN)
log('Press go on the UI to start', Ansi.WHITE)

# Gaussian blue with variable kernel size, aka more or less blurring
def blur(img, blur_amount=5):
    # TODO experiment with upscaling
    # TODO customizable variables for sigmas
    if(blur_amount == 7):
        dst2 = GaussianBlur(img,(7,7),0)
        dst = bilateralFilter(dst2, 7, 80, 80)
    else:
        dst2 = GaussianBlur(img,(5,5),0)
        dst = bilateralFilter(dst2, 7, 10 * blur_amount, 80)
    # plt.subplot(131)
    # plt.imshow(dst2)
    # plt.title('gauss')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(132)
    # plt.imshow(dst)
    # plt.title('abf')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(133)
    # plt.imshow(dst3)
    # plt.title('blur')
    # plt.xticks([]), plt.yticks([])
    # plt.show()
    return dst

# Laplacian filter for sharpening. Only want to do runs of 3x3 kernels to avoid oversharpening.
def sharp(img, sharp_point, sharp_low):
    # TODO customizable sliders for kernel parameters
    # TODO try darkening image
    s_kernel = np.array([[0, sharp_low, 0], [sharp_low, sharp_point, sharp_low], [0, sharp_low, 0]])

    sharpened = filter2D(img, -1, s_kernel)
    # plt.subplot(121)
    # plt.imshow(img2)
    # plt.title('Original')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(122)
    # plt.imshow(sharpened)
    # plt.title('sharp')
    # plt.xticks([]), plt.yticks([])
    # plt.show()
    return sharpened

# 1 - no png files found
# 2 - no input dir
# 3 - no output dir
# 4 - write error
def error(errcode):
    # popup success message
    popup = Tk()
    popup.title('Error')
    switcher = {
        1: "Error: No .png files found",
        2: "Error: No input directory",
        3: "Error: No output directory", 
        4: "Error: File write error"
    }

    label = Label(popup, text=switcher.get(errcode, "what"))
    label.pack(side=TOP, fill=X, pady=20)

    okbutton = Button(popup, text='Ok', command=popup.destroy)
    okbutton.pack()
    popup.mainloop()
    # popup error code

# function scans directory and returns genorator
def getfileList(dir):
    return (i for i in listdir(dir) if i.endswith('.png') or i.endswith('.PNG') or i.endswith('.jpg') or i.endswith('.JPG') or i.endswith('.jpeg'))

# function will call the blur and sharpen on every file in directory, and write output file
def removeScreentones(dir_i, dir_o, blur_amount, sh_point=5.56, sh_low=-1.14):
    if(dir_i == [] or len(dir_i)==0):
        return error(2)
    if(dir_o == [] or len(dir_o)==0):
        return error(3)
    inputs = list(getfileList(dir_i))
    if(len(inputs) == 0):
        return error(1)

    # calculate sh params, warning if they are unproportionate
    sh_point = float(sh_point)
    sh_low = float(sh_low)
    # print(sh_point, sh_low)
    sharps = (4 * sh_low) + sh_point - 1 # weight is initially just 1
    if(sharps > 0):
        popupw = Tk() # popup warning
        popupw.title('Warning')
        label = Label(popupw, text='Sharpening parameters result is high. Output will brighten')
        label.pack(side=TOP, fill=X, pady=20)
        okbutton = Button(popupw, text='Ok', command=popupw.destroy)
        okbutton.pack()
        popupw.mainloop()
    elif(sharps < 0):
        popupw = Tk() # popup warning
        popupw.title('Warning')
        label = Label(popupw, text='Sharpening parameters result is low. Output will darken')
        label.pack(side=TOP, fill=X, pady=20)
        okbutton = Button(popupw, text='Ok', command=popupw.destroy)
        okbutton.pack()
        popupw.mainloop()

    bs_amount = 0
    if(blur_amount==1):
        bs_amount=3
    if(blur_amount==2):
        bs_amount=5
    if(blur_amount==3):
        bs_amount=7

    loader = Tk()
    loader.title('Processing')
    load_label = Label(loader, text='Removing Screentones. Please wait')
    load_label.pack(fill=X, pady=10, padx=20)
    loader.update()
    for i in inputs:
        # print(dir_i+'/'+i)
        img = imread(dir_i + '/' + i)
        blurred = blur(img, bs_amount)
        ret = sharp(blurred, sh_point, sh_low)
        sucess = imwrite(dir_o + '/' + i, ret)
        if(sucess != True):
            return error(4)
    log('----- ToneRemover has done running, you may close the UI and continue -----', Ansi.GREEN)

    loader.destroy()
    # popup success message
    popup = Tk()
    popup.title('Success!')
    label = Label(popup, text='Process executed successfully!')
    label.pack(side=TOP, fill=X, pady=20)
    okbutton = Button(popup, text='Ok', command=popup.destroy)
    okbutton.pack()
    popup.mainloop()

# globals that hold directory strings
dtext = ""
otext = ""

# both functions used to get and set directories
def dnewdir():
    dtext = filedialog.askdirectory(title='Choose directory for input images (.png recommended)')
    dvar.set(dtext)

def onewdir():
    otext = filedialog.askdirectory(title='Choose directory for output images (.png recommended)')
    ovar.set(otext)

if __name__ == "__main__":
    # img = cv2.imread('16.png')
    # bs_amount = 5

    # blur_img = blur(img, bs_amount)
    # sharp_img = sharp(blur_img, img, bs_amount)
    # success = cv2.imwrite('output2.png', sharp_img)

    # GUI codes
    root = Tk()
    root.title("Screentone Remover v." + versionNumber)


    tFrame = Frame(root)
    bFrame = Frame(root)

    dvar = StringVar(root)
    ovar = StringVar(root)

    # directory label, entry, and button
    d_label = Label(tFrame, text = 'Input file directory: ')
    d_label.grid(row=1, sticky=E, padx=20, pady=20)
    d_entry = Entry(tFrame, textvariable = dvar)
    d_entry.insert(0, "./input")
    d_entry.grid(row=1, column=1)
    dir_button = Button(tFrame, text="Browse", command=dnewdir)
    dir_button.grid(row=1, column=2)
    
    # output directory label, entry, and button
    o_label = Label(tFrame, text = 'Output file directory: ')
    o_label.grid(row=2,sticky=E)
    o_entry = Entry(tFrame, textvariable=ovar)
    o_entry.insert(0, "./output")
    o_entry.grid(row=2, column=1)
    out_button = Button(tFrame, text="Browse", command=onewdir)
    out_button.grid(row=2, column=2)

    # blur sliders
    slideLabel = Label(bFrame, text = 'Blur amount: (Default is 2)')
    slideLabel.grid(row=0, padx=20)
    filtslide = Scale(bFrame, from_=1, to=3, orient=HORIZONTAL)
    filtslide.grid(row=1, columnspan=2)
    filtslide.set(2)

    # sharpening sliders
    helpLabel = Label(bFrame, text = 'Sharpening: | point strength + (4 * low strength) | should be ~= 0')
    helpLabel.grid(row=5, padx=10)
    sharpLabel = Label(bFrame, text = 'Sharpening point strength: (Default is +5.56)')
    sharpLabel.grid(row=2, padx=20)
    sharpSlide = Entry(bFrame)
    sharpSlide.grid(row=3)
    sharpSlide.insert(0, '5.56')
    shLabel = Label(bFrame, text = 'Sharpening low strength:  (Default is -1.14)')
    shLabel.grid(row=4, padx=20)
    helpLabel = Label(bFrame, text = 'NOTE: Must be negative, absolute val should be == (1/4) * point strength')
    helpLabel.grid(row=5, padx=10)
    shEntry = Entry(bFrame)
    shEntry.grid(row=6, padx=20)
    shEntry.insert(0, '-1.14')

    go_button = Button(bFrame, text="Go!", command = lambda: removeScreentones(d_entry.get(), o_entry.get(), filtslide.get(), sharpSlide.get(), shEntry.get()))
    go_button.grid( columnspan=2)
    root.geometry("400x420")
    tFrame.pack(fill="both", expand=True)
    bFrame.pack(fill="both", expand=True)

    # go_button.pack(side=RIGHT)
    root.mainloop()
    

    pass
