package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type freqList = []int32

func readInput() []int32 {
	var file, err = os.Open("day1.input")
	if err != nil {
		return []int32{-1}
	}
	var scanner = bufio.NewScanner(file)
	var in []int32
	for scanner.Scan() {
		i, _ := strconv.Atoi(scanner.Text())
		in = append(in, int32(i))
	}
	return in
}
func isInList(a int32, li []int32) bool {
	var hasFound = false
	for _, k := range li {
		if a == k {
			hasFound = true
		}
	}
	return hasFound
}

func mainkkk() {
	// for i, in := range readInput() {
	// 	freq += in
	// 	fmt.Println(i, in)
	// }
	var freqList []int32
	var curFreq int32 = 0
	var count = 0
	frequencies := readInput()
	for !isInList(curFreq, freqList) {
		println(curFreq)
		freqList = append(freqList, curFreq)
		curFreq = curFreq + frequencies[count]
		count = (count + 1) % len(frequencies)
	}
	fmt.Println(curFreq)
}
func main() {
	var freqList = []int32{1, 2, 3, 4, 5}
	println(isInList(1, freqList))
	println(isInList(6, freqList))
	mainkkk()
}
