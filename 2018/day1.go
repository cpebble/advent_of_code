package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func readInput() []int {
	var file, err = os.Open("day1.input")
	if err != nil {
		return []int{-1}
	}
	var scanner = bufio.NewScanner(file)
	var in []int
	for scanner.Scan() {
		i, _ := strconv.Atoi(scanner.Text())
		in = append(in, i)
	}
	return in
}

func main() {
	println("Hei")
	freq := 0
	for i, in := range readInput() {
		freq += in
		fmt.Println(i, in)
	}
	fmt.Println(freq)
}
