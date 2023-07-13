import hashlib

def hasing(data):
    hasher = hashlib.sha256()
    hasher.update(data.encode())
    hashed_data = hasher.hexdigest()
    return hashed_data

hash = hasing('qweqwe')
print(hash)