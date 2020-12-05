/////// NOT WORKING BECAUSE SHITTY GO REGEXP IMPL
package main

import (
	"regexp"

	"github.com/glenn-brown/golang-pkg-pcre/src/pkg/pcre"
)

func main() {
	input := []string{
		"fonbsmjyqugrapsczckghtvdxl",
		"fonpsmjyquwrnpeczikghtvdxw",
		"fonbsmdymuwrapexzikghtvdxl",
		"fonwsmjyquwrapeczikghttdpl",
		"fonbsmjkquwrapeczjkghtvdxx",
		"yonbsmjyquwrapecgikghtvdxc",
		"donbsmjyquqrapeczikghtadxl",
		"monbsmjyquprgpeczikghtvdxl",
		"fonbsmjyquwvapecqgkghtvdxl",
		"fonbsmjyquwrkphczikghsvdxl",
		"fonbomjyeuwvapeczikghtvdxl",
		"fonwsmjyjuwrapoczikghtvdxl",
		"foybsmjyquwcapeczikghsvdxl",
		"fonbsmjyquwrtaeczikgptvdxl",
		"ponbsmpyquwjapeczikghtvdxl",
	}

	pairs, triples := 0, 0
	// Check if has pair
	pattern1,_ := pcre.Compile("(.).*(\\1)", 0)
	for _, s := range input {
		match, _ := regexp.MatchString(, s)
		println(s, match)
		if match {
			pairs++
		}
	}
	println(pairs, triples)
}
