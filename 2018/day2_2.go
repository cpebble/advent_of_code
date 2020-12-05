package main

import (
	"bufio"
	"fmt"
	"os"

	"github.com/texttheater/golang-levenshtein/levenshtein"
)

func readInput() []string {
	var file, err = os.Open("day2.input")
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
	lines := readInput()
	for i, source := range lines {
		for _, target := range lines[i:] {
			a := disBetweenWords(source, target)
			if a == 2 {
				fmt.Printf("FOUND! %s %s", source, target)
			}
		}
		fmt.Printf("\nChecked %s\n", source)
	}

}
func disBetweenWords(a string, b string) int {
	distance := levenshtein.DistanceForStrings([]rune(a), []rune(b), levenshtein.DefaultOptions)
	return distance
}
