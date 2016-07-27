########################################################################
# Build the hackbox-update package
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
show:
	echo 'Run "make install" as root to install program!'
run:
	python update.py
install: build
	sudo gdebi --no hackbox-update_UNSTABLE.deb
uninstall:
	sudo apt-get purge hackbox-update
installed-size:
	du -sx --exclude DEBIAN ./debian/
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/usr/share;
	mkdir -p debian/usr/share/hackbox-update;
	mkdir -p debian/usr/share/applications;
	mkdir -p debian/etc/apt/apt.conf.d;
	mkdir -p debian/etc/cron.daily/;
	# copy over the cron scripts and set the update script to executable
	cp -vf cron/update.sh debian/etc/cron.daily/update
	chmod +x debian/etc/cron.daily/update
	cp -vf cron/update-reboot.sh ./debian/etc/cron.daily/zz-update-reboot
	chmod -x ./debian/etc/cron.daily/zz-update-reboot
	# copy the apt progressbar config
	cp -vf apt-progressbar-config debian/etc/apt/apt.conf.d/9999-hackbox-apt-progressbar
	# copy over the files 
	cp -vf update.py ./debian/usr/bin/update
	cp -vf update.desktop ./debian/usr/share/applications/update.desktop 
	# make the program executable
	chmod +x ./debian/usr/bin/update
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size	
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	# copy over package data
	cp -rv debdata/. debian/DEBIAN/
	# fix permissions in package
	chmod -Rv 775 debian/DEBIAN/
	chmod -Rv ugo+r debian/
	chmod -Rv go-w debian/
	chmod -Rv u+w debian/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb hackbox-update_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
