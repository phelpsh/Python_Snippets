import requests
import json
import base64 
from arcpy import AddMessage

# requires pycryptodome 
from Crypto.Cipher import PKCS1_v1_5 
from Crypto.PublicKey import RSA 

# location of private key (provided)
loc = r"C:\temp\code\keypair.pem"

def get_token():
    
    url = "https://bs-api.venntel.com/v1.5/securityToken"
    
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': "cccc" #obfuscated
        }
    
    tok = ""
    
    response = requests.get(url, headers=headers)   
    
    d = json.loads(response.text)  # converts json to dictionary
    
    if 'tempSecurityEncryptedToken' in d:
        tok = d['tempSecurityEncryptedToken']
    return tok

def call_venntel(tempkey):

    url = "https://bs-api.venntel.com/v1.5/locationData/search"
    
    data = { 
        "startDate" : "2018-12-02T02:03:48Z", 
        "endDate" : "2018-12-03T02:03:48Z",
        "areas": [{
            "latitude" : 39.090631,
            "longitude" : -77.525846,
            "radius" : 100
        }, {
            "latitude" : 39.088998,
            "longitude" : -77.52296,
            "radius" : 100
        }]
    }
    
    headers = {        
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': "cccccc",  #obfuscated
        'TempSecurityToken': tempkey
    }

    response = requests.post(url, headers=headers, json=data)

    if (response.status_code == 200):
        return response.text
    else:
        return "Something's not right " + str(response.status_code)
    
token = get_token()
if token != "":
    key = RSA.importKey(open(loc, mode='rb').read()) 
    cipher = PKCS1_v1_5.new(key)     
    barray = bytearray(base64.b64decode(token)) 
    payload = cipher.decrypt(barray, len(barray)).decode('UTF-8')  
    returned = call_venntel(payload)  # payload is temp key

if (returned == ''):
    arcpy.AddMessage("***no results***")
else:
    arcpy.AddMessage(returned)
