#! /usr/bin/python
########################################################################
# Updates and upgrades the system automaticly.
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
from os import system
from os.path import exists
from os import geteuid
import sys
# check for gui argument since it is a shortcut to relaunch the program graphically
if '--gui' in sys.argv:
	# check for graphical terminal emulators to run the program with
	if exists('/usr/bin/terminator'):
		# use terminator
		system('''terminator -f -T "Update Software" -x bash -c "pkexec update;echo 'Press enter to end the program.';read;"''')
	elif exists('/usr/bin/xterm'):
		# use xterm
		system('''xterm -T "Update Software" -e bash -c "pkexec update;echo 'Press enter to end the program.';read;"''')
	else:
		# if none exist just run the program normally
		system('pkexec update')
	# exit the program after gui execution
	exit()
#check for root since shortcuts need to be installed for all users
if geteuid() != 0:
	print 'ERROR: this command must be ran as root!'
	print 'It will install updates for the entire system!'
	exit()
else:
	if '--reboot-on' in sys.argv:
		# make the reboot script executable, the zz makes it run last
		system('chmod +x /etc/cron.daily/zz-update-reboot')
		# remove execute permissions for normal updates
		system('chmod -x /etc/cron.daily/update')
		exit()
	elif '--reboot-off' in sys.argv:
		# make the default cron script executable
		system('chmod +x /etc/cron.daily/update')
		# remove executable permissions on reboot script
		system('chmod -x /etc/cron.daily/zz-update-reboot')
		exit()
	elif '--view-log' in sys.argv:
		system('more /var/log/autoUpdate* | less')
		exit()
	elif '--clean-log' in sys.argv:
		system('rm -v /var/log/autoUpdateLog')
		system('rm -v /var/log/autoUpdateLog.old')
		exit()
	elif '--help' in sys.argv or '-h' in sys.argv:
		helpOutput ='#######################################################################\n'
 		helpOutput +='Updates and upgrades the system automaticly.\n'
 		helpOutput +='Copyright (C) 2014  Carl J Smith\n'
		helpOutput +='\n'
 		helpOutput +='This program is free software: you can redistribute it and/or modify\n'
 		helpOutput +='it under the terms of the GNU General Public License as published by\n'
 		helpOutput +='the Free Software Foundation, either version 3 of the License, or\n'
 		helpOutput +='(at your option) any later version.\n'
 		helpOutput +='This program is distributed in the hope that it will be useful,\n'
 		helpOutput +='but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
 		helpOutput +='MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
 		helpOutput +='GNU General Public License for more details.\n'
		helpOutput +='\n'
 		helpOutput +='You should have received a copy of the GNU General Public License\n'
 		helpOutput +='along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
 		helpOutput +='#######################################################################\n'
		helpOutput +='--help or -h\n'
		helpOutput +='    Shows this help menu.\n'
		helpOutput +='--new-conf\n'
		helpOutput +='    Installs the package maintainers version of\n'
		helpOutput +='    any config files that have been updated.\n'
		helpOutput +='--reboot\n'
		helpOutput +='    Reboots the computer after update.\n'
		helpOutput +='--reboot-on\n'
		helpOutput +='    Activates server style update then\n'
		helpOutput +='     reboot procedures. System will wait\n'
		helpOutput +='     till no users are logged in and usage\n'
		helpOutput +='     is low. The system will then update \n'
		helpOutput +='     and reboot.\n'
		helpOutput +='--reboot-off\n'
		helpOutput +='    Reverses the changes made by the reboot\n'
		helpOutput +='     on command.\n'
		helpOutput +='--log\n'
		helpOutput +='   Log during updates.\n'
		helpOutput +='--view-log\n'
		helpOutput +='    Displays logs of the system updates.\n'
		helpOutput +='--clean-log\n'
		helpOutput +='    Remove old logs.\n'
		helpOutput +='--auto-clean-log\n'
		helpOutput +='    Auto remove logs over 10000 lines long.\n'
 		helpOutput +='#######################################################################\n'
		print helpOutput
		# this just prints the help and quits the program when
		# the --help or -h argument is given to the program
		exit()
	if '--auto-clean-log' in sys.argv:
		# clean logs with more than 10000 lines, copy the big file to a .old file and then create a new log, this needs rewrote in python
		readFile=open('/var/log/autoUpdateLog','r')
		tempFile=''
		overFlowFile=''
		counter=0
		# read each line of the file into tempFile
		for line in readFile:
			counter+=1
			tempFile+=line
		# if log is more than 10000 lines move it to a .old file
		if counter > 10000:
			# write the content of existing file to a .old file
			overFlowFile=open('/var/log/autoUpdateLog.old','w')
			overFlowFile.write(tempFile)
			overFlowFile.close()
			# blank out existing file
			blankFile=open('/var/log/autoUpdateLog','w')
			blankFile.write('')
			blankFile.close()	
	## figure out if apt-fast or apt get is present use apt-fast if possible
	if exists('/usr/bin/apt-get'):
		installCommand = 'apt-get'
	if exists('/usr/bin/apt-fast'):
		installCommand = 'apt-fast'
	# check if logfile is to be made
	if ('--log' in sys.argv) or ('--auto-clean-log' in sys.argv):
		logCommand = " >> /var/log/autoUpdateLog"
		# add date header at begining of log
		system('echo "'+('#'*80)+'"'+logCommand)
		system('echo "Update started on $(date)"'+logCommand)
		system('echo "'+('#'*80)+'"'+logCommand)
		# print log stuff above to screen	
		print ('#'*80)
		system('echo "Update started on $(date)"')
		print ('#'*80)
	else:
		# log command is nothing if --log is not set
		logCommand = ''
	########################################################################
	print '#'*80
	print 'Checking for partially installed packages...'
	print '#'*80
	# the below command will complete package installs that were interupted, otherwise it does nothing
	system('dpkg --configure -a'+logCommand)
	# clean up the repo lists to keep from getting errors on comments
	print '#'*80
	print('Cleaning up the repo lists...')
	print '#'*80
	# remove all the comments from repo lists
	system('sed -i "s/^#.*$//g" /etc/apt/sources.list.d/*.list'+logCommand)
	# remove empty lines from repo lists
	system('sed -i "/^$/d" /etc/apt/sources.list.d/*.list'+logCommand)
	########################################################################
	print '#'*80
	print 'Updating the repos...'
	print '#'*80
	system(installCommand+' update --assume-yes'+logCommand)
	# the commands below fix broken packages, if broken, otherwise it does nothing
	print '#'*80
	print 'Searching for and fixing broken packages...'
	print '#'*80
	system(installCommand+' -f install'+logCommand)
	system(installCommand+' install --fix-missing'+logCommand)
	# the -o options in the below commands make them automaticly update config files
	# changed in the updates if they have not been edited by hand
	print '#'*80
	print 'Installing new packages...'
	print '#'*80
	if '--new-conf' in sys.argv: # set user to replace config files with package version
		print 'Using the package maintainers version of config files...'
		print '#'*80
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" upgrade --assume-yes'+logCommand)
		# the dist-upgrade option is included to update the kernel
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" dist-upgrade --assume-yes'+logCommand)
	else: # use the current conf files so nothing will change
		print 'Keeping your current config files...'
		print '#'*80
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade --assume-yes'+logCommand)
		# the dist-upgrade option is included to update the kernel 
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade --assume-yes'+logCommand)
	print '#'*80
	print ("Removing unused packages...")
	print '#'*80
	system(installCommand+' autoremove --assume-yes'+logCommand)
	print '#'*80
	print ("Clearing downloaded files...")
	print '#'*80
	system(installCommand+' clean --assume-yes'+logCommand)
	print '#'*80
	print ("Update Complete!")
	print '#'*80
	if exists('/usr/bin/reboot-required'):
		system('reboot-required')
	if '--reboot' in sys.argv:
		system('reboot')
