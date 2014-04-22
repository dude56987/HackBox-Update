show:
	echo 'Run "make install" as root to install program!'
	
run:
	python update.py
install:
	sudo apt-get install transmission-gtk --assume-yes
	sudo cp update.py /usr/bin/update
	sudo chmod +x /usr/bin/update
	sudo link /usr/bin/update /etc/cron.daily/update
uninstall:
	sudo rm /usr/bin/update
	sudo rm /etc/cron.daily/update
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
	mkdir -p debian/usr/share/applications;
	# make post and pre install scripts have the correct permissions
	chmod 775 debdata/*
	# copy over the binary
	cp -vf update.py ./debian/usr/bin/update
	cp -vf update.desktop ./debian/usr/share/applications/update.desktop 
	# make the program executable
	chmod +x ./debian/usr/bin/update
	# start the md5sums file
	md5sum ./debian/usr/bin/update > ./debian/DEBIAN/md5sums
	md5sum ./debian/usr/share/applications/update.desktop > ./debian/DEBIAN/md5sums
	# create md5 sums for all the config files transfered over
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	chmod -Rv go+r debian/ 
	dpkg-deb --build debian
	cp -v debian.deb update_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
