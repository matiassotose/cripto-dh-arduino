def dhPartialKey(pub_K1,priv_K1,pub_K2):
    partial_key = pub_K1**priv_K1
    partial_key = partial_key % pub_K2
    return partial_key

def dhFullKey(priv_K1, pub_K2, partial_k):
    full_key = partial_k ** priv_K1
    full_key = full_key % pub_K2
    return full_key

def dhEncrypt(message, full_key):
    encrypted_m = ""
    for char in message:
        encrypted_m += chr(ord(char) + full_key)
    return encrypted_m

def dhDecrypt(encrypted_message, full_key):
    message = ""
    for char in encrypted_message:
        message += chr(ord(char)-full_key)
    return message