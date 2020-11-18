import os
import sys
import time
from signal import signal, SIGINT
from sys import exit
import subprocess
from uuid import getnode as get_mac
import keyboard
import commands
def stop_if_already_running():
	script_name = os.path.basename(__file__)
	l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'| awk '{print $2}'" % script_name)
	if l[1]:
		while True:
			os.system('clear')
			logo()
			print ("")
			print("Looks Like the script is already running... What would you like to do?")
			print ("1. Create another random MAC")
			print ("2. Reset network card with same random MAC")
			print ("3. Use real MAC")
			mini_menu = raw_input(">> ")

			if mini_menu == '1':
				print 'Please wait...'
				time.sleep(1)
				print 'Stoping Network Manager...'
				os.system('service network-manager stop')
				print 'Putting down wlan0...'
				os.system('ifconfig wlan0 down')
				print 'Generating new MAC...'
				os.system('macchanger -r wlan0')
				print 'Restoring Network with new MAC...'
				os.system('service network-manager start')  
				os.system('ifconfig wlan0 up')
				exit()
			elif mini_menu == '2':
				print 'Stoping Network Manager...'
				os.system('service network-manager stop')
				print 'Putting down wlan0...'
				os.system('ifconfig wlan0 down')
				print 'Restoring Network with same MAC...'
				os.system('service network-manager start') 
				os.system('ifconfig wlan0 up')
				exit()
			elif mini_menu == '3':
				print 'Stoping Network Manager...'
				os.system('service network-manager stop')
				print 'Putting down wlan0...'
				os.system('ifconfig wlan0 down')
				print 'Restoring...'
				os.system('macchanger -p wlan0')
				os.system('service network-manager start') 
				os.system('ifconfig wlan0 up')
				exit()
			else:
				print ("Unknown Option.")





get_og_mac = """ifconfig wlan0 | awk '/ether/{print $2}'"""
amac = os.popen(get_og_mac).read()
user = os.getenv("SUDO_USER")
if user is None:
	os.system('clear')
	print "This program needs/root 'sudo'"
	time.sleep(5)
	os.system('clear')
	exit()
def logo():
	print '''
       _____                 _                 __  __          _____ 
      |  __ \               | |               |  \/  |   /\   / ____|
      | |__) |__ _ _ __   __| | ___  _ __ ___ | \  / |  /  \ | |     
      |  _  // _` | '_ \ / _` |/ _ \| '_ ` _ \| |\/| | / /\ \| |     
      | | \ \ (_| | | | | (_| | (_) | | | | | | |  | |/ ____ \ |____ 
      |_|  \_\__,_|_| |_|\__,_|\___/|_| |_| |_|_|  |_/_/    \_\_____|
                                                                
      Created By Xipe0x456. | Automating Random MAC Spoofing.                                                            
'''
	print '        Current MAC:'
	os.system('ifconfig wlan0 | awk "/ether/{print $2}"')

devnull = open(os.devnull,"w")
retval = subprocess.call(["dpkg","-s","macchanger"],stdout=devnull,stderr=subprocess.STDOUT)
devnull.close()
if retval != 0:
	logo()
	print ''
	print "Package macchanger not installed."
	while True:
		print 'Would you like me to install for you?'
		yn = raw_input('Y/N?> ')
		if yn == 'y':
			os.system('wget http://ftp.br.debian.org/debian/pool/main/m/macchanger/macchanger_1.7.0-5.4_amd64.deb')
			os.system('dpkg -i macchanger_1.7.0-5.4_amd64.deb')
			break
		elif yn == 'n':
			os.system('clear')
			logo()
			print ''
			print 'MacChanger is needed. Please install to use this script.'
			time.sleep(5)
			os.system('clear')
			exit()
		else:
			print 'Unknown option.'

#stop_if_already_running()
logo()
print ''
print 'Please wait...'
time.sleep(1)
print 'Stoping Network Manager...'
os.system('service network-manager stop')
print 'Putting down wlan0...'
os.system('ifconfig wlan0 down')
print 'Generating new MAC...'
os.system('macchanger -r wlan0')
print 'Restoring Network with new MAC...'
os.system('service network-manager start')  
os.system('ifconfig wlan0 up')
print 'Spoofed! Please hit CTRL-C to stop...'
def handler(signal_received, frame):
	print ''
	print 'Oof! CTRL-C Detected.. Please wait..'
	print 'Stoping Network Manager...'
	os.system('service network-manager stop')
	print 'Putting down wlan0...'
	os.system('ifconfig wlan0 down')
	print 'Restoring MAC...'
	os.system('macchanger -p wlan0')
	print 'Restoring Network...'
	os.system('service network-manager start')  
	os.system('ifconfig wlan0 up')
	print('SIGINT or CTRL-C detected. Exiting gracefully')
	exit(0)
if __name__ == '__main__':
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit, or hit Q for a new Mac Address.')
    while True:
		
    	os.system('clear')
    	logo()
    	print '        Spoofed! Please hit CTRL-C to stop...'
    	fake_og_mac = os.popen(get_og_mac).read()
    	if fake_og_mac == amac:
    		logo()
    		print ''
    		print 'Shit! Breaking from network! Mac switched back to original. Re-Spoofing...'
    		os.system('service network-manager stop')
    		os.system('ifconfig wlan0 down')
    		os.system('macchanger -r wlan0')
    		os.system('service network-manager start')  
    		os.system('ifconfig wlan0 up')
    		os.system('clear')
    		logo()
    		print ''
    	time.sleep(1)
