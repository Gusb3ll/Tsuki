"""
Feb 2020 - Nathan Cueto
Attempt to remove screentones from input images (png) using blurring and sharpening
"""

import numpy as np
from os import listdir
from cv2 import GaussianBlur, bilateralFilter, filter2D, imread, imwrite

from cmyui import log, Ansi

log('----- ToneRemover modified by Gusbell -----', Ansi.CYAN)

def blur(img, blur_amount=5):
    if(blur_amount == 7):
        dst2 = GaussianBlur(img,(7,7),0)
        dst = bilateralFilter(dst2, 7, 80, 80)
    else:
        dst2 = GaussianBlur(img,(5,5),0)
        dst = bilateralFilter(dst2, 7, 10 * blur_amount, 80)
    return dst

def sharp(img, sharp_point, sharp_low):
    s_kernel = np.array([[0, sharp_low, 0], [sharp_low, sharp_point, sharp_low], [0, sharp_low, 0]])
    sharpened = filter2D(img, -1, s_kernel)
    return sharpened

def getfileList(dir):
    return (i for i in listdir(dir) if i.endswith('.png') or i.endswith('.PNG') or i.endswith('.jpg') or i.endswith('.JPG') or i.endswith('.jpeg'))

def removeScreentones(dir_i, dir_o, blur_amount, sh_point=5.56, sh_low=-1.14):
    if(dir_i == [] or len(dir_i)==0):
        log('No input directory', Ansi.RED)
    if(dir_o == [] or len(dir_o)==0):
        log('No output directory', Ansi.RED)
    inputs = list(getfileList(dir_i))
    if(len(inputs) == 0):
        log('No png file founded', Ansi.RED)

    log('Removing tone', Ansi.CYAN)

    sh_point = float(sh_point)
    sh_low = float(sh_low)
    sharps = (4 * sh_low) + sh_point - 1
    # if(sharps > 0):
    #     popupw = Tk()
    #     popupw.title('Warning')
    #     label = Label(popupw, text='Sharpening parameters result is high. Output will brighten')
    #     label.pack(side=TOP, fill=X, pady=20)
    #     okbutton = Button(popupw, text='Ok', command=popupw.destroy)
    #     okbutton.pack()
    #     popupw.mainloop()
    # elif(sharps < 0):
    #     popupw = Tk()
    #     popupw.title('Warning')
    #     label = Label(popupw, text='Sharpening parameters result is low. Output will darken')
    #     label.pack(side=TOP, fill=X, pady=20)
    #     okbutton = Button(popupw, text='Ok', command=popupw.destroy)
    #     okbutton.pack()
    #     popupw.mainloop()

    bs_amount = 0
    if(blur_amount==1):
        bs_amount=3
    if(blur_amount==2):
        bs_amount=5
    if(blur_amount==3):
        bs_amount=7

    # loader = Tk()
    # loader.title('Processing')
    # load_label = Label(loader, text='Removing Screentones. Please wait')
    # load_label.pack(fill=X, pady=10, padx=20)
    # loader.update()
    for i in inputs:
        img = imread(dir_i + '/' + i)
        blurred = blur(img, bs_amount)
        ret = sharp(blurred, sh_point, sh_low)
        sucess = imwrite(dir_o + '/' + i, ret)
        if(sucess != True):
            log('An error occured', Ansi.RED)
    log('ToneRemover has done running', Ansi.GREEN)

    # loader.destroy()
    # popup = Tk()
    # popup.title('Success!')
    # label = Label(popup, text='Process executed successfully!')
    # label.pack(side=TOP, fill=X, pady=20)
    # okbutton = Button(popup, text='Ok', command=popup.destroy)
    # okbutton.pack()
    # popup.mainloop()

dtext = ""
otext = ""

# def dnewdir():
#     dtext = filedialog.askdirectory(title='Choose directory for input images (.png recommended)')
#     dvar.set(dtext)

# def onewdir():
#     otext = filedialog.askdirectory(title='Choose directory for output images (.png recommended)')
#     ovar.set(otext)

if __name__ == '__main__':
    d_entry = './input'
    o_entry = './output'
    filtslide = 2
    sharpSlide = 5.56
    shEntry = -1.14
    removeScreentones(d_entry, o_entry, filtslide, sharpSlide, shEntry)
    # root = Tk()
    # root.title("Screentone Remover v." + versionNumber)

    # tFrame = Frame(root)
    # bFrame = Frame(root)

    # dvar = StringVar(root)
    # ovar = StringVar(root)

    # d_label = Label(tFrame, text = 'Input file directory: ')
    # d_label.grid(row=1, sticky=E, padx=20, pady=20)
    # d_entry = Entry(tFrame, textvariable = dvar)
    # d_entry.insert(0, "./input")
    # d_entry.grid(row=1, column=1)
    # dir_button = Button(tFrame, text="Browse", command=dnewdir)
    # dir_button.grid(row=1, column=2)
    
    # o_label = Label(tFrame, text = 'Output file directory: ')
    # o_label.grid(row=2,sticky=E)
    # o_entry = Entry(tFrame, textvariable=ovar)
    # o_entry.insert(0, "./output")
    # o_entry.grid(row=2, column=1)
    # out_button = Button(tFrame, text="Browse", command=onewdir)
    # out_button.grid(row=2, column=2)

    # slideLabel = Label(bFrame, text = 'Blur amount: (Default is 2)')
    # slideLabel.grid(row=0, padx=20)
    # filtslide = Scale(bFrame, from_=1, to=3, orient=HORIZONTAL)
    # filtslide.grid(row=1, columnspan=2)
    # filtslide.set(2)

    # helpLabel = Label(bFrame, text = 'Sharpening: | point strength + (4 * low strength) | should be ~= 0')
    # helpLabel.grid(row=5, padx=10)
    # sharpLabel = Label(bFrame, text = 'Sharpening point strength: (Default is +5.56)')
    # sharpLabel.grid(row=2, padx=20)
    # sharpSlide = Entry(bFrame)
    # sharpSlide.grid(row=3)
    # sharpSlide.insert(0, '5.56')
    # shLabel = Label(bFrame, text = 'Sharpening low strength:  (Default is -1.14)')
    # shLabel.grid(row=4, padx=20)
    # helpLabel = Label(bFrame, text = 'NOTE: Must be negative, absolute val should be == (1/4) * point strength')
    # helpLabel.grid(row=5, padx=10)
    # shEntry = Entry(bFrame)
    # shEntry.grid(row=6, padx=20)
    # shEntry.insert(0, '-1.14')

    # go_button = Button(bFrame, text="Go!", command = lambda: removeScreentones(d_entry.get(), o_entry.get(), filtslide.get(), sharpSlide.get(), shEntry.get()))
    # go_button.grid( columnspan=2)
    # root.geometry("400x420")
    # tFrame.pack(fill="both", expand=True)
    # bFrame.pack(fill="both", expand=True)

    # root.mainloop()
    

    # pass
