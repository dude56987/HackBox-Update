# /bin/bash
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
