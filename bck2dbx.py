#!/usr/bin/python3

import dropbox
import sys
import time
import os
import subprocess
import sys
import gzip

# DROPBOX PERSONAL DATA - TO BE FILLED IN
db_access_token='XXXXXXXX'
db_path='XXXXXXXX'

# PROGRAM ARGUMENTS
if len(sys.argv) > 1:
	folder=str(sys.argv[1])
else:
	print('Usage: ' + sys.argv[0] + ' [FOLDER_PATH]')
	sys.exit()

# VARIABLES
now=time.strftime("%Y%m%d_%H%M%S", time.localtime())
FNULL = open(os.devnull, 'w')
path=os.path.dirname(os.path.realpath(__file__))
#path='/home/'
filename='bckp-'+now+'.tar.gz'

print('[INFO] This program will backup the folder `' + folder + '` to `' + db_path + filename + '`...')
print("[INFO] Authenticating at Dropbox... ", end="")

try:
  dbx = dropbox.Dropbox(db_access_token)
  account = dbx.users_get_current_account()
	print("OK")
	#print('	- Account_id: ' + account.account_id)
	#print('	- Account_name: ' + account.name.given_name)
	#print('	- Account_e-mail: ' + account.email)
except:
	print("Authentication NOT successful!")
	sys.exit()

try:
	command='tar -zcvf ' + path + filename + ' ' + folder +' -R'
	print("[INFO] Compressing folders and files... ", end="")
	subprocess.call(command.split(), shell=False, stdout=FNULL, stderr=subprocess.STDOUT)
	command='chmod 777 ' + path + filename
	subprocess.call(command.split(), shell=False, stdout=FNULL, stderr=subprocess.STDOUT)
	print("OK")
except:
	print('[ERROR] Something went wrong during compression of '+ path + filename)
	sys.exit()

print("[INFO] Uploading to Dropbox... ", end="")
try:
	f = gzip.open(path + filename, mode='r')
	fileupload = dbx.files_upload(f,'/Backup/'+filename)
	print("OK")
except:
	print("[ERROR] Ouch! Something went wrong!")