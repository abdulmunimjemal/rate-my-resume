import os

# calculate file size, if it is greater than 10MB, return False, else return True
def healthy_file_size(file, max_size=2):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size <= max_size * 1024 * 1024