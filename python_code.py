import gspread
from oauth2client.service_account import ServiceAccountCredentials

import serial
import time

import email_conf
from boltiot import Email, Bolt
import json, time

mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)  #email_conf text file has API key and other confidential data of BOLT module.

# how we interact with our data in Google Sheets
scope=["https://spreadsheets.google.com/feeds",\
"https://www.googleapis.com/auth/spreadsheets",\
"https://www.googleapis.com/auth/drive.file",\
"https://www.googleapis.com/auth/drive"]

#creating client to interact with Google Sheets
credentials=ServiceAccountCredentials.\
from_json_keyfile_name("credentials.json",scope)   #credentials.json file has confidential information for accessing data from our google sheets
client=gspread.authorize(credentials)
sheet=client.open("project1").sheet1

#function for sending mail
def mail_func(email_id):
	mailer = Email(email_conf.MAILGUN_API_KEY, \
	email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_id)
	try:
		print("Making request to Mailgun to send an email")
		response = mailer.send_email("You got a Reward",\
		"Thank you for your valuable contribution in recycling the plastic and making incredible india clean and pollution free.")
		response_text = json.loads(response.text)
		print("Response received from Mailgun is: " + \
		str(response_text['message']))
	except Exception as e: 
       		print ("Error occured: Below are the details")
       		print (e)

#function to send data to Arduino and to get data from arduino
def ard_func():
	i=0
	ard_data=list()
	while(i<3):
		ArduinoSerial=serial.Serial('/dev/ttyACM0',9600)	#activating USB port for sending data
		time.sleep(3)
		ArduinoSerial.write(b'1')
		time.sleep(3)
		ard_data.append(ArduinoSerial.readline())	#reading data sent by arduino
		i=i+1
	print(ard_data)
	mail_trigger=0
	for i in range(0,2,1):			#checking data which has data determing whether thrown one is bottle or not
		if(ard_data[i]==b'11\r\n'):
			mail_trigger=1
			break
	return mail_trigger

for i in range(45,10000,1):
		cello1=sheet.cell(i,2).value
		leng1=len(cello1)
		if(leng1==0):
			i=i+1
		elif(leng1>0):
			j=i+1
			print(i)
			print("entered mail : ",cello1)
			break

while(True):
	while(10000):		#checking whether email is entered or not
		cello2=sheet.cell(j,2).value
		leng2=len(cello2)
		if(leng2==0):
			j=j
		else:
			j=j+1
			break
	print(j-1)
	print("entered mail :",cello2)
	mail_trig_from_func=ard_func()
	if(mail_trig_from_func==1):
		mail_func(cello2)
	else:
		print("not a bottle")
	
	

