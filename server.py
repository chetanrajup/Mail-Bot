import socket
import threading
import json
import os
import smtplib
import sys
import email,ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


FORMAT = "utf-8"
PORT = 5050
SERVER = "127.0.0.1"

ADDR = (SERVER,PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_dir(usn,conn):
    path = "C:/SEM 4/SOCKET PROGRAMMING/CLOUD_FILES/" + usn
    dir_list = os.listdir(path)
    dir_list = str(dir_list)
    conn.send(dir_list.encode(FORMAT))

def send_email(recvID ,subject, body ):
    try:
        sender_email = "AppraiserSEproject@gmail.com"
        password = "jshtnqlejhtydejk" 
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls() #secure transport layer
        server.login(sender_email, password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender_email,recvID, message) #sendmail is a inbuilt fn
        return "MS" #mail successful
    except Exception as e:
        print(e)
        return "MNS"


def send_attach(subj,bdy,recvID,flname):
    try:
        sender_email = "AppraiserSEproject@gmail.com"
        password = "jshtnqlejhtydejk" 

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recvID
        message["Subject"] = subj
        
        # Add body to email
        message.attach(MIMEText(bdy, "plain"))

        # Open PDF file in binary mode
        with open(flname, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream") 
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {flname}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recvID, text)
            return "MS"
    except:
        return "MNS"

def handle_client_request(conn,addr,username):
    msg = conn.recv(1024).decode(FORMAT)
    if (msg == 'A'):
        
        msg6 = conn.recv(1024).decode(FORMAT)
        if ( msg6 == "Aa"):
            msgml = conn.recv(4096).decode(FORMAT)
            (recvID,subj,bdy) = msgml.split(":")
            resml = send_email(recvID,subj,bdy)
            conn.send(resml.encode("utf-8"))
        else:
            send_dir(username,conn)
            msgml4 = conn.recv(4096).decode(FORMAT)
            (recvID1,cap1,bdy1,flname1) = msgml4.split(":")
            resmla2 = send_attach(cap1,bdy1,recvID1,flname1)
            conn.send(resmla2.encode("utf-8"))
        handle_client_request(conn,addr,username)

        
        

    elif (msg == 'B'):
        send_dir(username,conn)
        msgml1 = conn.recv(4096).decode(FORMAT)
        (myID,cap,bdy,flname) = msgml1.split(":")
        resmla = send_attach(cap,bdy,myID,flname)
        conn.send(resmla.encode("utf-8"))
        handle_client_request(conn,addr,username)



    if (msg == 'C'):
        # dir_name = username
        path = "C:/SEM 4/SOCKET PROGRAMMING/CLOUD_FILES/" + username + "/"
        #print(path)
        file_name = conn.recv(1024).decode(FORMAT)
        #print(file_name)
        file_size = conn.recv(1024).decode(FORMAT)

        with open(path + file_name ,"wb") as file:
            c = 0
            while c < int(file_size):
                data = conn.recv(1024)
                if not (data):
                    break
                file.write(data)
                c += len(data)
        print("File recieved successfully from ",addr)
        handle_client_request(conn,addr,username)

        
        
    if (msg == 'D'):
        send_dir(username,conn)
        handle_client_request(conn,addr,username)

        
    if (msg == 'E'):
        send_dir(username,conn)
        file = conn.recv(1024).decode(FORMAT)
        path = "C:/SEM 4/SOCKET PROGRAMMING/CLOUD_FILES/" + username + "/" + file
        os.remove(path) # file doesnt exist case not handeled 
        print("file from",addr,"got deleted")
        handle_client_request(conn,addr,username)

        
    if (msg == 'F'):
        conn.close()
        print(f'[DISCONNECTED]...... user with ip {addr} disconnected')
        sys.exit()
        # server.quit()......find other way to quit server
        

def handle_client_auth(msg):
    res=''
    with open('data.json') as json_file:
        data = json.load(json_file)
        (choosen,username,password) = msg.split(":")
        if(choosen == "1"):
            if(username in data and data[username]['password'] == password):
                res = "LS"
            elif(username in data):
                res = "LU"
            elif(username not in data):
                res = "UD"
        elif(choosen == "2"):
            if(username not in data):
                data[username]={
                    'password':password
                }
                with open('data.json','w') as ofile:
                    json.dump(data,ofile)
                res = "RS"
            else:
                res = "RU"
        return res


def handle_client(conn,addr):
    print(f"[New connection from]... {addr}")
    connected = True

    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if not msg:
            break 
        
        if (msg=="T"):
            conn.close()
            print(f'[DISCONNECTED]...... user with ip {addr} disconnected')
            # server.quit()
            return 
        else:
            res = handle_client_auth(msg)
            conn.send(res.encode("utf-8"))
            (choosen,username,password) = msg.split(":")
            if(res=="RS"):
                path = "C:/SEM 4/SOCKET PROGRAMMING/CLOUD_FILES/" + username
                os.mkdir(path)
            if (res=="LS" or res == "RS"):
                handle_client_request(conn,addr,username)
     
def start():
    server.listen()
    print(f'[LISTENING]... server listening on {SERVER}')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target= handle_client, args = (conn,addr))
        thread.start()

print("[STARTING]...starting server")
start()