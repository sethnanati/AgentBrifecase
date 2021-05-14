import json


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import oauth

BLOCK_SIZE = 16

def encrypt(data):
    obj = AES.new(oauth()['apiKey'], AES.MODE_CBC, oauth()['ivKey'])
    encdata = obj.encrypt(pad(data, BLOCK_SIZE))
    cipherhexdata = (encdata.hex())
    #print('cipherhexdata:', cipherhexdata)
    return cipherhexdata
