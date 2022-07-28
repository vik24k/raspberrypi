""" 
The idea:  Imagine, you are outdoor, maybe in holiday and you want to ssh into your raspberry at home but you can't since your house modem's ip-addess
has changed. This script is a simple solution for users who have a raspberry pi at home turned on 24/7 and no possiblity to set a static public ip address
since the ISP does not let you do it (trust me, it's not so rare).   

The logic: the script will retrieve your public ip address and check if it is the same one written in the .txt file, if that's the case it will just exit 
(the ip has remained the same),if the content does not match instead it will notify your email with the new ip address and then update the .txt file with it.

Suggestion: 
set a cronjob running this script every 2-3 minutes.

BEFORE RUNNING THE SCRIPT!!!

create a new gmail account that will be controlled by te raspberry
add 2 steps auth
set a specific 16 chars password for apps (google it to discover how to do it)

create a .txt file in your raspberry and write inside it your pubic ip address to start, then modify the script here below inserting the right path of the file at the right place
replace the fake credentials here below with your real ones.
"""

import subprocess
import os
import requests
import smtplib
import ssl
from email.message import EmailMessage


def GetIp():
   return requests.get('https://api.ipify.org').content.decode("utf-8")


def NotifyChange(NewIp, OldIp):

   print("ip has changed... notifying {}...".format(EmailAddress))

   sender = "pi-controlledgmail.address@gmail.com"
   passwd = "passwordforpigmailaccount"
   receiver = "address.tonotify@gmail.com"
   subject = "Il tuo indirizzo ip pubblico è cambiato!"
   body = """hi, your Pi here, just wanna tell you that your house ip has changed from {} to {}""".format(OldIp, NewIp)

   em = EmailMessage()
   em['From'] = sender
   em['To'] = receiver
   em['Subject'] = subject
   em.set_content(body)
   
   context = ssl.create_default_context()
   with(smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)) as smtp:
      smtp.login(sender, passwd)
      smtp.sendmail(sender, receiver, em.as_string())

def WriteNewIp(new_ip):
   with open('/your/txt/file/path/currentip.txt', 'r') as fin:
      data = fin.read().splitlines(True)
   with open('/your/txt/file/path/currentip.txt', 'w') as fout:
      fout.writelines(data[1:])
      fout.write(new_ip)
   print("txt file updated")

def main():
   
   new_ip = GetIp()
   with open("/your/txt/file/path/currentip.txt", "r+") as f:
      previous_ip = f.readline().strip("\n")
      if(previous_ip==new_ip):
         print("ip has not changed.. quitting...")
         exit()
      else:
         NotifyChange(new_ip, previous_ip)
         WriteNewIp(new_ip)
        
if __name__=="__main__":
  main()
