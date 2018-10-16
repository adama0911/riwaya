import threading
import sys
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

import warime

FILE_FOLD= "./files_fold/"
REQUESTS_FOLD= FILE_FOLD + "requests_fold/"
RESPONCES_FOLD= FILE_FOLD + "responses_fold/"
HANDLE_FOLD= FILE_FOLD + "handle_fold/"
RESPONSES_HANDLE_FOLD= FILE_FOLD + "responses_handle_fold/"
NEXT_PRIORITY_REAUEST_FILE= FILE_FOLD + "./nextPriorityRequestFile.txt"
NEXT_REAUEST_FILE= FILE_FOLD + "./nextRequestFile.txt"
LOGS_FOLD= "./logs/"

BROWSER_BIN_PATH = '/usr/bin/firefox'
WEBSIT_URL  =   "https://www.warime.com/callmoney/checking.zul"

# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.

#os.environ['MOZ_HEADLESS'] = '1'

# Select your Firefox binary.
binary = FirefoxBinary(BROWSER_BIN_PATH, log_file=sys.stdout)

# Start selenium with the configured binary.
driver = webdriver.Firefox(firefox_binary=binary)

driver.get(WEBSIT_URL)
"""class Task(threading.Thread):
    def __init__(self,opp):
        threading.Thread.__init__(self)"""
class Task():
    def __init__(self,opp):
        self.opp = opp
        self.fileName= ""
        self.request= ""
        self.response= ""
        self.requesthandl= ""
        self.responsehandle= ""
        self.fileReponseRetrait=""

    def getNextPriorityFileName(self):
        try:
            with open(NEXT_PRIORITY_REAUEST_FILE,'r') as iostream:
                num = int(iostream.read())
                name = str(num) + '.txt'
                iostream.close() 
                self.fileName = name  
                print(self.fileName)             
                return name
        except IOError as e:
            print("opening next request file failed ")
            print ("I/O error({0}): {1}"+ format(e.errno, e.strerror))
            return 1

    def getNextFileName(self):
        try:
            with open(NEXT_REAUEST_FILE,'r') as iostream:
                num = int(iostream.read())
                name = str(num) + '.txt'
                iostream.close() 
                self.fileName = name               
                return name
        except IOError as e:
            print("opening next request file failed ")
            print ("I/O error({0}): {1}"+ format(e.errno, e.strerror))
            return 1

    def getNextRequest(self, fileName):
        try:
            if os.path.exists(REQUESTS_FOLD + fileName):
                with open(REQUESTS_FOLD + fileName,'r') as iostream_request:
                    request = iostream_request.read()
                    print(REQUESTS_FOLD + fileName)
                    print(request)
                    iostream_request.close()
                    with open(NEXT_REAUEST_FILE,'w') as iostream_next_request:
                        number = int((fileName.split('.'))[0]) + 1
                        iostream_next_request.write(str(number))
                        iostream_next_request.close()
                        return request
            elif IOError:
                print ("request no found "+str(fileName))
                return 1
                
        except IOError as e:            
            print ("I/O error({0}): {1}"+ format(e.errno, e.strerror))
            return 1

    def requestPriorityProcessing(self,request,benefInfoSup):

        number = int(((self.fileName).split('.'))[0])
        print(benefInfoSup)
        warime.retirerSuite(self.opp,request,number,benefInfoSup)
        self.setResponse(self.fileReponseRetrait)

    def requestProcessing(self, request):
        print(request)
        req = request.split('[')
        operation = int(req[0])
        print(req)
        if operation==1:
            print("Envoi processing ....")
            resp = warime.envoiyer(self.opp,req,operation)
            print(self.opp.response)
            self.setResponse(self.fileName)

        elif operation==2:
            print("Retrait processing....")
            number = int(((self.fileName).split('.'))[0])
            warime.retirer(self.opp,req,number)
            self.setRequestHandle()


    def setResponse(self,fileReponse):
        try:
            with open(RESPONCES_FOLD + fileReponse ,'w') as iostream:
                iostream.write(str(self.opp.response))
                iostream.close()
                return 0                
        except IOError as e:
            print("opening next request file failed ")
            print ("I/O error({0}): {1}"+ format(e.errno, e.strerror))
            return 1

    def setRequestHandle(self):
        try:
            with open(HANDLE_FOLD + self.fileName ,'w') as iostream:
                iostream.write(str(self.opp.requesthandle))
                iostream.close()
                return 0              
        except IOError as e:
            print("opening next request file failed ")
            print ("I/O error({0}): {1}"+ format(e.errno, e.strerror))
            return 1

    def getHandleResponse(self):
        if os.path.exists(RESPONSES_HANDLE_FOLD + self.fileName):
            try:
                with open(RESPONSES_HANDLE_FOLD + self.fileName ,'r+') as iostream:
                    resp = iostream.readline()
                    iostream.close()

                    tab = resp.split(']')

                    req = tab[1].split("[")

                    spl = tab[0].split("[")

                    self.fileReponseRetrait= req[4]

                    typePiece = spl[0]
                    numPiece  = spl[1]
                    pays      = spl[2]
                    datedelivrance    = spl[3]
                    datevalidite = ((spl[4]).split('\\'))[0]

                    with open(NEXT_PRIORITY_REAUEST_FILE,'w') as iostream_next_request:
                        number = int((self.fileName.split('.'))[0]) + 1
                        iostream_next_request.write(str(number))
                        iostream_next_request.close()
                        return [spl,req]
            except IOError as e:
                print("opening next request file failed ")
                return 1 
        elif IOError:
                print ("request no found "+str(self.fileName))
                return 1  

    def run(self):
        nextPriorityFile = self.getNextPriorityFileName()
        if  nextPriorityFile != 1:
            cont = self.getHandleResponse()
            if cont != 1:
                benefInfoSup = cont[0]
                req = cont[1]
                self.requestPriorityProcessing(req,benefInfoSup)
            elif cont == 1:
                nextFile = self.getNextFileName()
                if(nextFile != 1):
                    req = self.getNextRequest(nextFile)
                    if(req!=1):
                        self.requestProcessing(req)


if __name__=="__main__":
    
    driver  = warime.connexion(driver)
    if driver!=1:
        while 1:     
            opp = warime.Operations(driver)
            task = Task(opp)
            task.run()