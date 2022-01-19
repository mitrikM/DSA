import sys
import os
from PyQt5.QtWidgets import QMainWindow ,QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
from PyQt5 import QtGui, uic, QtCore

import hashlib
import sympy
import random
import math 
from zipfile import ZipFile
from os.path import basename

qtCreatorFile = "kryptoUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    return (str1.join(s))

class MyApp(QMainWindow, Ui_MainWindow):
 
        

    
    def getKeys(self):
        minNum= 10000000000
        maxNum= 99999999999
        p = sympy.randprime(minNum,maxNum)
        q= sympy.randprime(minNum,maxNum)
        
        while p==q:
            q= sympy.randprime(minNum,maxNum)
            
        n=p*q
        
        totient= (p-1)*(q-1)
        
        e= random.randint(1, n)
        
        while math.gcd(e,totient) !=1:
            e= random.randint(1, n)
        
        d= pow(e,-1,totient)
        publicKey= str(e)+" "+str(n)
        privateKey=str(d)+" "+str(n)

        
        
        
        
        f=open("kluc.priv","w+")
        f.write(privateKey)
        f.close()
        
        g=open("kluc.pub","w+")
        g.write(publicKey)
        g.close()
        
        self.label_2.setText("kluce vygenerovane")


        
        
    def podpis(self):
        #vyber suboru a jeho hashovanie
        Response =QFileDialog.getOpenFileName(
            parent=self,
            caption="Vyber Súbor ktory chces podpisat",
            directory=os.getcwd(),
            filter=None,
            )
        cesta=Response[0]
        with open(Response[0],'rb') as subor:
            data = subor.read()
        

        data=hashlib.sha3_512(data)
        data=data.hexdigest()
        
        
        
        plainText=data
        plainText=str(plainText)
        i=0
        cypherText=[]
        
        Response =QFileDialog.getOpenFileName(
            parent=self,
            caption="Vyber privatny kluc",
            directory=os.getcwd(),
            filter="kluc.priv",
            )
        key=open(Response[0],"r")
        key=key.read()
        key=key.split()
        key=list(key)
        d=key[0]
        n=key[1]
        
            

        
        while(i<len(plainText)):
            BigNumber=""
            binaryText=[]
            if i+6 > len(plainText):
                maxIndex=len(plainText)
            else:
                maxIndex=i+6
            for j in range (i,maxIndex):
                num=ord(plainText[j])
                binaryText.append(f'{num:012b}') 
            for j in range(0,maxIndex-i):
                BigNumber+=binaryText[j]
                
            BigNumber=int(BigNumber,2)
            x=pow(BigNumber,int(d),int(n))
            cypherText.append(x)
            i+=6
       

        cypherText=str(cypherText)
        cypherText=list(cypherText)
        cypherText=listToString(cypherText)
        cypherText=cypherText.replace("[","")
        cypherText=cypherText.replace("]","")
        cypherText=cypherText.replace(",","")
        
        
        g=open("podpis.sign","w+")
        g.write(cypherText)
        g.close()    
        
        zipObj = ZipFile('podpis.zip', 'w')
        
        zipObj.write("podpis.sign")
        zipObj.write(cesta,basename(cesta))

        zipObj.close()
        self.label_2.setText("data podpisane")

    def overenie(self):
  
        zipObj = ZipFile("podpis.zip","r")
        zipObj.extractall('overenie')
        zipObj.close()
        Response =QFileDialog.getOpenFileName(
            parent=self,
            caption="Vyber originalny subor",
            directory='overenie',
            filter=None,
            )
        
        with open(Response[0],'rb') as subor:
            data = subor.read()
        
        data=hashlib.sha3_512(data)
        data=data.hexdigest()

        
        
        Response =QFileDialog.getOpenFileName(
            parent=self,
            caption="Vyber public key",
            directory=os.getcwd(),
            filter="kluc.pub",
            )
        
        key=open(Response[0],"r")
        key=key.read()
        key=key.split()
        key=list(key)
        e=key[0]
        n=key[1]
        
        Response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Vyber .sign subor",
            directory='overenie',
            filter='podpis.sign',
            )
        sign=Response[0]
        
        
        
    

        vstup=open(sign,'r')

        
        vstup=vstup.read()
        vstup=str(vstup)
        vstup=vstup.replace("[","")
        vstup=vstup.replace("]","")
        vstup=vstup.replace(",","")


        i=0
        bigNumber=""
        x=[]
        while i<len(vstup):
            
            

            if not(vstup[i]==" " or i==len(vstup)-1):

                bigNumber+=vstup[i]


            else:
                if i==len(vstup)-1:
                    bigNumber+=vstup[i]

            
                
                bigNumber=pow(int(bigNumber),int(e),int(n))
                binNum=format(bigNumber,'b')
                if len(binNum)%12!=0:
                    for p in range(12-len(binNum)%12):
                        binNum=''.join(('0',binNum))
                        
                j=0 
                while  j<len(binNum):
                    blok=[]
                    for k in range(j,j+12):
                        blok.append(binNum[k])
                    blok=listToString(blok)
                    blok=int(blok,2)
                    pom=chr(blok)
                    pom=str(pom)
                    x.append((pom))
                    j+=12
                    bigNumber=""


            i+=1 



                
        if(listToString(x)==data):
            self.label_2.setText("overenie prebehlo uspesne")

            
        else:
            self.label_2.setText("overenie prebehlo neuspesne")

                
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)  
        self.pushButton_Generovat.clicked.connect(self.getKeys)
        self.pushButton_2.clicked.connect(self.podpis)
        self.pushButton_overit.clicked.connect(self.overenie)

        
        
     
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        
           