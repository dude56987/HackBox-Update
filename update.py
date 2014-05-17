#! /usr/bin/python
########################################################################
# Updates and upgrades the system automaticly.
# Copyright (C) 2014  Carl J Smith
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
#check for root since shortcuts need to be installed for all users
if geteuid() != 0:
	print 'ERROR: this command must be ran as root!'
	print 'It will install updates for the entire system!'
	exit()
else:
	if '--help' in sys.argv or '-h' in sys.argv:
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
 		helpOutput +='#######################################################################\n'
		print helpOutput
		# this just prints the help and quits the program when
		# the --help or -h argument is given to the program
		exit()
	## figure out if apt-fast or apt get is present use apt-fast if possible
	if exists('/usr/bin/apt-get'):
		installCommand = 'apt-get'
	if exists('/usr/bin/apt-fast'):
		installCommand = 'apt-fast'
	# note that the dist-upgrade option is included to update the kernel automatically
	system(installCommand+' update --assume-yes')
	# the commands below fix broken packages, if broken, otherwise it does nothing
	system(installCommand+' -f install')
	system(installCommand+' install --fix-missing')
	# the -o options in the below commands make them automaticly update config files
	# changed in the updates if they have not been edited by hand
	if '--new-conf' in sys.argv: # set user to replace config files with package version
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" upgrade --assume-yes')
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" dist-upgrade --assume-yes')
	else: # use the current conf files so nothing will change
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade --assume-yes')
		system(installCommand+' -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade --assume-yes')
	print ("Removing unused packages...")
	system(installCommand+' autoremove --assume-yes')
	print ("Clearing downloaded files...")
	system(installCommand+' clean --assume-yes')
	print ("Update Complete!")
	if exists('/usr/bin/reboot-required'):
		system('reboot-required')
	if '--reboot' in sys.argv:
		system('reboot')
