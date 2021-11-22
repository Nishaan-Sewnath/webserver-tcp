from flask import Flask, send_file, render_template
import socket
import sys
from datetime import datetime
import time
import threading


lines = ''
log = open("/usr/src/app/sensorlog.csv","w")
log.close()
log = []

HOST = None  # Symbolic name meaning all available interfaces
PORT = 1078  # Arbitrary non-privileged port
BUFF = 1024
s = None
conn = None
command = None
Exit = False


app = Flask(__name__)

#validates the data sent and received are the same
def readMessage(message):
    try:
        if (int(message[1:6]) == len(message[6:])):
            return [message[0],message[1:6],message[6:]]
        else:
            return False
    except:
        return False

def CreateMessage(header, message):
    return (header + "{:<5}".format(len(message)) + message)

#get html info from temp folder in server src
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('root.html')

#Sends message to the client to turn on the sensors
@app.route('/Sensor_On')
def Sensor_On():
    global conn
    message = CreateMessage("S","Turn ON")
    conn.send(message.encode())
    

#Downloads the logs
@app.route('/Log_Download')
def download_file():
    #Path of sensorlog file
    path = "/usr/src/app/sensorlog.csv"

    #Return file as downloadable attachment
    return send_file(path,as_attachment=True)

#Sends message to the client to turn off the sensors
@app.route('/Sensor_Off')
def Sensor_Off():
    global conn
    message = CreateMessage("S","Turn OFF")
    conn.send(message.encode())
    

#Sends message to the client to get the currnet status of the sensors
@app.route('/Status')
def Status():
    global conn
    message = CreateMessage("S","Status")
    conn.send(message.encode())
    

#checks the last few readings of the sensors
@app.route('/Check')
def check():
    global log
    print('Checking the logs: ')
    lines = ''
    #Loop through log list, adding each to new line of 'data'
    for a in log:
        lines = lines + "Light level: " + a[0] + " | Temperature: " + a[1] + \
            " | Taken on: " + a[2] + " at " + a[3] + "<br>"
    #print all logs in formatted block
    return lines

#Sends message to the client that the server will terminate
@app.route('/Exit')
def Exit():
    global conn, Exit
    Exit = True
    message = CreateMessage("S","Exit")
    conn.send(message.encode())
    print('Client has left')
    quit()


#thread that processes the data
def threads():
    global conn, log
    while(True):
        data = conn.recv(BUFF)
        data = readMessage(data.decode())            
        
        if (data == False):
            print("Message sent was corrupted")
            continue
        try:
            command = data[0]
            if command == 'S':
                msg = data[2].split("#")
                print(msg)
                if(not msg[1][len(msg[1])-1].isdigit()): 
                    msg[1] = msg[1][0:len(msg[1])-1]
                    #if array full, remove oldest entry
                x = [msg[0],msg[1],datetime.now().date().strftime("%d:%m:%y"),str(datetime.now().time())[0:8]]
                log.append(x)
                if len(log) == 11:
                    log.pop(0)
                logfile = open("/usr/src/app/sensorlog.csv","a")
                logfile.write(x[0]+","+x[1]+","+x[2]+","+x[3]+"\n")
                logfile.close()

            elif command == 'M':
                print(data[2])
            else:
                print("Error")
                print(data)

        except:
            print("Error with read in")

        time.sleep(1) 

def main():
    global s, conn

    #recevies the info about the client to connect, and returns error messages if the connection fails
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind((sa))
            
            s.listen(1)
        except OSError as msg:
            print('Didnt bind')
            s.close()
            s = None
            continue
        break

    if s is None:
        
        print('could not open socket')
        sys.exit(1)
        
    else:
        print('socket connected!')

    conn, addr = s.accept()

    conn.send(CreateMessage('M','Welcome to the server').encode())
    
    print('Connected by', addr)

    #creates and starts the threads
    thread = threading.Thread(target=threads)
    thread.daemon = True
    thread.start()
    while True:
        time.sleep(5)
        
if __name__ == '__main__':

    threadMain = threading.Thread(target=main)
    threadMain.daemon = True
    threadMain.start()
    app.run(host='0.0.0.0', port=80)
