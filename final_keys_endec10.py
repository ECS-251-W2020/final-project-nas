import rsa
import rsa.randnum
import subprocess
import sys
#from Crypto.PublicKey import RSA  
#from Crypto.Util import asn1  
#from base64 import b64decode 

#Creates private and public keys for a node in the network and stores these keys on the local machine in PEM formats     
def create_keys():

#Creates new keys, public and private key
    (servers_pubkey, servers_privkey) = rsa.newkeys(512)
    #print(servers_pubkey)
    #print(servers_privkey)
        
        # Saves private and public keys on local machine in PEM format
    priv_key_file = open('NAS_private_key.pem', 'w')
    priv_key_file.write(servers_privkey.save_pkcs1().decode('utf-8'))
    priv_key_file.close()
    #pub_key_file = open('NAS_public_key.pem', 'w')
    #my_public_key_pem_file = pub_key_file.write(servers_pubkey.save_pkcs1().decode('utf-8'))
    #pub_key_file.close()
    print(servers_pubkey.save_pkcs1().decode('utf-8'))
    pem_pubkey = servers_pubkey.save_pkcs1().decode('utf-8')
    #my_final_public_key = rsa.PublicKey.load_pkcs1(pem_pubkey)
    #print(pem_pubkey)
    return pem_pubkey

    
#Encode and encrypt the command

#def encode_and_encrypt_message(self,message):
	
    #Enter the linux command and encode it in UTF-8,since RSA module operates on bytes, not strings
    #encoded_message = message.encode('utf8')

    #client encrypts its linux command using servers public key
    #encrypted_message = rsa.encrypt(encoded_message, self.servers_pubkey)
    #return encrypted_message

#Decrypt and decode the command

#def decrypt_and_decode_message(self,encrypted_message):
     #server decrypts it using its own private key
     #message = rsa.decrypt(encrypted_message, self.servers_privkey)

     #Decoded message
     #decoded_message = message.decode('utf8')
     #return decoded_message

# break files into chunks of 245 bytes, encrypt each of them individually and concatenate them

    #def send_encrypted_file(self,file):
#	my_encrypted_file = 


#Loads the key from a local file which is in PEM format and converts it into normal key format which can be used for encryption and decryption

def load_private_key():
    #Read the private key stored in secondary memory in PEM format
    with open('NAS_private_key.pem', mode='rb') as privatefile:
        private_key_data = privatefile.read()
  
    #Convert the PEM format to normal private key format
    my_final_private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
    return my_final_private_key

#def create_keys_and_return_public_key():
    #Read the public key stored in secondary memory in PEM format
    #with open('NAS_public_key.pem', mode='rb') as privatefile:
    #    public_key_data = privatefile.read()
    
    #public_key_data = create_keys()
    #Convert the PEM format to normal public key format
    #my_final_public_key = rsa.PublicKey.load_pkcs1(public_key_data)
    #return my_final_public_key

# Performs encryption on a message when keys are present locally on the machine

def encrypt_using_public_key(message,public_key):
        
        #Enter the linux command and encode it in UTF-8,since RSA module operates on bytes, not strings
    encoded_message = message.encode('utf8') 
    
    my_final_public_key = rsa.PublicKey.load_pkcs1(public_key)    
        #client encrypts its linux command using servers public key
    encrypted_message_1 = rsa.encrypt(encoded_message, my_final_public_key)
    return encrypted_message_1

#Performs decryption on an encrypted message when keys are present locally on a machine

def decrypt_using_private_key(encrypted_message):
        
        #server decrypts it using its own private key
    message = rsa.decrypt(encrypted_message,load_private_key())

        #Decoded message
    decoded_message = message.decode('utf8')
    return decoded_message
        


my_public_key = create_keys()

message1 = "hi there"

print("****************************************")
#print(data)
print("Your message:\n")
print(message1)
print("Length of message is {}".format(len(message1)))
print("*****************************************\n")

#print("*****************************************")
#my_encrypted_message = create_keys_and_encrypt_using_public_key(message1)
#print(my_encrypted_message)
#print(len(my_encrypted_message))
#print("*****************************************\n")

#print("******************************************")
#my_decrypted_message = decrypt_using_private_key(my_encrypted_message)
#print(my_decrypted_message)
#print(len(my_decrypted_message))
#print("******************************************\n")
