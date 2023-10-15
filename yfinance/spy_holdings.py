# Get constituents of SPY
#Downloads holdings from ssga
import requests 
import pandas as pd 
import os 
import shutil
import datetime as dt
import config as c

url = s.SPY_DOWNLOAD_URL

file_name = f"spy_data_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
folder_name = c.SPY_DATA_FOLDER
archive_name = c.SPY_ARCHIVE_FOLDER

if not os.path.exists(folder_name): 
    os.mkdir(folder_name)

if not os.path.exists(archive_name): 
    os.mkdir(archive_name)

for file in os.listdir(folder_name): 
    shutil.move(os.path.join(folder_name, file), os.path.join(archive_name, file))

response = requests.get(url)

try:
    with open(os.path.join(folder_name, file_name), "wb") as f: 
        f.write(response.content)
    print('File downloaded successfully!!')
except:
    print('There is an exception downloading SPY file')