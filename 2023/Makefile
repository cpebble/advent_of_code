
# I.e. skel_day2
skel_%:
	mkdir $*
	cp -r .skel/* $*/
	find $* -type f -exec sed -i "s/{{DAY}}/$*/" {} + ;

