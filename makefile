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
	# copy the apt progressbar config
	cp apt-progressbar-config debian/etc/apt/apt.conf.d/9999-hackbox-apt-progressbar
	# copy over the files 
	cp -vf update.py ./debian/usr/bin/update
	cp -vf update-reboot.sh ./debian/usr/share/hackbox-update/update-reboot
	cp -vf update.desktop ./debian/usr/share/applications/update.desktop 
	# make the program executable
	chmod +x ./debian/usr/bin/update
	chmod +x ./debian/usr/share/hackbox-update/update-reboot
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
