#!/usr/bin/python3

import dropbox
import sys
import time
import os
import subprocess
import sys
import gzip

# DROPBOX PERSONAL DATA, TO BE FILLED-IN
db_access_token='XXXXXXXX'
db_path='XXXXXXXX'

#PROGRAM ARGUMENTS
if len(sys.argv) > 1:
	folder=str(sys.argv[1])
	if (os.path.exists(folder)==False):
		print("[ERROR] The folder path provided doesn't exist.")
		sys.exit()
else:
	print('Usage: ' + sys.argv[0] + ' [SOURCE_FOLDER_PATH]')
	sys.exit()

#TIME
now=time.strftime("%Y%m%d_%H%M%S", time.localtime())

#VARIABLES
FNULL = open(os.devnull, 'w')
p1 = subprocess.Popen(["pwd"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out, err = p1.communicate()
path=str(out)[2:-3]+'/'
filename='bckp-'+now+'.tar.gz'

print('\n[INFO] Starting program. It will backup `' + folder + '` to `' + db_path + filename)
print('[INFO] Actual path: `'+ path+'`')
print("[INFO] Authenticating at Dropbox... ", end="")
sys.stdout.flush()

#DROPBOX AUTHENTICATION
try:
	dbx = dropbox.Dropbox(db_access_token)
	account = dbx.users_get_current_account()
	print("[OK]")
	#print('	- Modified: `' + dbx.files_get_metadata('/Backup/').client_modified + '`')
	print('	- Account_id: `' + account.account_id + '`')
	print('	- Account_name: `' + account.name.given_name+ '`')
	print('	- Account_e-mail: `' + account.email+ '`')
	#print('	- Account_type: `' + account.account_type+ '`')
	#sys.stdout.flush()
except:
	print("[KO]")
	print("[ERROR] Authentication NOT successful!")
	sys.exit()

#FILE COMPRESSION
print("[INFO] Compressing folders and files... ", end="")
sys.stdout.flush()
try:
	#command='tar -zcvf ' + path + filename + ' ' + folder +' -R'
	p1 = subprocess.Popen(["tar","-zcvf",path+filename,folder,"-R"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p1.communicate()
	#print(out)
	#print(err)
	p1.wait();
	#command='chmod 777 ' + path + filename
	p2 = subprocess.Popen(["chmod","777",path+filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	#print(out)
	#print(err)
	p2.wait();
	print("[OK]")
	print('	- Teomporary file: `' + path+filename+ '`')
except:
	print("[KO]")
	print('[ERROR] Something went wrong during compression of '+ path + filename)
	sys.exit()

#DROPBOX UPLOAD
print("[INFO] Uploading to Dropbox... ", end="")
sys.stdout.flush()
try:
	f = gzip.open(path + filename, mode='r')
	fileupload = dbx.files_upload(f,'/Backup/'+filename) #Method used to upload files smaller than 150MB
	print("[OK]")
except:
	print("[KO]")
	print("\n[ERROR] Ouch! Something went wrong!")
	sys.exit()

print('	- Filename: `' + db_path+filename + '`')
print('	- Modified: `' + str(dbx.files_get_metadata('/Backup/'+filename).client_modified) + '`')

#DELETING LOCAL FILE
print("[INFO] Deleting local file `" +path+filename + '`... ', end="")
sys.stdout.flush()
try:

	p1 = subprocess.Popen(["rm","-f",path+filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = p1.communicate()
	#print(out)
	#print(err)
	p1.wait();
	print("[OK]")
except:
	print("[KO]")
	print('[ERROR] Something went wrong during compression of '+ path + filename)
	sys.exit()
