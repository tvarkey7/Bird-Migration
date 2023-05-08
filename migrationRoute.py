#======================================= Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import netCDF4 as nc 
from netCDF4 import Dataset
import csv, math, random, time
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cartopy.crs as ccrs
import cartopy.feature as cf 
from sklearn import linear_model
import smtplib
import os
from email.message import EmailMessage 
import imghdr
import re
print('Debug - No issues with libraries')
#========================================
f_value = open("value.txt",'w')
#======================================= #Global Variables
Bird_name = ''
YearChosen =2020
Buttons = False
Button_win6 = False
height1=300
width1 = 500
tempincrease= 6 #this is just a filler value - it will be changed 
PlotButtonAvailable = True
RouteOffset = random.random()
RouteChange = ((tempincrease) * RouteOffset)+random.uniform(1,5)
email = ''	


#======================================= #Methods
def TempAnomaly(): #plotting the temp anomaly time series data
	# Average data across all grid points to create a global average time series.
	global_average = np.mean(temp[:,:,:], axis=(1,2))
	annual_temp = np.mean(np.reshape(global_average, (117,12)), axis = 1) # reshape the data into [117,12] as there are 117 years in the dataset,each with 12 months, then calculate the average for each year
	# Calculate the 1961-1990 average
	# the annual temperature is sliced with the indices 60:89 to give the values from 1960 to 1990
	av_1961_1990 = np.mean(annual_temp[60:89])# idk why but the value range wanted needs to be -1 at the end, idk.
	# Calculate the annual anomaly values compared to the 1961-1990 average
	temp_anomaly = annual_temp - av_1961_1990
	# Plot Timeseries
	plt.figure()
	plt.plot(np.arange(1901,2018,1), temp_anomaly)
	plt.ylim(np.floor(min(temp_anomaly)), np.ceil(max(temp_anomaly)))
	plt.title("Global Average Temperature Anomaly (1901-2017)")
	plt.xlabel("Years")
	plt.ylabel(u"Difference from 1961-1990 average (\u2103)")
	plt.show()



#======================== Closing Window (win11)
def win11():
	window = Tk()
	window.iconbitmap('icon1.ico')
	height2 = 300
	width2 = 500 #
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width2/2)
	y_coord=(s_height/2)-(height2/2)
	window.geometry(f'{width2}x{height2}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')
	#window.attributes('-topmost', 1)
	#window.attributes('-topmost', 0)
	l1 = Label(window, text='Thank you for using this Program\nPress Exit to exit the program. ', pady=20).pack()
	b1 = Button(window,text='Exit',command=lambda:[window.destroy()]).pack()
#=======window 10
def win10():
	window = Tk()
	window.iconbitmap('icon1.ico')
	height2 = 300
	width2 = 500
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width2/2)
	y_coord=(s_height/2)-(height2/2)
	window.geometry(f'{width2}x{height2}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')
	l1 = Label(window, text='Your modelled route has been saved!\nWould you like to e-mail it?').pack()



	def mail():
		window2=Tk()
		window2.iconbitmap('icon1.ico')
		#window2.attributes('-topmost', 1)
		#window2.attributes('-topmost', 0)
		height1 = 300
		width1 = 500
		s_width=window2.winfo_screenwidth()
		s_height=window2.winfo_screenheight()
		x_coord=(s_width/2)-(width1/2)
		y_coord=(s_height/2)-(height1/2)
		window2.geometry(f'{width1}x{height1}+{int(x_coord)}+{int(y_coord)}')
		window2.title('Bird Migration Investigation')
		l1 = Label(window2, text='Enter the e-mail address you would like the model to be sent to.\n').pack()
		email_enter = Entry(window2,bg="light grey",bd = 4, relief=FLAT,width=50)
		email_enter.pack()
		l2 = Label(window2, text= '')
		l2.pack()
		#the line below is the regular expression for the accepted email
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]+[a-z]+[.]\w{2,3}$'
		
		def validate2(email): 
			if re.search(regex, email): #this checks the regular expression to the email entered
				print("mailed to: "+email)
				send_mail() 
				b3 = Button(window2, text = 'Next', command=lambda:[window2.destroy(),win11()], relief=GROOVE, pady=5)
				b3.pack(anchor=E)
			else:
				print("Not mailed")
				l2.config(text='invalid email address - Please re-enter an email address')
				#get_email()
				#validate2(email)

		
		def send_mail():
			#referencing an environment variable (made manually)	
			#the reason for using environment variables is to remove the need to put passwords (or sensitive info)in code.
			EMAIL_ADDRESS = os.environ.get('emailadd')
			EMAIL_PASSWORD = os.environ.get('emailpwd')
			email = email_enter.get()
			msg = EmailMessage()
			msg['Subject'] = 'Bird Migration Model'
			msg['From'] = EMAIL_ADDRESS
			msg['To'] = email
			msg.set_content('Attached is an image of the route you modelled.')

			#opening the saved image of the modelled route and reading the bytes
			with open('MigrationRoute.png','rb') as f: 
				#reading the file's data and storing it as a variable
				file_data = f.read() 
				#getting the file type as a variable to use it as one of the paramenters for the attachment subroutine
				file_type = imghdr.what(f.name)
				file_name = f.name
			#adding the attachment to the email
			msg.add_attachment(file_data, maintype='image', subtype=file_type,filename=file_name)
			#opens communication with the mail server - I'm using Gmail and port 587 (SMTP port)
			with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
				#identifies us to the mail server
				smtp.ehlo()
				#encrypts our emails
				smtp.starttls()
				#re-identifies us to the mail server - now encrypted
				smtp.ehlo()
				#login to mail server
				smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
				#sending the email
				smtp.send_message(msg)
		def get_email():
			global email
			email = email_enter.get() #storing the email entered as a global variable to validate it
			email = email.lower() #converts the email they entered into lowercase
			return email
		
		b1 = Button(window2, text='Send e-mail',command=lambda:[get_email(),validate2(email)]).pack()

	#the variable of the radio button
	i = IntVar(window)
	i.set("2") 


	r1 = Radiobutton(window, text="Yes", value=1, variable=i)
	r2 = Radiobutton(window, text="No", value=2,variable=i)
	r1.pack()
	r2.pack()

	def choice2():
		if i.get() == 1:
			#time.sleep(1)
			print("Mail Chosen")
			mail()
		elif i.get() == 2:
			win11()
			#print("email not sent")
		else:
			print("error - choice not recognised")
			


	button = Button(window, text="select", command=lambda:[window.destroy(), choice2()])
	button.pack()
#======================================= window 9
def win9():
	window = Tk()
	window.iconbitmap('icon1.ico')
	height1 = 300
	width1 = 500
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width1/2)
	y_coord=(s_height/2)-(height1/2)
	window.geometry(f'{width1}x{height1}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')

	def save_graph():   # This subroutine creates routes. The way its being done is by creating a map first, then the specific routes can be drawn onto the map.
		ax = plt.axes(projection=ccrs.PlateCarree())
		ax.coastlines()
		ax.stock_img()
		ax.set_extent([-25,60,-40,60])
		def Route1(): #plotting the map  -Route1() is the subroutine that draws lines onto the map for the Nightingale.
			#=============================arrays for co-ords
			xs= []
			ys = []       #These are empty arrays. I create co-ordinates then append it to the empty arrays and then plot the values inside the arrays

			#=================================Nightingale route
			#---Start pt
			s0lat, s0lon = -0.1689,52.13         #these are the specific points at which the birds either stop (from my research) or they are seen flying over
			xs.append(s0lat)
			ys.append(s0lon)
			#-stop 1
			s1lat, s1lon = 2.343,49.3                 
			xs.append(s1lat)
			ys.append(s1lon)
			#-stop 2
			s2lat, s2lon = -0.719,42.67
			xs.append(s2lat)
			ys.append(s2lon)
			#-stop 3
			s3lat, s3lon = -5.646,42.42
			xs.append(s3lat)
			ys.append(s3lon)
			#-stop 4
			s4lat, s4lon = -8.884,39.26
			xs.append(s4lat)
			ys.append(s4lon)
			#-stop 5 
			s5lat, s5lon = -6.332,32.12
			xs.append(s5lat)
			ys.append(s5lon)
			#-stop 6
			s6lat, s6lon = -12.12,25.66
			xs.append(s6lat)
			ys.append(s6lon)
			#-stop 7
			s7lat, s7lon = -15.18,16.98
			xs.append(s7lat)
			ys.append(s7lon)
			#-stop 8
			s8lat, s8lon = -13.82,10.52
			xs.append(s8lat)
			ys.append(s8lon)

			ax.plot(xs,ys,markersize=3,color='r',label="Current Route")
			global RouteChange
			xs1s = [i+RouteChange for i in xs]
			ax.plot(xs1s,ys,markersize=3,color ='g', label = 'Projected')     #this line plots and gives the line a label. 
			#=============================================Raptor Route

		def Route2():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x2s = []
			y2s = []      
			#==========
			s0lat, s0lon = 29.95,63.38
			x2s.append(s0lat)
			y2s.append(s0lon)
			#-stop 1
			s1lat, s1lon = 27.51,50.87                  
			x2s.append(s1lat)
			y2s.append(s1lon)
			#-stop 2
			s2lat, s2lon = 24.38,41.8
			x2s.append(s2lat)
			y2s.append(s2lon)
			#-stop 3
			s3lat, s3lon = 33.14,37.42
			x2s.append(s3lat)
			y2s.append(s3lon)
			#-stop 4
			s4lat, s4lon = 32.83,26.47
			x2s.append(s4lat)
			y2s.append(s4lon)
			#-stop 5 
			s5lat, s5lon = 38.14,15.21
			x2s.append(s5lat)
			y2s.append(s5lon)
			#-stop 6
			s6lat, s6lon = 30.64,-4.497
			x2s.append(s6lat)
			y2s.append(s6lon)
			#-stop 7
			s7lat, s7lon = 29.07,-14.82
			x2s.append(s7lat)
			y2s.append(s7lon)
			#-stop 8
			s8lat, s8lon = 22.82,-25.14
			x2s.append(s8lat)
			y2s.append(s8lon)
			ax.plot(x2s,y2s,markersize=3,color='r',label="Current Route")
			#=====================================legend creation
			global RouteChange
			xs2s = [i+RouteChange for i in x2s]
			ax.plot(xs2s,y2s, markersize=3, color = 'g', label='Projected Route')
		

		def Route3():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x3s = []
			y3s = []      
			#==========
			s0lat, s0lon =23.76,55.25
			x3s.append(s0lat)
			y3s.append(s0lon)
			#-stop 1
			s1lat, s1lon = 11.24,51.49                 
			x3s.append(s1lat)
			y3s.append(s1lon)
			#-stop 2
			s2lat, s2lon = 6.24,52.12
			x3s.append(s2lat)
			y3s.append(s2lon)
			#-stop 3
			s3lat, s3lon =-0.329,47.43
			x3s.append(s3lat)
			y3s.append(s3lon)
			#-stop 4
			s4lat, s4lon = 1.548,34.29
			x3s.append(s4lat)
			y3s.append(s4lon)
			#-stop 5 
			s5lat, s5lon =-6.898, 13.33
			x3s.append(s5lat)
			y3s.append(s5lon)
			#-stop 6
			s6lat, s6lon = 9.055,7.389
			x3s.append(s6lat)
			y3s.append(s6lon)
			#-stop 7
			s7lat, s7lon = 14.37,-4.497
			x3s.append(s7lat)
			y3s.append(s7lon)

			ax.plot(x3s,y3s,markersize=3,color='r',label="Current Route")
			global RouteChange
			xs3s = [i+RouteChange for i in x3s]
			#=====================================legend creation
			ax.plot(xs3s,y3s, markersize=3, color = 'g', label='Projected Route')

		def Route4():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x4s = []
			y4s = []      
			#==========
			s0lat, s0lon =-2.206,53.99
			x4s.append(s0lat)
			y4s.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 3.112,48.36               
			x4s.append(s1lat)
			y4s.append(s1lon)
			ax.plot(s1lat, s1lon, 'go', markersize=3)
			#-stop 2
			s2lat, s2lon = 9.055,47.43
			x4s.append(s2lat)
			y4s.append(s2lon)
			ax.plot(s2lat, s2lon, 'go', markersize=3)
			#-stop 3
			s3lat, s3lon = 8.742,28.35
			x4s.append(s3lat)
			y4s.append(s3lon)
			ax.plot(s3lat, s3lon, 'go', markersize=3)
			#-stop 4
			s4lat, s4lon = 15.31,17.4
			x4s.append(s4lat)
			y4s.append(s4lon)
			ax.plot(s4lat, s4lon, 'go', markersize=3)
			#-stop 5 
			s5lat, s5lon = 18.75,5.825
			x4s.append(s5lat)
			y4s.append(s5lon)
			ax.plot(s5lat, s5lon, 'go', markersize=3)
			#-stop 6
			s6lat, s6lon = 22.82,-6.686
			x4s.append(s6lat)
			y4s.append(s6lon)
			ax.plot(s6lat, s6lon, 'go', markersize=3)
			#-stop 7
			s7lat, s7lon = 20.63, -15.76
			x4s.append(s7lat)
			y4s.append(s7lon)
			ax.plot(s7lat, s7lon, 'go', markersize=3)
			#stop 8
			s8lat, s8lon = 18.75, -26.08
			x4s.append(s8lat)
			y4s.append(s8lon)
			ax.plot(s8lat, s8lon, 'go', markersize=3)
			ax.plot(x4s, y4s, markersize=3,color='r',Label='Current Route')
			global RouteChange
			xs4s = [i+RouteChange for i in x4s]
			xs4s[0] = -2.206	
			ax.plot(xs4s,y4s, markersize=3, color = 'g', label='Projected Route')	
		
		global Bird_name                     #This is for the bird name selection. THe user can chose which bird they want to specifically look at. 
		                                     #It looks at the input taken before (the code is further below for the drop down menu) and then plots the route for the bird they picked. 
		if Bird_name=='Nightingale':
			Route1()
		elif Bird_name =='Raptor':
			Route2()
		elif Bird_name == "Eurasian Spoonbill":
			Route3()
		elif Bird_name == "Barn Swallow":
			Route4()
		else:
			print('Error - Internal Problem')
		ax.legend(loc='lower left')
		plt.title('Projected Migration Route')
		plt.savefig("MigrationRoute.png", bbox_inches="tight", pad_inches=1)
		


	l1 = Label(window, text="Would you like to save your modelled route?").pack()
	#b1 = Button(window, text="click", command=save_graph).pack()
	i = IntVar()
	i.set("2") 


	def choice2():
		if i.get() == 1:
			save_graph()
			win10()
			
		elif i.get() == 2:
			win11()

	r1 = Radiobutton(window, text="Yes", value=1, variable=i)
	r2 = Radiobutton(window, text="No", value=2,variable=i)
	r1.pack()
	r2.pack()

	button = Button(window, text="select", command=lambda:[window.destroy(),choice2()])
	button.pack()
#======================== window 8
def win8():
	window = Tk()
	window.iconbitmap('icon1.ico')
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')
	label=Label(window,text='Press the buttons below to create a map').pack(anchor=N)
	def button2():
		b2 = Button(window, text="Next", command = lambda:[window.destroy(),win9()],relief=GROOVE)
		b2.pack()
	def choose_graph():   # This subroutine creates routes. The way its being done is by creating a map first, then the specific routes can be drawn onto the map.
		ax = plt.axes(projection=ccrs.PlateCarree())
		ax.coastlines()
		ax.stock_img()
		ax.set_extent([-25,60,-40,60])
		def Route1(): #plotting the map  -Route1() is the subroutine that draws lines onto the map for the Nightingale.
			#=============================arrays for co-ords
			xs= []
			ys = []       #These are empty arrays. I create co-ordinates then append it to the empty arrays and then plot the values inside the arrays

			#=================================Nightingale route
			#---Start pt
			s0lat, s0lon = -0.1689,52.13         #these are the specific points at which the birds either stop (from my research) or they are seen flying over
			xs.append(s0lat)
			ys.append(s0lon)
			#-stop 1
			s1lat, s1lon = 2.343,49.3                 
			xs.append(s1lat)
			ys.append(s1lon)
			#-stop 2
			s2lat, s2lon = -0.719,42.67
			xs.append(s2lat)
			ys.append(s2lon)
			#-stop 3
			s3lat, s3lon = -5.646,42.42
			xs.append(s3lat)
			ys.append(s3lon)
			#-stop 4
			s4lat, s4lon = -8.884,39.26
			xs.append(s4lat)
			ys.append(s4lon)
			#-stop 5 
			s5lat, s5lon = -6.332,32.12
			xs.append(s5lat)
			ys.append(s5lon)
			#-stop 6
			s6lat, s6lon = -12.12,25.66
			xs.append(s6lat)
			ys.append(s6lon)
			#-stop 7
			s7lat, s7lon = -15.18,16.98
			xs.append(s7lat)
			ys.append(s7lon)
			#-stop 8
			s8lat, s8lon = -13.82,10.52
			xs.append(s8lat)
			ys.append(s8lon)

			ax.plot(xs,ys,markersize=3,color='r',label="Current Route")
			global RouteChange
			xs1s = [i+RouteChange for i in xs]
			ax.plot(xs1s,ys,markersize=3,color ='g', label = 'Projected')     #this line plots and gives the line a label. 
			#=============================================Raptor Route

		def Route2():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x2s = []
			y2s = []      
			#==========
			s0lat, s0lon = 29.95,63.38
			x2s.append(s0lat)
			y2s.append(s0lon)
			#-stop 1
			s1lat, s1lon = 27.51,50.87                  
			x2s.append(s1lat)
			y2s.append(s1lon)
			#-stop 2
			s2lat, s2lon = 24.38,41.8
			x2s.append(s2lat)
			y2s.append(s2lon)
			#-stop 3
			s3lat, s3lon = 33.14,37.42
			x2s.append(s3lat)
			y2s.append(s3lon)
			#-stop 4
			s4lat, s4lon = 32.83,26.47
			x2s.append(s4lat)
			y2s.append(s4lon)
			#-stop 5 
			s5lat, s5lon = 38.14,15.21
			x2s.append(s5lat)
			y2s.append(s5lon)
			#-stop 6
			s6lat, s6lon = 30.64,-4.497
			x2s.append(s6lat)
			y2s.append(s6lon)
			#-stop 7
			s7lat, s7lon = 29.07,-14.82
			x2s.append(s7lat)
			y2s.append(s7lon)
			#-stop 8
			s8lat, s8lon = 22.82,-25.14
			x2s.append(s8lat)
			y2s.append(s8lon)
			ax.plot(x2s,y2s,markersize=3,color='r',label="Current Route")
			#=====================================legend creation
			global RouteChange
			xs2s = [i+RouteChange for i in x2s]
			ax.plot(xs2s,y2s, markersize=3, color = 'g', label='Projected Route')
		

		def Route3():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x3s = []
			y3s = []      
			#==========
			s0lat, s0lon =23.76,55.25
			x3s.append(s0lat)
			y3s.append(s0lon)
			#-stop 1
			s1lat, s1lon = 11.24,51.49                 
			x3s.append(s1lat)
			y3s.append(s1lon)
			#-stop 2
			s2lat, s2lon = 6.24,52.12
			x3s.append(s2lat)
			y3s.append(s2lon)
			#-stop 3
			s3lat, s3lon =-0.329,47.43
			x3s.append(s3lat)
			y3s.append(s3lon)
			#-stop 4
			s4lat, s4lon = 1.548,34.29
			x3s.append(s4lat)
			y3s.append(s4lon)
			#-stop 5 
			s5lat, s5lon =-6.898, 13.33
			x3s.append(s5lat)
			y3s.append(s5lon)
			#-stop 6
			s6lat, s6lon = 9.055,7.389
			x3s.append(s6lat)
			y3s.append(s6lon)
			#-stop 7
			s7lat, s7lon = 14.37,-4.497
			x3s.append(s7lat)
			y3s.append(s7lon)

			ax.plot(x3s,y3s,markersize=3,color='r',label="Current Route")
			global RouteChange
			xs3s = [i+RouteChange for i in x3s]
			#=====================================legend creation
			ax.plot(xs3s,y3s, markersize=3, color = 'g', label='Projected Route')


		def Route4():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x4s = []
			y4s = []      
			#==========
			s0lat, s0lon =-2.206,53.99
			x4s.append(s0lat)
			y4s.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 3.112,48.36               
			x4s.append(s1lat)
			y4s.append(s1lon)
			ax.plot(s1lat, s1lon, 'go', markersize=3)
			#-stop 2
			s2lat, s2lon = 9.055,47.43
			x4s.append(s2lat)
			y4s.append(s2lon)
			ax.plot(s2lat, s2lon, 'go', markersize=3)
			#-stop 3
			s3lat, s3lon = 8.742,28.35
			x4s.append(s3lat)
			y4s.append(s3lon)
			ax.plot(s3lat, s3lon, 'go', markersize=3)
			#-stop 4
			s4lat, s4lon = 15.31,17.4
			x4s.append(s4lat)
			y4s.append(s4lon)
			ax.plot(s4lat, s4lon, 'go', markersize=3)
			#-stop 5 
			s5lat, s5lon = 18.75,5.825
			x4s.append(s5lat)
			y4s.append(s5lon)
			ax.plot(s5lat, s5lon, 'go', markersize=3)
			#-stop 6
			s6lat, s6lon = 22.82,-6.686
			x4s.append(s6lat)
			y4s.append(s6lon)
			ax.plot(s6lat, s6lon, 'go', markersize=3)
			#-stop 7
			s7lat, s7lon = 20.63, -15.76
			x4s.append(s7lat)
			y4s.append(s7lon)
			ax.plot(s7lat, s7lon, 'go', markersize=3)
			#stop 8
			s8lat, s8lon = 18.75, -26.08
			x4s.append(s8lat)
			y4s.append(s8lon)
			ax.plot(s8lat, s8lon, 'go', markersize=3)
			ax.plot(x4s, y4s, markersize=3,color='r',Label='Current Route')
			global RouteChange
			xs4s = [i+RouteChange for i in x4s]
			xs4s[0] = -2.206	
			ax.plot(xs4s,y4s, markersize=3, color = 'g', label='Projected Route')	

		global Bird_name                     #This is for the bird name selection. THe user can chose which bird they want to specifically look at. 
		                                     #It looks at the input taken before (the code is further below for the drop down menu) and then plots the route for the bird they picked. 
		if Bird_name=='Nightingale':
			Route1()
		elif Bird_name =='Raptor':
			Route2()
		elif Bird_name == "Eurasian Spoonbill":
			Route3()
		elif Bird_name == "Barn Swallow":
			Route4()
		else:
			print('Error - Internal Problem')
		ax.legend(loc='lower left')
		plt.title('Projected Migration Route')
		plt.show()
	b1 = Button(window, text = "Plot", command=lambda:[button2(),choose_graph()]).pack()
	l1 = Label(window, text='').pack()

#======================== window 7
def win7():
	window=Tk()
	window.iconbitmap('icon1.ico')
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')

	dataframe1 = pd.read_csv('CO2emissions.csv') #read the data file into a dataframe
	reg = linear_model.LinearRegression() 
	reg.fit(dataframe1[['Years']],dataframe1.Y_vals) #getting a regression line for my dataset
	co2val = reg.predict([[2050]]) # the value in the square brackets is the year for which you want a predicted value
	#print(str(co2val)[1:11])#the value predicted using the algorithm is then printed 
	#print(reg.coef_)  # in terms of graphs, this value is the gradient of the solid line of the graph
	#print(reg.intercept_)  #this is the y intercept of the solid line of the graph. In context, this would be the net CO2 emissions in the year 0AD.

	d=pd.read_csv("CO2emissions2.csv")#import data set to dataframe
	#print(d.head())
	p = reg.predict(d)#use the algorithm on the newly imported dataset
	#print(p)
	d['CO2'] = p
	#print(d)
	#d.to_csv('predictions.csv')

	#writing the values from the regressing algorithm to the file using a while loop
	col = 0
	year = 1970
	crbn = reg.predict([[year]])
	co2 = str(crbn)[1:11]
	with open('predictions.csv','w', newline="") as f:
	  wr=csv.writer(f)
	  headers = ['Years','CO2']
	  wr.writerow(headers)
	  while year < 2051:
	    year = year + 1
	    #col = col + 1
	    crbn = reg.predict([[year]])
	    co2 = str(crbn)[1:11] 
	    List = [year,co2]
	    wr.writerow(List)
	    if year == 2050:
	      break
	  f.close() 

	x,y = np.loadtxt('predictions.csv',unpack=True, delimiter=',', skiprows=1)

	merge_df1 = pd.read_csv("predictions.csv")
	merge_df2 = pd.read_csv("TempChange.csv")
	#============
	dataframe = pd.merge(merge_df1,merge_df2, left_on="Years",right_on="Years", how="left")
	params = dataframe.iloc[(dataframe['Years']-YearChosen).abs().argsort()[:1]] 
	#print(params)
	params.to_csv("test123.csv",header= None)

	def plotbutton():
		global 	PlotButtonAvailable
		if PlotButtonAvailable == True:
			PlotButtonAvailable = False
		button3 = Button(window, text='Plot Map', command=lambda:[window.destroy(),win8()],relief=GROOVE)
		button3.pack()

	def plot():
		plotbutton()
		fig = plt.Figure(figsize=(8,5), dpi=100)
		ax = fig.add_subplot(111)
		chart = FigureCanvasTkAgg(fig, window)
		ax.set_xlabel('Year')
		ax.set_ylabel('CO2 Emitted')
		ax.set_title('Forecasted CO2 Emissions until 2050')
		ax.plot(x,y)
		ax.plot(YearChosen,((reg.coef_*YearChosen)+reg.intercept_),'go')
		ax.annotate("Chosen Year", (YearChosen,((reg.coef_*YearChosen)+reg.intercept_)))
		#chart.title("Forecasted annual CO2 Emissions until 2050")
		chart.get_tk_widget().pack()
		with open('test123.csv', newline='') as f:
			reader = csv.reader(f)
			data = list(reader)
		print(data[0][3])
		label2.config(text='Your modelled increase is: ' + str(data[0][3]) +' Degrees C')
		global tempincrease
		tempincrease = data[0][3]
		return tempincrease
		
			

	
		

	label1 = Label(window, text="Your chosen year is " + str(YearChosen)).pack(anchor=N)
	l2 = Label(window, text="Press the button below to plot a graph that predicts the carbon dioxide emissions\n Plotting this will give you the increase in temperature.").pack()
	button1 = Button(window, text="Plot", command=plot, relief=GROOVE).pack(anchor=N)
	label2 = Label(window, text='')
	label2.pack()

#======================== window 6
def win6():
	window=Tk()
	window.iconbitmap('icon1.ico')
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')

	def validate():
		try:
			year = int(entry_year.get())
			if year > 2050:
				label2.config(text="Enter a smaller year between and including 2020 and 2050",fg="red")
			elif year < 2020:
				label2.config(text="Enter a larger year between and including 2020 and 2050", fg="red")
			elif 2016 <= year <= 2050:
				label2.config(text="Year Chosen! Press Next", fg='black')
				button = Button(window, text="Next", command=lambda:[window.destroy(), win7()],relief=GROOVE).pack(anchor=SE)
				global YearChosen
				YearChosen = year
				return YearChosen

		except:
			ValueError
			year=0
			label2.config(text="Please enter a year - Must be a whole number!",fg='red')

	label1 = Label(window, text="Enter the year you want to model - A year between and including 2020 and 2050").pack()
	entry_year = Entry(window,width=4,bg="light grey",bd = 4, relief=FLAT)
	entry_year.pack()
	l2 = Label(window,text='').pack()
	button1 = Button(window, text='Select',command=validate,relief=GROOVE)
	button1.pack()
	label2 = Label(window, text='')
	label2.pack()


#======================== window 5
def win5(): 
	window=Tk() #this is a subroutine from the Tkinter library - its used to create a window
	window.iconbitmap('icon1.ico')#from here to ...
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}') #... here is just designing the GUI. These settings are used to keep the sizes similar
	window.title('Bird Migration Investigation')
	style.use('ggplot')
	f_emissions = pd.read_csv('CO2Emissions.csv') #this gets the data from the CSV file and puts it into a pandas dataframe 
	#print(f_emissions.head())

	def CO2_graph(): #this subrouting creates a graph - this will be called on the press of a button
		series_value = f_emissions.values
		X= f_emissions['Years']#year    - it looks at the dataframe in pandas and takes data that's title is Years in the file
		Y = f_emissions['Y_vals']#emissions  - this does the same as the line above, just looks for data in the column that has the title Y_vals
		plt.title('Annual Global CO2 Emissions')
		plt.xlabel('Year')
		plt.ylabel('CO2 Emitted / Billion Tonnes')
		plt.plot(X,Y)
		plt.show()	
	#b1=Button(window, text='CO2 Emissions Graph upto 2016', command = CO2_graph).pack(anchor=N)

	def anomaly_graph():
		df = pd.read_csv('CO2emissions.csv') #read the data file into a dataframe

		reg = linear_model.LinearRegression() 
		reg.fit(df[['Years']],df.Y_vals) #getting a regression line for my dataset
		co2val = reg.predict([[2050]]) # the value in the square brackets is the year for which you want a predicted value
		#print(str(co2val)[1:11])#the value predicted using the algorithm is then printed 
		#print(reg.coef_)  # in terms of graphs, this value is the gradient of the solid line of the graph
		#print(reg.intercept_)  #this is the y intercept of the solid line of the graph. In context, this would be the net CO2 emissions in the year 0AD.

		plt.xlabel('Year')#x label
		plt.ylabel('CO2 Emiited (in Billion Tonnes)')#y label
		plt.scatter(df.Years, df.Y_vals, color='red', marker='.')
		plt.plot(df.Years,reg.predict(df[['Years']]),color='green')
		plt.title("Carbon Dioxide Annual Emissions")
		plt.show()

		d=pd.read_csv("CO2emissions2.csv")#import data set to dataframe
		#print(d.head())
		p = reg.predict(d)#use the algorithm on the newly imported dataset
		#print(p)
		d['CO2'] = p
		#print(d)
		#d.to_csv('predictions.csv')

		#writing the values from the regressing algorithm to the file using a while loop
		col = 0
		year = 1970
		crbn = reg.predict([[year]])
		co2 = str(crbn)[1:11]
		with open('predictions.csv','w', newline="") as f:
			wr=csv.writer(f)
			while year < 2051:
				year = year + 1
				#col = col + 1
				crbn = reg.predict([[year]])
				co2 = str(crbn)[1:11]	
				List = [year,co2]
				wr.writerow(List)
				if year == 2051:
					break
			f.close()	
			
		x,y = np.loadtxt('predictions.csv',unpack=True, delimiter=',')
	
	l1 = Label(window, text="Press the button to generate a graph that shows how much carbon dioxide is emitted annually").pack()
	b2=Button(window, text="CO2 emission anomaly graph", command=anomaly_graph).pack(anchor=N)
	l2 = Label(window, text="").pack()
	b3=Button(window, text='Next -->', command=lambda:[window.destroy(), win6()],relief=GROOVE).pack(anchor=S)

#==========================window 4

def win4():
	window=Tk()
	window.iconbitmap('icon1.ico')
	height = 550
	width = 550
	global Bird_name
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')
	label=Label(window,text='Press the button below to generate the current bird migration route for the '+Bird_name).pack(anchor=N)
	def choose_graph():   # This subroutine creates routes. The way its being done is by creating a map first, then the specific routes can be drawn onto the map.
		ax = plt.axes(projection=ccrs.PlateCarree())
		ax.coastlines()
		ax.stock_img()
		ax.set_extent([-25,60,-40,60])
		def Route1(): #plotting the map  -Route1() is the subroutine that draws lines onto the map for the Nightingale.
			#=============================arrays for co-ords
			xs= []
			ys = []       #These are empty arrays. I create co-ordinates then append it to the empty arrays and then plot the values inside the arrays

			#=================================Nightingale route
			#---Start pt
			s0lat, s0lon = -0.1689,52.13         #these are the specific points at which the birds either stop (from my research) or they are seen flying over
			xs.append(s0lat)
			ys.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 2.343,49.3                 
			xs.append(s1lat)
			ys.append(s1lon)
			ax.plot(s1lat, s1lon, 'ro', markersize=3)
			#-stop 2
			s2lat, s2lon = -0.719,42.67
			xs.append(s2lat)
			ys.append(s2lon)
			ax.plot(s2lat, s2lon, 'ro', markersize=3)
			#-stop 3
			s3lat, s3lon = -5.646,42.42
			xs.append(s3lat)
			ys.append(s3lon)
			ax.plot(s3lat, s3lon, 'ro', markersize=3)
			#-stop 4
			s4lat, s4lon = -8.884,39.26
			xs.append(s4lat)
			ys.append(s4lon)
			ax.plot(s4lat, s4lon, 'ro', markersize=3)
			#-stop 5 
			s5lat, s5lon = -6.332,32.12
			xs.append(s5lat)
			ys.append(s5lon)
			ax.plot(s5lat, s5lon, 'ro', markersize=3)
			#-stop 6
			s6lat, s6lon = -12.12,25.66
			xs.append(s6lat)
			ys.append(s6lon)
			ax.plot(s6lat, s6lon, 'ro', markersize=3)
			#-stop 7
			s7lat, s7lon = -15.18,16.98
			xs.append(s7lat)
			ys.append(s7lon)
			ax.plot(s7lat, s7lon, 'ro', markersize=3)
			#-stop 8
			s8lat, s8lon = -13.82,10.52
			xs.append(s8lat)
			ys.append(s8lon)
			ax.plot(s8lat, s8lon, 'go', markersize=3)
			ax.plot(xs,ys,markersize=3,color ='r', label = 'Nightingale')     #this line plots and gives the line a label. 
			#=============================================Raptor Route

		def Route2():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x2s = []
			y2s = []      
			#==========
			s0lat, s0lon = 29.95,63.38
			x2s.append(s0lat)
			y2s.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 27.51,50.87                  
			x2s.append(s1lat)
			y2s.append(s1lon)
			ax.plot(s1lat, s1lon, 'go', markersize=3)
			#-stop 2
			s2lat, s2lon = 24.38,41.8
			x2s.append(s2lat)
			y2s.append(s2lon)
			ax.plot(s2lat, s2lon, 'go', markersize=3)
			#-stop 3
			s3lat, s3lon = 33.14,37.42
			x2s.append(s3lat)
			y2s.append(s3lon)
			ax.plot(s3lat, s3lon, 'go', markersize=3)
			#-stop 4
			s4lat, s4lon = 32.83,26.47
			x2s.append(s4lat)
			y2s.append(s4lon)
			ax.plot(s4lat, s4lon, 'go', markersize=3)
			#-stop 5 
			s5lat, s5lon = 38.14,15.21
			x2s.append(s5lat)
			y2s.append(s5lon)
			ax.plot(s5lat, s5lon, 'go', markersize=3)
			#-stop 6
			s6lat, s6lon = 30.64,-4.497
			x2s.append(s6lat)
			y2s.append(s6lon)
			ax.plot(s6lat, s6lon, 'go', markersize=3)
			#-stop 7
			s7lat, s7lon = 29.07,-14.82
			x2s.append(s7lat)
			y2s.append(s7lon)
			ax.plot(s7lat, s7lon, 'go', markersize=3)
			#-stop 8
			s8lat, s8lon = 22.82,-25.14
			x2s.append(s8lat)
			y2s.append(s8lon)
			ax.plot(s8lat, s8lon, 'go', markersize=3)
			#=====================================legend creation
			ax.plot(x2s,y2s, markersize=3, color = 'g', label='Raptor')
		

		def Route3():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x3s = []
			y3s = []      
			#==========
			s0lat, s0lon =23.76,55.25
			x3s.append(s0lat)
			y3s.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 11.24,51.49                 
			x3s.append(s1lat)
			y3s.append(s1lon)
			ax.plot(s1lat, s1lon, 'go', markersize=3)
			#-stop 2
			s2lat, s2lon = 6.24,52.12
			x3s.append(s2lat)
			y3s.append(s2lon)
			ax.plot(s2lat, s2lon, 'go', markersize=3)
			#-stop 3
			s3lat, s3lon =-0.329,47.43
			x3s.append(s3lat)
			y3s.append(s3lon)
			ax.plot(s3lat, s3lon, 'go', markersize=3)
			#-stop 4
			s4lat, s4lon = 1.548,34.29
			x3s.append(s4lat)
			y3s.append(s4lon)
			ax.plot(s4lat, s4lon, 'go', markersize=3)
			#-stop 5 
			s5lat, s5lon =-6.898, 13.33
			x3s.append(s5lat)
			y3s.append(s5lon)
			ax.plot(s5lat, s5lon, 'go', markersize=3)
			#-stop 6
			s6lat, s6lon = 9.055,7.389
			x3s.append(s6lat)
			y3s.append(s6lon)
			ax.plot(s6lat, s6lon, 'go', markersize=3)
			#-stop 7
			s7lat, s7lon = 14.37,-4.497
			x3s.append(s7lat)
			y3s.append(s7lon)
			ax.plot(s7lat, s7lon, 'go', markersize=3)
		
			#=====================================legend creation
			ax.plot(x3s,y3s, markersize=3, color = 'g', label='Eurasian Spoonbill')

		def Route4():   # this subrotuine is for another bird - the raptor. The same layout is used as the route above. 
			x4s = []
			y4s = []      
			#==========
			s0lat, s0lon =-2.206,53.99
			x4s.append(s0lat)
			y4s.append(s0lon)
			ax.plot(s0lat,s0lon, 'go', markersize=3)
			#-stop 1
			s1lat, s1lon = 3.112,48.36               
			x4s.append(s1lat)
			y4s.append(s1lon)
			ax.plot(s1lat, s1lon, 'go', markersize=3)
			#-stop 2
			s2lat, s2lon = 9.055,47.43
			x4s.append(s2lat)
			y4s.append(s2lon)
			ax.plot(s2lat, s2lon, 'go', markersize=3)
			#-stop 3
			s3lat, s3lon = 8.742,28.35
			x4s.append(s3lat)
			y4s.append(s3lon)
			ax.plot(s3lat, s3lon, 'go', markersize=3)
			#-stop 4
			s4lat, s4lon = 15.31,17.4
			x4s.append(s4lat)
			y4s.append(s4lon)
			ax.plot(s4lat, s4lon, 'go', markersize=3)
			#-stop 5 
			s5lat, s5lon = 18.75,5.825
			x4s.append(s5lat)
			y4s.append(s5lon)
			ax.plot(s5lat, s5lon, 'go', markersize=3)
			#-stop 6
			s6lat, s6lon = 22.82,-6.686
			x4s.append(s6lat)
			y4s.append(s6lon)
			ax.plot(s6lat, s6lon, 'go', markersize=3)
			#-stop 7
			s7lat, s7lon = 20.63, -15.76
			x4s.append(s7lat)
			y4s.append(s7lon)
			ax.plot(s7lat, s7lon, 'go', markersize=3)
			#stop 8
			s8lat, s8lon = 18.75, -26.08
			x4s.append(s8lat)
			y4s.append(s8lon)
			ax.plot(s8lat, s8lon, 'go', markersize=3)
			ax.plot(x4s, y4s, markersize=3,color='g',Label='Barn Swallow')

		global Bird_name                     #This is for the bird name selection. THe user can chose which bird they want to specifically look at. 
		                                     #It looks at the input taken before (the code is further below for the drop down menu) and then plots the route for the bird they picked. 
		if Bird_name=='Nightingale':
			Route1()
		elif Bird_name =='Raptor':
			Route2()
		elif Bird_name == "Eurasian Spoonbill":
			Route3()
		elif Bird_name == "Barn Swallow":
			Route4()
		else:
			print('Error - Internal Problem')
		ax.legend(loc='lower left')
		plt.title('Current Migration Route')
		plt.show() 	
	b1=Button(window, text='Current Bird Route', command=lambda:[choose_graph()]).pack(anchor=N)
	def graph2(): #plotting the temp anomaly time series data
		# Average data across all grid points to create a global average time series.
		filename = "globaltempanomaly.nc"
		data = Dataset(filename)
		temp = data.variables['tmp'][:] 

		#ntimes, nlat, nlon = np.shape(temp)
		#print("The temp array has dimensions: \n"
    	#"Time (number of years x 12 months): {}\n"
    	#"Latitudes: {}\n" 
    	#"Longitudes: {}".format(ntimes, nlat, nlon)
    	#)
		temp_av_1901_2017 = np.mean(temp[:,:,:], axis = 0)

		print ('Debug - No issue with Dataset')
		global_average = np.mean(temp[:,:,:], axis=(1,2))
		annual_temp = np.mean(np.reshape(global_average, (117,12)), axis = 1) # reshape the data into [117,12] as there are 117 years in the dataset,each with 12 months, then calculate the average for each year
		# Calculate the 1961-1990 average
		# the annual temperature is sliced with the indices 60:89 to give the values from 1960 to 1990
		av_1961_1990 = np.mean(annual_temp[60:89])# idk why but the value range wanted needs to be -1 at the end, idk.
		# Calculate the annual anomaly values compared to the 1961-1990 average
		temp_anomaly = annual_temp - av_1961_1990
		# Plot Timeseries - the following code plots the data and labels the axis. 
		plt.figure()
		plt.plot(np.arange(1901,2018,1), temp_anomaly)
		plt.ylim(np.floor(min(temp_anomaly)), np.ceil(max(temp_anomaly))) #this line makes sure that the y axis is large enough to fit all the data points. 
		plt.title("Global Average Temperature Anomaly (1901-2017)")
		plt.xlabel("Years")
		plt.ylabel(u"Difference from 1961-1990 average (\u2103)")
		plt.show()


	l1 = Label(window, text="The button below creates a graph that shows the temperature anomaly").pack(anchor=N)
	b2=Button(window,text='Global Temperature Anomaly',command=graph2).pack(anchor=N)
	def close():
		window.destroy()
	l2 = Label(window, text="").pack(anchor=N)
	b3=Button(window, text='Next -->',command=lambda:[close(), win5()],relief=GROOVE).pack(anchor=S)

#============================window 3
def win3():
	window=Tk()
	window.iconbitmap('icon1.ico')
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')
	l1 = Label(window, text="Use the dropdown menu below to choose the bird. You will model its migratory route").pack(anchor=N)
	def sel_val(event):                                                     #This was the drop down menu mentioned before. THis is where the user picks the bird they want to focus on.                  
		birdname.config(text=clicked.get() +" selected")   #The two options are Nightingale and Raptor. Once the user has press "Select", the bird's name gets stored into a variable for later use
		bname = str(clicked.get())
		#return bname
		global Bird_name
		Bird_name = bname
		b1.pack(anchor=S)

	options=["Nightingale","Raptor", "Eurasian Spoonbill", "Barn Swallow"]  # These are the options for the drop down menu

	clicked=StringVar()
	#clicked.set("Choose Bird") #This just presets the drop down box selection to the first value in the array above (Nightingale)
	birdname=Label(window)
	birdname.pack(anchor=S)

	dropdown=ttk.Combobox(window,textvariable=clicked, value=options,state="readonly") # THis line enables for the drop down menu to work.
	dropdown.current(0)
	dropdown.bind("<<ComboboxSelected>>", sel_val)
	dropdown.pack()
	b1= Button(window, text='Select', command=lambda:[print(Bird_name),window.destroy(),win4()],relief=GROOVE)
	#b1= Button(window, text='Select', command=lambda:[print(Bird_name),window.destroy(),win4()],relief=GROOVE).pack(anchor=S)
	#b2=Button(window, text='Save your Choice', command=save_val).pack()

#========================window 2
def win2():
	start_window.destroy()
	window = Tk()
	window.iconbitmap('icon1.ico')
	window.title('CO2 Level Input')
	height = 550
	width = 550
	s_width=window.winfo_screenwidth()
	s_height=window.winfo_screenheight()
	x_coord=(s_width/2)-(width/2)
	y_coord=(s_height/2)-(height/2)
	window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
	window.title('Bird Migration Investigation')

	#THe following code is for the slider for the user to input their CO2 values. 
	label1=Label(window, text='Chose a value for Global CO2 emissions to model the data.\n\nAs a reference, in 2016, the global CO2 output was 35 Billion Tonnes \n\n Pick a value (in billions)Press ""select value"" and then ""close"', relief='flat').pack(anchor=N)
	v=DoubleVar() #this value is the value that moves with the slider and shows the value that the slider is currently on. 
	slider=Scale(window, variable=v, from_=25, to=50, resolution=1, orient=HORIZONTAL).pack(anchor=N) # this line sets the limits and configures the slider.
	def select(): #relaying the chosen value to the file
		val_dis.config(text = str(v.get())+ " billion tonnes of CO2") #This line confirms to the user of their selection. It writes the value of the variable "v" with "Billion tonnes of CO2" "on the end.
	def Save_val():                          #This subroutine saves the value to a text file for later use. 
		with open("value.txt",'w') as f:
			val = str(v.get()*1000000000)
			print(val, file = f)
			f.close()
		#window.destroy()

	def show_buttons():
		global Buttons
		global SaveVal
		global Closewin1
		if Buttons == False:
			Buttons=True
			SaveVal=Button(window,text='Save Value',command=Save_val, relief=GROOVE)
			SaveVal.pack(anchor=S)
			def close():
				window.destroy()
			Closewin1=Button(window,text='Next -->',command=lambda:[close(),win3()], relief=GROOVE)
			Closewin1.pack(anchor=SE)
		else:
			SaveVal.destroy()
			Closewin1.destroy()
			Buttons=False
			show_buttons()

	Choose_value=Button(window, text='Select Value', command=lambda:[select(),show_buttons()]).pack(anchor=N)
	val_dis=Label(window)
	val_dis.pack()



##################################### MAIN CODE #########################################
#====================window 1 - this is the first window that pops up. It's just a starting screen. 
start_window = Tk()
start_window.iconbitmap('icon1.ico')
width = 550
height = 550
s_width=start_window.winfo_screenwidth()
s_height=start_window.winfo_screenheight()
x_coord=(s_width/2)-(width/2)
y_coord=(s_height/2)-(height/2)
start_window.geometry(f'{width}x{height}+{int(x_coord)}+{int(y_coord)}')
start_window.title('Bird Migration Investigation')
l1 = Label(start_window,text='Bird Migration Investigation\n\nPress Next To Start')
l1.pack()
b1 = Button(start_window, text='Next -->', command=win2, relief=GROOVE).pack()
l2 = Label(start_window,text="\n").pack()
#get the image
my_img = Image.open("win1.jpg")
#resize it
resizedimg = my_img.resize((450,375),Image.ANTIALIAS)
#make the resized image a varible 
new_img = ImageTk.PhotoImage(resizedimg)
#apply the new image
my_label = Label(start_window, image=new_img)
my_label.pack(anchor=S)

mainloop()

#========== this bit of code retrieves the CO2 val and makes it a global var)
with open("value.txt", 'r') as f:
	CO2 = f.read()
	f_value.close()
