#!/usr/bin/python3

import subprocess
import datetime
from sys import stdout
import mysql.connector
import time

import sqlite3

con = sqlite3.connect('failed.db')

con.execute('''CREATE TABLE IF NOT EXISTS failed (ID INTEGER AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))''')

con.commit()
con.close()

def SaveMySQL(failedstr):
   con = sqlite3.connect('failed.db')
   con.execute("INSERT INTO failed (message) VALUES ('"+str(failedstr)+"')")
   con.commit()
   con.close()

def Security():
    print(d)
    a = subprocess.Popen(["awk",'match($6,/Failed/) && /'+d+'/ -F { print $1, $2, $3,$6,$9,$11,$12,$13;exit;}',"/var/log/auth.log"],
    #a = subprocess.Popen(["awk",'/": Failed"/ && /'+d+'/ -F { print $1, $2, $3,$6,$11,$12,$13;exit;}',"/var/log/auth.log"],
    stdout = subprocess.PIPE)
    #output = str(a.communicate())
    output = a.stdout.read().strip()
    #outputlist.append(output)
    return output

if __name__ == '__main__':

    while True:
        #d = datetime.datetime.now()
        from datetime import datetime, timedelta
        #take off a minute
        global d
        d = datetime.today() - timedelta(hours=0, minutes=0)
        t = datetime.today() - timedelta(hours=0, minutes=0)
        d = d.strftime("%b %d")
        t = t.strftime("%H:%M:%S")
        day = ('01','02','03','04','05','06','07','08','09')
        for daystr in day:
         if d.find(daystr) !=-1:
          d=d.replace('0',' ')
        d=d+' '+t
        time.sleep(1)
        #d="Dec 23 05:21:03"

        with open('checked.txt','w+') as file:
         #  file.write('Checked the log file for failed messages. at '+d)
           failed = Security()
        if (failed):
            with open('Failed.txt','a+') as File:
                failedstr = str(failed)
                failedstr=failedstr.replace("b'","")
                failedstr=failedstr.replace("'","")
                File.write(str(failedstr+"\n"))
                print(failedstr)
                SaveMySQL(failedstr)
                #os.system('mail -s "You have an intuder at richard@richard-Thinkcentre-M77" rchrdperreault@gmail.com')
                #subprocess.call(['/home/richard/sendmail.sh', "You have an intruder at richard@richard-Thinkcentre-M77",failed])
                #echo $failed | mail -s 'You have an intruder at richard@richard-Thinkcentre-M77' rchrdperreault@gmail.com
                p1 = subprocess.Popen(["echo", failed],
                stdout=subprocess.PIPE)
                output = subprocess.check_output(('mail',"-s 'You have an intruder at richard@richard-Thinkcentre-M77'","rchrdperreault@gmail.com"), stdin=p1.stdout)   