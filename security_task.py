#!/usr/bin/python3

import subprocess
import datetime
import mysql.connector
#pip install mysql-connector-python-rf

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  auth_plugin='mysql_native_password',
  database="rlstech",
  collation='utf8mb4_unicode_ci',
  password="JmR677677#"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS failed (ID INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))")

#d = datetime.datetime.now()
from datetime import datetime, timedelta
#take off a minute
d = datetime.today() - timedelta(hours=0, minutes=1)
d = d.strftime("%b %d %H:%M")
#d="Nov 10 19:17"


def Security():
    print(d)
    a = subprocess.Popen(["awk",'match($6,/Failed/) && /'+d+'/ -F { print $1, $2, $3,$6,$9,$11,$12,$13;exit;}',"/var/log/auth.log"],
    #a = subprocess.Popen(["awk",'/": Failed"/ && /'+d+'/ -F { print $1, $2, $3,$6,$11,$12,$13;exit;}',"/var/log/auth.log"],
    stdout = subprocess.PIPE)
    #output = str(a.communicate())
    output = a.stdout.read().strip()
    txt=output.decode()
    #outputlist.append(output)
    return txt

if __name__ == '__main__':

    with open('checked.txt','w+') as file:
     file.write('Checked the log file for failed messages. at '+d)
    failed = Security()
    if (failed):
        with open('Failed.txt','a+') as File:
            failedstr = str(failed)
            #failedstr=failedstr.replace("b'","")
            #failedstr=failedstr.replace("'","")
            File.write(str(failedstr+"\n"))
            print(failedstr)
            mycursor = mydb.cursor()
            sql = "INSERT INTO failed (message) VALUES ('"+str(failedstr)+"')"
            mycursor.execute(sql)
            mydb.commit()
            #os.system('mail -s "You have an intuder at richard@richard-Thinkcentre-M77" rchrdperreault@gmail.com')
            subprocess.call(['sendmail.sh', "You have an intruder at richard@richard-Thinkcentre-M77",failed])
    
