package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func readInput() []string {
	var file, err = os.Open("day3.input")
	if err != nil {
		return []string{}
	}
	var scanner = bufio.NewScanner(file)
	var in []string
	for scanner.Scan() {
		i := scanner.Text()
		in = append(in, i)
	}
	return in
}

func main() {
	var a [1012][1012]int
	// fmt.Println(a)
	commands := readInput()
	// for y, row := range a{
	// 	for x,claims := range row{

	// 	}
	// }
	for _, c := range commands {
		_, l, t, w, h := parseCommand(c)
		a = fillSquare(t, l, w, h, a)
	}
	// fmt.Println(a)
	claimCount := 0
	for y := 0; y < 1012; y++ {
		for x := 0; x < 1012; x++ {
			if a[x][y] >= 2 {
				claimCount++
			}
		}
		// fmt.Println(a[y])
	}
	fmt.Println("claims:", claimCount)
	// Find the claim without overlap
	for _, c := range commands {
		hasOverlap := false
		id, l, t, w, h := parseCommand(c)
		for y := t; y < (t + h); y++ {
			for x := l; x < (l + w); x++ {
				if a[y][x] > 1 {
					hasOverlap = true
				}
				// fmt.Println(x, y)
				a[y][x]++
			}
		}
		if !hasOverlap {
			fmt.Println(id)
		}
	}
}

//	claimCount := 0
// for _, c := range commands {
// 	l, t, w, h := parseCommand(c)
// 	for y := t; y < (t + h); y++ {
// 		for x := l; x < (l + w); x++ {
// 			if a[y][x] == 0 {
// 				a[y][x] = 1
// 			} else if a[y][x] == 1 {
// 				claimCount += 1
// 				a[y][x] += 1
// 			}
// 			a[y][x]++
// 		}
// 	}
// }
func fillSquare(t int, l int, w int, h int, Arr [1012][1012]int) [1012][1012]int {
	hasOverlap := true
	for y := t; y < (t + h); y++ {
		for x := l; x < (l + w); x++ {
			if Arr[y][x] > 0 {
				hasOverlap = true
			}
			// fmt.Println(x, y)
			Arr[y][x]++
		}
	}
	if !hasOverlap {
		// fmt.Println("Found a claim with no overlap(as of now) on :", t, l, w, h)
	}
	return Arr
}

func parseCommand(str string) (int, int, int, int, int) {
	var re = regexp.MustCompile(`(?m)#([\d]+) @ ([\d]+),([\d]+): ([\d]+)x([\d]+)`)
	gr := re.FindStringSubmatch(str)
	// fmt.Println(gr)
	id, _ := strconv.Atoi(gr[1])
	t, _ := strconv.Atoi(gr[2])
	l, _ := strconv.Atoi(gr[3])
	w, _ := strconv.Atoi(gr[4])
	h, _ := strconv.Atoi(gr[5])
	// Top, Left, W, H
	return id, t, l, w, h
}
