#from distutils.log import error
import socket
import sys
from getpass import getpass
import os


PORT = 5050
FORMAT= 'utf-8'
SERVER =   "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def ui3():
    print(' ---------------- ')
    print('| 1 :- SEND TEXT | ')
    print('| 2 :- SEND FILE | ')
    print(' ---------------- ')

    choice = int(input('Enter your choice:- '))
    if (choice == 1):
        msg = "Aa"
        client.send(msg.encode(FORMAT))
        recvID = input("enter the receivers gmail id :- ")
        subj   = input("enter the subject of mail    :- ")
        bdy    = input("enter the body of the mail   :- ")
        msg2 = recvID + ":" + subj + ":" + bdy
        client.send(msg2.encode(FORMAT))
        resmlc=client.recv(1024).decode(FORMAT)
        if (resmlc == "MS"):
            print("mail successfully SENT")
            ui2()
        else:
            print("there was some error pls try again")
            ui2()
    elif (choice == 2):
        msg = "Ab"
        client.send(msg.encode(FORMAT))
        recvID = input("enter the receivers gmail id :- ")
        subj   = input("enter the subject of mail    :- ")
        bdy    = input("enter the body of the mail   :- ")
        print("set of files in ur dir")
        dir_list = client.recv(1024).decode(FORMAT)
        print(dir_list)
        flname = input("enter the the name of the file :- ")
        msg3 = recvID + ":" + subj + ":" + bdy + ":" + flname
        client.send(msg3.encode(FORMAT))
        resmlc1=client.recv(1024).decode(FORMAT)
        if (resmlc1 == "MS"):
            print("mail successfully sent")
            ui2()
        else:
            print("there was some error pls try again")
            ui2()

    else:
        print("INVALID CHOICE")
        ui3()

def ui2():
        print(' -------------------  ')
        print('| 1 :- SEND MAIL    | ')
        print('| 2 :- GET MAIL     | ') 
        print('| 3 :- SEND FILES   | ')
        print('| 4 :- VIEW FILES   | ')
        print('| 5 :- DELETE FILES | ')
        print('| 6 :- LOG OUT      | ')
        print(' -------------------  ')
        choice = int(input('Enter your choice:- '))

        if(choice == 1):
            msg = "A"
            client.send(msg.encode(FORMAT))
            ui3()
        elif(choice == 2):
            msg = "B"
            client.send(msg.encode(FORMAT))
            myID =   input("enter ur gmail id :- ")
            bdy   = input("enter the body of mail :- ")
            cap    = input("enter caption for the mail :- ") #subj
            print("set of files in ur dir")
            dir_list = client.recv(1024).decode(FORMAT)
            print(dir_list)
            flname = input("enter the file name :- ")

            msg3 = myID + ":" + cap + ":" + bdy + ":" + flname
            client.send(msg3.encode(FORMAT))
            resmlc1=client.recv(1024).decode(FORMAT)
            if (resmlc1 == "MS"):
                print("mail successfully sent")
                ui2()
            else:
                print("there was some error pls try again")
                ui2()
            


        elif(choice == 3):
            msg = "C"
            client.send(msg.encode(FORMAT))
            path1 = input("Enter path: ")
            file_name = input("File name: ")
            dir_list= os.listdir(path1)

            if file_name not in dir_list:
                print("Invalid file name")

            if file_name in dir_list:
                size = os.path.getsize(file_name)
                file_size = str(size)
                client.send(file_name.encode(FORMAT))
                client.send(file_size.encode(FORMAT))

                with open(file_name,"rb") as file:
                    #if (FileNotFoundError):
                        #print("File not Found")
                    c = 0
                    while c < int(file_size):
                        data = file.read(1024)
                        if not (data):
                            break
                        client.sendall(data)
                        c += len(data) 
                print("File transfered successfully")
                ui2()
            ui2()

        elif(choice == 4):
            msg = "D"
            client.send(msg.encode(FORMAT))
            dir_list = client.recv(1024).decode(FORMAT)
            print(dir_list)
            ui2()
            
        
        
        elif(choice == 5): # NOT WORKING
            msg = "E"
            client.send(msg.encode(FORMAT))
            dir_list = client.recv(1024).decode(FORMAT)
            print("list of files in dir")
            print(dir_list)
            file_name = input("type the filename to delete :- ")
            client.send(file_name.encode(FORMAT))
            print("file successfully deleted")
            ui2()
            
        
        
        elif(choice == 6):
            msg="F"
            client.send(msg.encode(FORMAT))
            print("successfully logged out")
            sys.exit()
        
        else:
            print("INVALID CHOICE")
            ui2()

def ui():
    while(True):
        print(' --------------- ')
        print('| 1 :- LOGIN    | ')
        print('| 2 :- REGISTER | ')
        print('| 3 :- EXIT     | ')
        print(' --------------- ')
        choice = int(input('Enter your choice:- '))
        if(choice == 1 or choice == 2):
            usn =  input ('Enter your username:- ')
            # pswd = getpass('Enter your password:-  ')
            pswd = input('Enter your password:-  ')
            if (choice == 1):
                msg = "1:"+ usn + ":" + pswd
            else:
                msg = "2:"+ usn + ":" + pswd
            client.send(msg.encode(FORMAT)) 
            result=client.recv(1024).decode(FORMAT)
            if (result == "RS"): # reg successful 
                print("registration successful ")
                ui2()
            elif (result == "RU"):  #reg unsuccessful 
                print("user already exist pls try loggin in or username might be taken ")
                ui()
            elif (result == "LS"):  #login successful
                print("successfully logged in ")
                ui2()
            elif (result == "UD"):
                print("Username doesnt exists")
                ui()
            else:                #login unsuccessful
                print(" unable to login pls try again")
                ui()
        elif(choice == 3):
            msgt="T"
            client.send(msgt.encode(FORMAT))
            print('CONNECTION TERMINATED')
            sys.exit()
        else: 
            print('INVALID CHOICE')
            ui()
ui()