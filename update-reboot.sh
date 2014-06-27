# /bin/bash
# check if any users are logged in
for dir in /home/*; do
	user=$(echo $dir | sed "s/\/home\///g")
	echo "Logged in users:"
	if users | grep $user; then
		# if someone is logged in exit this script
		echo 	
		echo "Users are logged in, system will not reboot."
		echo "To update and reboot use the command"
		echo
		echo "update --reboot"
		echo
		echo "This script is used for automated updates to"
		echo "workstations."
		exit 1
	fi
done
echo "############################################" >> /var/log/autoUpdateLog
echo "# REBOOT AND UPDATE ON:" >> /var/log/autoUpdateLog
date >> /var/log/autoUpdateLog
update >> /var/log/autoUpdateLog
# reboot the computer
reboot
