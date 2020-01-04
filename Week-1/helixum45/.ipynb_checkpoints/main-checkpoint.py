from features import *
from priceDrop import * 

import sys 
import argparse


if(sys.argv[1] == "-c"):
    mobile1Name = sys.argv[2]
    mobile2Name = sys.argv[3]
    print("<<<<<<<  " + mobile1Name +"  >>>>>> <<<<<<  "+ mobile2Name+"  >>>>>")
    
    mobile1 = Features(mobile1Name)
    mobile2 = Features(mobile2Name)
    
    compareJSON(mobile1, mobile2).saveJSONComparision()
    
elif(sys.argv[1] == "-i"):
    mobileName = sys.argv[2]
    print("<<<<<<  "+mobileName+"  >>>>>>")
    
    mobile = Features(mobileName)
    mobile.saveToJSON()

elif(sys.argv[1] == "-n"):
    senderEmail = input("Senders Email :  ")
    senderPassword = input("Enter password :  ")
    receiverEmail = input("Receivers Email :  ")
    
    mobile1 = Features(sys.argv[3])
    p1 = int("".join(mobile1.getSpecs()['Price'][1:].split(',')))

    if(sys.argv[2] ==  "-o"):
        tp = trackPrice(mobile1,p1, senderEmail, senderPassword, receiverEmail)
        tp.trackAndNotifyOne(60)
        
        
    elif(sys.argv[2] ==  "-t"):
        mobile2 = Features(sys.argv[3])
        p2 = int("".join(mobile2.getSpecs()['Price'][1:].split(',')))
        
        tp = trackPrice(mobile1,mobile2, p1, p2, senderEmail, senderPassword, receiverEmail)
        tp.trackAndNotifyTwo(60)
    
    
