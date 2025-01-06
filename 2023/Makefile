
example_%: inputs/%.example
	echo "Pull example from clip? :"
	read q;
	test ' "$q" == "y" ' && copyq read 0 > $<
# I.e. skel_day2
cargo_%: %/Cargo.toml 
	mkdir $*
	cp -r .skel/* $*/
	find $* -type f -exec sed -i "s/{{DAY}}/$*/" {} + ;

skel_%: cargo_% example_%
	echo "Hi"

