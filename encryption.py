import rsa

PRIVATE_KEY_PATH = "private_key.pem"

# Creates private and public keys for a node in the network and stores these
# keys on the local machine in PEM formats
def create_keys():

    #Creates new keys, public and private key
    (servers_pubkey, servers_privkey) = rsa.newkeys(512)

    # Saves private and public keys on local machine in PEM format
    priv_key_file = open(PRIVATE_KEY_PATH, 'wb')
    priv_key_file.write(servers_privkey.save_pkcs1())
    priv_key_file.close()

    pubkey = servers_pubkey.save_pkcs1().decode()[31:-30]

    return pubkey

# Performs encryption a message usign a provided public key
def encrypt_using_public_key(message,public_key):

    public_key = "-----BEGIN RSA PUBLIC KEY-----\n" + public_key + \
                "\n-----END RSA PUBLIC KEY-----\n"

    # Enter the linux command and encode it in UTF-8,since RSA module operates
    # on bytes, not strings
    encoded_message = message.encode()
    my_final_public_key = rsa.PublicKey.load_pkcs1(public_key)

    #client encrypts its linux command using servers public key
    encrypted_message = rsa.encrypt(encoded_message, my_final_public_key)

    return encrypted_message

#Performs decryption on an encrypted message when keys
#are present locally on a machine
def decrypt_using_private_key(encrypted_message):

    #Read the private key stored in secondary memory in PEM format
    with open(PRIVATE_KEY_PATH, mode='rb') as privatefile:
        private_key_data = privatefile.read()

    #Convert the PEM format to normal private key format
    my_final_private_key = rsa.PrivateKey.load_pkcs1(private_key_data)

    #server decrypts it using its own private key
    message = rsa.decrypt(encrypted_message,my_final_private_key)

    #Decoded message
    decoded_message = message.decode()
    return decoded_message

create_keys()
