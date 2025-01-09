.PRECIOUS: inputs/%.input inputs/%.example %/ %/Cargo.toml

inputs/%.example:
	echo "Pull example from clip? :"
	read q;
	test ' "$q" == "y" ' && copyq read 0 > $@

inputs/%.input:
	read q; # Pull example from clip? :
	test ' "$q" == "y" ' && copyq read 0 > $@
# I.e. skel_day2
%/Cargo.toml: 
	# "Creating directory"
	mkdir $*
	cp -r .skel/* $*/
	find $* -type f -exec sed -i "s/{{DAY}}/$*/" {} + ;



skel_%: inputs/%.example inputs/%.input %/Cargo.toml
	# Ran

