
import socket
import sys
from thread import *
import Crypto
from Crypto.PublicKey import RSA
from random import randint
import ast
import pickle
import numpy as np

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#generate RSA keypair
key = RSA.generate(2048)
#generate a separate public key for others to use
pub = key.publickey()

#export this public key to a file for others to use
f = open('mykey.pem','w')
f.write(pub.exportKey('PEM'))
f.close()

#create random dots two nonces to send to the two clients 
non_a = (randint(1,10))
non_b = (randint(1,10))
dots = list(np.random.randint(-2 ** 31, 2 ** 31, 10))


#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
array_a = dots + [non_a]
array_b = dots + [non_b]

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    conn.send(str(array_a))
    
    #receive data from client A
    d = conn.recv(1024)   
    #get client's public key (for later)
    f = open('cl1key.pem','r')
    cl1key = RSA.importKey(f.read())
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #decrypt the data
    data = ((d))
    b = key.decrypt(data)
    
    #repeat the same for client B
    conn2, addr2 = s.accept()
    conn2.send(str(array_b))
    
    d2 = conn2.recv(1024)
    
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    data2 = ((d2))
    c = key.decrypt(data2)
    
    #multiply decrypted values with opposite nonces
    a1= b*non_b
    a2= c*non_a

    #if the final values are equal, output same else not same
    if (a1==a2):
        print "EQUAL"
        conn.send("EQUAL")
        conn2.send("EQUAL")
    else:
        print "NOT EQUAL"
        conn.send("NOT EQUAL")
        conn2.send("NOT EQUAL")
    print "END"
    
s.close()
