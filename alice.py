
import socket   #for sockets
import sys  #for exit
#from paillier.paillier import *
import json
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import ast
import pickle
import numpy as np

coeffs = raw_input("Enter the coeffs: ")

# creating polynome
coeffs = [int(x) for x in coeffs.strip().split()]
p = np.poly1d(coeffs)

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
host = 'localhost';
port = 8889;

#import the public key of the server
f = open('mykey.pem','r')
key = RSA.importKey(f.read())

#generate RSA keypair
mykey = RSA.generate(2048)
#generate a separate public key for others to use
pub = mykey.publickey()

#export this public key to a file for others to use
f = open('cl1key.pem','w')
f.write(pub.exportKey('PEM'))
f.close()

try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
#receive the nonce from server
d = s.recv(4096)
array_a = ast.literal_eval(d)

print ('array received', array_a)

array = array_a[:-1]
e = array_a[-1]

print ('array', array)
print ('e', e)


results_a = list(p(array))
print ('results a', results_a, type(results_a[0]))

h = MD5.new()
h.update(bytes(str(results_a)))
#get the digest of the hash
g = h.digest()
#encrypt the product of digest and nonce
x = key.encrypt(((g*e)), 1)

y = (x[0])
try :
    #Set the ciphertext
    s.sendall((y))
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'
 
#Now receive data
reply = s.recv(4096)
#print reply
print (reply)
