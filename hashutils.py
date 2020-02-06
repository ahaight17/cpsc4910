import hashlib

def makeHash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def checkHash(password, hash):
    if makeHash(password) == hash:
        return True
    return False
