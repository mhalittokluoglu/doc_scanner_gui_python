import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from tkinter import messagebox
import img2pdf
class GUI_App:
    def __init__(self,win):

        self.del_th_images = 'rm -f ./TH_Images/*'
        self.a = 125
        self.c = 12
        image_empty = np.zeros([640,480,3],np.uint8)
        cv_img = cv2.cvtColor(image_empty,cv2.COLOR_BGR2RGB)
        img1 = Image.fromarray(cv_img);
        self.empty_image= ImageTk.PhotoImage(image = img1)

        self.check_a4 = False
        self.check_var = tk.IntVar()


        main_frame = tk.Frame(win)
        photo_frame = tk.Frame(main_frame)

        right_frame = tk.Frame(main_frame)

        main_frame.grid(row = 0, column = 0)
        photo_frame.grid(row = 0, column = 0)
        right_frame.grid(row = 0, column = 1)

        self.photo_label = tk.Label(photo_frame,image = self.empty_image)
        self.photo_label.grid(row = 0, column = 0)
        self.open_image_bttn = tk.Button(right_frame,text = 'Open Images', command = self.open_images)
        self.counter_label = tk.Label(right_frame,text = '')
        self.counter_entry = tk.Entry(right_frame)
        self.next_bttn = tk.Button(right_frame,text = 'Next Image',command = self.next_image_func)
        self.prev_bttn = tk.Button(right_frame,text = 'Prev Image',command = self.prev_image_func)
        self.a_label = tk.Label(right_frame,text = 'A:')
        self.a_entry = tk.Entry(right_frame)
        self.a_entry.insert(0,str(self.a))
        self.c_label = tk.Label(right_frame,text = 'C:')
        self.c_entry = tk.Entry(right_frame)
        self.c_entry.insert(0,str(self.c))
        self.save_bttn = tk.Button(right_frame,text='Save the Thresholded Image',command = self.save_image)
        self.save_all_bttn = tk.Button(right_frame,text = 'Try To Threshold All Images',command = self.save_them_all)
        self.convert_pdf_bttn = tk.Button(right_frame,text = 'Convert Thresholded Images To PDF',command = self.convert2pdf_func)
        self.chk_a4 = tk.Checkbutton(right_frame,text = 'A4 Format',variable = self.check_var,onvalue = 1,offvalue=0,command = self.check_changed)
        self.del_th_images_bttn = tk.Button(right_frame,text = 'Delete TH Images',command = self.del_th_images_func)

        self.counter_entry.bind("<Return>", self.onReturn)
        self.a_entry.bind("<Return>",self.get_a_Val)
        self.c_entry.bind("<Return>",self.get_c_Val)

        self.open_image_bttn.grid(row = 0, column = 0)
        self.counter_entry.grid(row = 1, column = 0)
        self.counter_label.grid(row = 1, column = 1)
        self.prev_bttn.grid(row = 2, column = 0)
        self.next_bttn.grid(row = 2, column = 1)
        self.a_label.grid(row = 3, column = 0)
        self.a_entry.grid(row = 3, column = 1)
        self.c_label.grid(row = 4, column = 0)
        self.c_entry.grid(row = 4, column = 1)
        self.save_bttn.grid(row = 5, column = 0, columnspan = 2)
        self.save_all_bttn.grid(row = 6, column = 0, columnspan = 2)
        self.convert_pdf_bttn.grid(row = 7, column = 0, columnspan = 2)
        self.chk_a4.grid(row = 8,column = 0, columnspan = 2)
        self.del_th_images_bttn.grid(row = 9, column = 0, columnspan = 2)

    def open_images(self):
        self.images_names = os.listdir('./Cropped_images/')
        self.image_counter = 0
        self.images_names.sort()
        self.image_number = 0
        for item in self.images_names:
            self.image_number += 1
        self.show_image()


    def th_bgr_img(self,img,a,c):
        b,g,r = cv2.split(img)
        th_b = cv2.adaptiveThreshold(b,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,a,c)
        th_g = cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,a,c)
        th_r = cv2.adaptiveThreshold(r,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,a,c)
        img2 = cv2.merge((th_b,th_g,th_r))
        return img2

    def show_image(self):
        self.current_image = cv2.imread('./Cropped_images/'+self.images_names[self.image_counter])
        current_image_gray = cv2.cvtColor(self.current_image,cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(self.current_image,(480,640))
        self.th1 = self.th_bgr_img(resized_image,self.a,self.c)
        self.th2 = self.th_bgr_img(self.current_image,self.a,self.c)
        img = Image.fromarray(self.th1)
        self.c_image_copy = ImageTk.PhotoImage(image = img)
        self.photo_label.imgtk = self.c_image_copy
        self.photo_label.configure(image = self.c_image_copy)
        self.counter_entry.delete(0,'end')
        self.counter_entry.insert(0,str(self.image_counter+1))
        self.counter_label['text'] = 'of '+ str(self.image_number)


    def next_image_func(self):
        if self.image_number > self.image_counter+1:
            self.image_counter += 1
        self.show_image()

    def prev_image_func(self):
        if self.image_counter > 0:
            self.image_counter -= 1
        self.show_image()

    def save_image(self):
        cv2.imwrite('./TH_Images/'+self.images_names[self.image_counter],self.th2)

    def save_them_all(self):
        if self.image_counter != 0:
            self.image_counter = 0
        for i in range(0,self.image_number):
            self.show_image()
            self.save_image()
            self.next_image_func()

    def check_changed(self):
        if self.check_var.get() == 1:
            self.check_a4 = True
        else:
            self.check_a4 = False

    def convert2pdf_func(self):
        th_images = os.listdir('./TH_Images/')
        i = 0
        for image in th_images:
            th_images[i] =  './TH_Images/'+ th_images[i]
            i += 1
        th_images.sort()
        if self.check_a4 == True:
            a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
            layout_fun = img2pdf.get_layout_fun(a4inpt)
            with open('./TH_Images.pdf','wb') as f:
                f.write(img2pdf.convert(th_images,layout_fun=layout_fun))
        else:
            with open('./TH_Images.pdf','wb') as f:
                f.write(img2pdf.convert(th_images))

    def del_th_images_func(self):
        os.system(self.del_th_images)

    def onReturn(self,*args):
        try:
            counter_img = int(self.counter_entry.get())-1
            if counter_img >= 0 and counter_img < self.image_number:
                self.image_counter = counter_img
                self.show_image()
        except ValueError:
            pass

    def get_a_Val(self,*args):
        try:
            self.a = int(self.a_entry.get())
            if self.a % 2 == 0:
                self.a = self.a + 1
            if self.a < 3:
                self.a = 3
            self.a_entry.delete(0,'end')
            self.a_entry.insert(0,str(self.a))
            self.show_image()
        except ValueError:
            pass

    def get_c_Val(self,*args):
        try:
            self.c = int(self.c_entry.get())
            if self.c < 1:
                self.c = 1
            self.c_entry.delete(0,'end')
            self.c_entry.insert(0,str(self.c))
            self.show_image()
        except ValueError:
            pass



win = tk.Tk()
win.title('Scanner App')
prog = GUI_App(win)
win.mainloop()
