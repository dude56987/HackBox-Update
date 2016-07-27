# /bin/bash
########################################################################
# Update the system and reboot when no users are logged in.
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
# check if any users are logged in
while true;do
	# set or reset the flag for logged in users
	loggedIn=false;
	# compare user home directories to the output from the users command
	for dir in /home/*; do
		user=$(echo $dir | sed "s/\/home\///g")
		if who | grep -c -q $user; then
			# if someone is logged in print thier name
			echo "$user is still logged in."
			# also set the flag that someone is logged in
			loggedIn=true;
		fi
	done
	if $loggedIn;then
		# if logged in is true someone is logged in so repeat the loop
		# after a 90 second delay
		echo "Users are logged in, system will not reboot yet."
		echo "Waiting 90 seconds to check again..."
		sleep 90;
	else
		# break the loop and run update if no users are logged in
		break;
	fi
done
# update the system, use autoclean logs to clear logs
update --auto-clean-log
# reboot the computer 
reboot
