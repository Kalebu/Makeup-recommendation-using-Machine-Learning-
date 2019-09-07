from tkinter import *
from tkinter import filedialog
from sklearn.externals import joblib
import cv2
import threading
from threading import Thread
from PIL import Image
import time


#================window definition=====================

class Focus():
	approve = False
	proceed = False
	image_pixel = None
	model = joblib.load('Fashion.pkl')

	def __init__(self, root):
		self.ocula = cv2
		root.title("Fashion-Prediction")
		root.geometry("1080x720")
		root.configure(background="#454")
		self.image_button = Button(root, text="Load Image",bg="#173", fg="#112",relief="flat", command=self.load_file)
		self.take_a_picture = Button(root,text='Take a picture', bg="#187", fg = 'White', relief='flat', command=self.body)
		self.cancel_taking_picture = Button(root,text='Cancel', bg="black", fg = 'red', relief='flat', command=lambda:self.check_take_action(cancel=True, take=True))
		self.take_now = Button(root,text='Take', bg="black", fg = 'White', relief='flat', command=lambda:self.check_take_action(take=True, cancel=False))
		self.image_section = Label(root,width=500, height=500)
		self.information_section = Label(root, width=30, height=3)
		self.image_button.place(x=200, y=50)
		self.take_a_picture.place(x=200, y=300)
	
	def load_file(self):
		self.file_name = filedialog.askopenfilename()
		picture = Image.open(self.file_name)
		picture = picture.resize((250, 300), resample=0, box = None)
		picture.save('load_image.png')
		self.body(filename='load_image.png')

	def show_take_option(self, state = False):
		if state:
			self.take_now.place(x=150, y=400)
			self.cancel_taking_picture.place(x=350, y=400)
			self.image_section.place(x = 450, y = 200)
		else:
			self.take_now.place_forget()
			self.cancel_taking_picture.place_forget()
			self.image_section.place_forget()

	def information_menu(self, state=False):
		if state:
			self.information_section.place(x=100, y=450)
			self.image_section.place(x=450, y=100)
		else:
			self.information_section.place_forget()
			self.image_section.place_forget()
	
	def information_section_section(self, info):
		self.information_menu(state=True)
		self.information_section.configure(text=info)
		self.image_section.configure(image=self.image_pixel)

	def develop_report(self, category):
		category = category +1 
		if category:
			class_name = category[0]
			result = 'The person need makeup class {} '.format(class_name)
			print(result)
			self.information_section_section(result)
		else:
			pass

	def predict(self, image_name = 'temp.png'):
		temp_img = Image.open(image_name)
		temp_img = temp_img.resize((250, 300), resample=False, box=None)
		temp_img.save('resized.png')
		self.image_pixel = PhotoImage(file = image_name)
		pred_img = cv2.imread('resized.png', 0).reshape(1, -1)
		category = self.model.predict(pred_img)
		self.develop_report(category)
		pass


	def check_take_action(self, take=False, cancel=False, from_s = False):
		if take:
			self.show_thread.do_run = False
			print('stopping')
			self.ocula.destroyAllWindows()
			print('allow window destroyed')
			self.camera.release()
			print('camera realesed')
			print('stopped')
			if cancel:
				pass
			else:
				print('predicting')
				self.predict()
				time.sleep(1)
				print('predicted')
			

	def showing_picture(self):
		self.camera = self.ocula.VideoCapture(0)
		self.camera.set(3, 500)
		self.camera.set(4, 500)
		if self.camera.isOpened():
			camera_state, frame = self.camera.read()
		else:
			camera_state = False	 
		c_thread = threading.currentThread()
		if camera_state:		
			while camera_state and getattr(c_thread, "do_run", True):
				camera_state, frame = self.camera.read()
				self.ocula.imwrite('temp.png', frame)
				#frame.save('temp.png')
				plant_picture = PhotoImage(file = 'temp.png')
				self.image_section.configure(image = plant_picture)
				time.sleep(0.01)
		pass

	def body(self, filename=None):
		if filename:
			self.show_take_option()
			self.predict(filename)
			pass
		else:
			self.information_menu()
			self.show_take_option(state=True)
			self.show_thread = Thread(target=self.showing_picture)
			self.show_thread.daemon=True
			self.show_thread.start()
			pass
root = Tk()
eye = Focus(root)
root.mainloop()
