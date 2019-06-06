import os
import glob



def remove_files(folder_name):
    folder_path = folder_name + '/*'
    files = glob.glob(folder_path)
    for f in files:
        os.remove(f)