#!/usr/bin/python3

import subprocess
import datetime
#pip install mysql-connector-python
import mysql.connector
import time

from mysql.connector.connection import MySQLConnection

def SaveMySQL():

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  auth_plugin='mysql_native_password',
  database="rlstech",
  collation='utf8mb4_unicode_ci',
  password="JmR677677#"
)
  mycursor = mydb.cursor()
  sql = "INSERT INTO failed (message) VALUES ('"+str(failedstr)+"')"
  mycursor.execute(sql)
  mydb.commit()

def Security():
    print(d)
    #awk 'match($6,/Failed/) -F { print $1, $2, $3,$6,$9,$11,$12,$13}' /var/log/auth.log
    a = subprocess.Popen(["awk",'match($6,/Failed/) && /'+d+'/ -F { print $1, $2, $3,$6,$7,$9,$11,$12,$13,$14,$15;exit;}',"/var/log/auth.log"],
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
        #d="Mar  1 22:07:55"

        with open('checked.txt','w') as file:
           file.write('Checked the log file for failed messages. at '+d)
           failed = Security()
        if (failed):
            with open('Failed.txt','a+') as File:
                failedstr = str(failed,'UTF-8')
                # failedstr=failedstr.replace("b'","")
                # failedstr=failedstr.replace("'","")
                print(failedstr)
                SaveMySQL()
                #os.system('mail -s "You have an intuder at richard@richard-Thinkcentre-M77" rchrdperreault@gmail.com')
                #subprocess.call(['/home/richard/sendmail.sh', "You have an intruder at richard@richard-Thinkcentre-M77",failed])
