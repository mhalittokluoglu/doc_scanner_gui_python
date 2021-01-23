#/usr/bin/python3
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import img2pdf
from pikepdf import _cpphelpers
from tkinter import messagebox
class GUI_App:
    def __init__(self,win):

        self.del_cropped_images = 'del /s /q .\Cropped_images\*'
        image_empty = np.zeros([640,480,3],np.uint8)
        cv_img = cv2.cvtColor(image_empty,cv2.COLOR_BGR2RGB)
        img1 = Image.fromarray(cv_img);
        self.empty_image= ImageTk.PhotoImage(image = img1)


        x1_init = 10
        x2_init = 390
        y1_init = 20
        y2_init = 600
        self.x_r_cor = [x1_init,x2_init,x2_init,x1_init]
        self.y_r_cor = [y1_init,y1_init,y2_init,y2_init]
        self.x_cor = [0,0,0,0]
        self.y_cor = [0,0,0,0]

        self.error_photos = []


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
        self.photo_label.bind('<Button-1>', self.get_Position)
        self.open_image_bttn = tk.Button(right_frame,text = 'Open Images', command = self.open_images)
        self.counter_label = tk.Label(right_frame,text = '')
        self.counter_entry = tk.Entry(right_frame)
        self.next_bttn = tk.Button(right_frame,text = 'Next Image',command = self.next_image_func)
        self.prev_bttn = tk.Button(right_frame,text = 'Prev Image',command = self.prev_image_func)
        self.lu_bttn = tk.Button(right_frame,text = 'Left Upper Coordinate',command = self.lu_func)
        self.lu_label = tk.Label(right_frame,text = '0')
        self.ru_bttn = tk.Button(right_frame,text = 'Right Upper Coordinate',command = self.ru_func)
        self.ru_label = tk.Label(right_frame,text = '0')
        self.rd_bttn = tk.Button(right_frame,text = 'Right Down Coordinate',command = self.rd_func)
        self.rd_label = tk.Label(right_frame,text = '0')
        self.ld_bttn = tk.Button(right_frame,text = 'Left Down Coordinate',command = self.ld_func)
        self.ld_label = tk.Label(right_frame,text = '0')
        self.find_cor_bttn = tk.Button(right_frame,text = 'Try To Find Coordinates',command = self.find_cor_image)
        self.save_bttn = tk.Button(right_frame,text='Save the Cropped Image',command = self.save_image)
        self.save_all_bttn = tk.Button(right_frame,text = 'Try To Crop All Images',command = self.save_them_all)
        self.error_label = tk.Label(right_frame,text = '')
        self.convert_pdf_bttn = tk.Button(right_frame,text = 'Convert Cropped Images To PDF',command = self.convert2pdf_func)
        self.chk_a4 = tk.Checkbutton(right_frame,text = 'A4 Format',variable = self.check_var,onvalue = 1,offvalue=0,command = self.check_changed)
        self.del_cr_images_bttn = tk.Button(right_frame,text = 'Delete Cropped Images',command = self.del_cr_images)
        self.open_th_program_bttn = tk.Button(right_frame,text = 'Open TH Program',command = self.open_th_program)

        self.counter_entry.bind("<Return>", self.onReturn)

        self.open_image_bttn.grid(row = 0, column = 0)
        self.counter_entry.grid(row = 1, column = 0)
        self.counter_label.grid(row = 1, column = 1)
        self.prev_bttn.grid(row = 2, column = 0)
        self.next_bttn.grid(row = 2, column = 1)
        self.lu_bttn.grid(row = 3, column = 0)
        self.lu_label.grid(row = 3, column = 1)
        self.ru_bttn.grid(row = 4, column = 0)
        self.ru_label.grid(row = 4, column = 1)
        self.rd_bttn.grid(row = 5, column = 0)
        self.rd_label.grid(row = 5, column = 1)
        self.ld_bttn.grid(row = 6, column = 0)
        self.ld_label.grid(row = 6, column = 1)
        self.find_cor_bttn.grid(row = 7, column = 0, columnspan = 2)
        self.save_bttn.grid(row = 8, column = 0, columnspan = 2)
        self.save_all_bttn.grid(row = 9, column = 0, columnspan = 2)
        self.error_label.grid(row = 10, column = 0, columnspan = 2)
        self.convert_pdf_bttn.grid(row = 11, column = 0, columnspan = 2)
        self.chk_a4.grid(row = 12,column = 0, columnspan = 2)
        self.del_cr_images_bttn.grid(row = 13, column = 0, columnspan = 2)
        self.open_th_program_bttn.grid(row = 14, column = 0, columnspan = 2)

    def get_Position(self,event):
        self.x_cor1,self.y_cor1 = event.x,event.y

    def lu_func(self):
        self.x_r_cor[0] = self.x_cor1
        self.y_r_cor[0] = self.y_cor1
        self.lu_label['text'] = f'{self.x_r_cor[0]} {self.y_r_cor[0]}'
        self.show_image()

    def ru_func(self):
        self.x_r_cor[1] = self.x_cor1
        self.y_r_cor[1] = self.y_cor1
        self.ru_label['text'] = f'{self.x_r_cor[1]} {self.y_r_cor[1]}'
        self.show_image()

    def rd_func(self):
        self.x_r_cor[2] = self.x_cor1
        self.y_r_cor[2] = self.y_cor1
        self.rd_label['text'] = f'{self.x_r_cor[2]} {self.y_r_cor[2]}'
        self.show_image()

    def ld_func(self):
        self.x_r_cor[3] = self.x_cor1
        self.y_r_cor[3] = self.y_cor1
        self.ld_label['text'] = f'{self.x_r_cor[3]} {self.y_r_cor[3]}'
        self.show_image()


    def open_images(self):
        self.images_names = os.listdir('./Images/')
        self.image_counter = 0
        self.images_names.sort()
        self.image_number = 0
        for item in self.images_names:
            self.image_number += 1
        self.show_image()


    def find_cor_image(self):
        try:
            pts0 = self.get_image_cor()
            for i in range(0,4):
                self.x_cor[i] = pts0[i][0]
                self.y_cor[i] = pts0[i][1]
                self.x_r_cor[i] = pts0[i][0]/self.width_ratio
                self.y_r_cor[i] = pts0[i][1]/self.height_ratio
            self.show_image()
        except TypeError:
            pass

    def show_image(self):
        self.current_image = cv2.imread('./Images/'+self.images_names[self.image_counter])
        self.width_ratio = self.current_image.shape[1]/480
        self.height_ratio = self.current_image.shape[0]/640
        for i in range(0,4):
            self.x_cor[i] = self.x_r_cor[i]*self.width_ratio
            self.y_cor[i] = self.y_r_cor[i]*self.height_ratio

        resized_image = cv2.resize(self.current_image,(480,640))
        resized_copy = resized_image.copy()
        try:
            resized_copy = cv2.circle(resized_copy,(int(self.x_r_cor[0]),int(self.y_r_cor[0])), 3, (0,255,0),-1)
            resized_copy = cv2.circle(resized_copy,(int(self.x_r_cor[1]),int(self.y_r_cor[1])), 3, (0,255,0),-1)
            resized_copy = cv2.circle(resized_copy,(int(self.x_r_cor[2]),int(self.y_r_cor[2])), 3, (0,255,0),-1)
            resized_copy = cv2.circle(resized_copy,(int(self.x_r_cor[3]),int(self.y_r_cor[3])), 3, (0,255,0),-1)
        except AttributeError:
            pass
        cv_img = cv2.cvtColor(resized_copy,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_img)
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
        w1 = self.x_cor[1]-self.x_cor[0]
        w2 = self.x_cor[2]-self.x_cor[3]
        wdth = max(w1,w2)

        h1 = self.y_cor[3]-self.y_cor[0]
        h2 = self.y_cor[2]-self.y_cor[1]
        hgth = max(h1,h2)
        pts1 = np.float32([[0,0],[wdth,0],[wdth,hgth],[0,hgth]])
        pts0 = np.zeros([4,2],dtype = 'float32')
        for i in range(0,4):
            pts0[i][0] = self.x_cor[i]
            pts0[i][1] = self.y_cor[i]

        op = cv2.getPerspectiveTransform(pts0,pts1)
        dst = cv2.warpPerspective(self.current_image,op,(int(wdth),int(hgth)))
        cv2.imwrite('./Cropped_images/'+self.images_names[self.image_counter],dst)

    def save_them_all(self):
        if self.image_counter != 0:
            self.image_counter = 0
        if len(self.error_photos) != 0:
            self.error_photos = []
        for i in range(0,self.image_number):
            self.show_image()
            self.find_cor_image()
            try:
                if int(self.error_photos[-1])-1 != self.image_counter:
                    self.save_image()
            except IndexError:
                self.save_image()
            self.next_image_func()
        if len(self.error_photos) != 0:
            warning_message = ''
            for item in self.error_photos:
                warning_message += item+','

            messagebox.showwarning("WARNING!!!","Images:"+warning_message+' did not cropped Properly')
            self.error_label['text'] = 'Errors at:'+ warning_message
        else:
            self.error_label['text'] = 'No error'

    def check_changed(self):
        if self.check_var.get() == 1:
            self.check_a4 = True
        else:
            self.check_a4 = False


    def convert2pdf_func(self):
        cropped_images = os.listdir('./Cropped_images/')
        i = 0
        for image in cropped_images:
            cropped_images[i] =  './Cropped_images/'+ cropped_images[i]
            i += 1
        cropped_images.sort()
        if self.check_a4 == True:
            a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
            layout_fun = img2pdf.get_layout_fun(a4inpt)
            with open('./Cropped_images.pdf','wb') as f:
                f.write(img2pdf.convert(cropped_images,layout_fun=layout_fun))
        else:
            with open('./Cropped_images.pdf','wb') as f:
                f.write(img2pdf.convert(cropped_images))




    def del_cr_images(self):
        os.system(self.del_cropped_images)

    def open_th_program(self):
        os.system("python th_images.py")

    def onReturn(self,*args):
        try:
            counter_img = int(self.counter_entry.get())-1
            if counter_img >= 0 and counter_img < self.image_number:
                self.image_counter = counter_img
                self.show_image()
        except ValueError:
            pass

    def order_points(self,h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2), dtype = "float32")
        s = h.sum(1)
        hnew[0] = h[np.argmin(s)]
        hnew[2] = h[np.argmax(s)]
        diff = np.diff(h, axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
        return hnew


    def get_image_cor(self):
        img = self.current_image.copy()
        self.width_ratio = img.shape[1]/480
        self.height_ratio = img.shape[0]/640
        img = cv2.resize(img,(480,640))
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),0)
        edged = cv2.Canny(blurred,30,50)
        contours,hierarchy = cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours,key=cv2.contourArea,reverse = True)
        for c in contours:
            area = cv2.contourArea(c)
            if area> 1000:
                p = cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,0.02*p,True)
                if len(approx) == 4:
                    target = approx
                    break
        try:
            approx2 = self.order_points(target)
            approx3 = np.zeros((4,2), dtype = "float32")
            for i in range(0,4):
                approx3[i][0] = approx2[i][0]*self.width_ratio

            for i in range(0,4):
                approx3[i][1] = approx2[i][1]*self.height_ratio

            return approx3
        except UnboundLocalError:
            print(f'Error in {self.images_names[self.image_counter]} --> {self.image_counter+1}')
            self.error_photos.append(str(self.image_counter+1))



win = tk.Tk()
win.title('Scanner App')
prog = GUI_App(win)
win.mainloop()
