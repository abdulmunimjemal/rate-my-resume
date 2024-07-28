from hashlib import sha256

def calculate_file_hash(file):
    file.seek(0)
    hasher = sha256()
    while chunk := file.read(8192):
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()

