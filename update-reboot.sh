# /bin/bash
# check if any users are logged in
while true;do
	loggedIn=false;
	for dir in /home/*; do
		user=$(echo $dir | sed "s/\/home\///g")
		echo "Logged in users:"
		if users | grep $user; then
			# if someone is logged in exit this script
			echo "$user";
			loggedIn=true;
		fi
	done
	if [ $loggedIn == false ];then
		# break the loop and run update if no users are logged in
		break;
	else
		echo "Users are logged in, system will not reboot yet."
	fi
	sleep 90;
done
# update the system, use autoclean logs to clear logs
update --auto-clean-log
# reboot the computer
reboot
