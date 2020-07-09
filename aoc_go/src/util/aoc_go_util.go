package util

import (
	"fmt"
	"strconv"
)

type aocSolverFunc func(string) int

func TestSolver(solver aocSolverFunc, input string, expectedOutput int) {
	actualOutput := solver(input)
	if actualOutput != expectedOutput {
		err := fmt.Sprintf("f(%v) returns %v, expected %v", input, actualOutput, expectedOutput)
		panic(err)
	}
}

func ToDigits(text string) []int {
	result := []int{}
	// fmt.Println(result)

	for _, c := range text {
		asChar := string(c)
		asDigit, err := strconv.Atoi(asChar)
		if err != nil {
			panic(err)
		}
		// fmt.Printf("%v, %c, %v, %v \n", i, c, asChar, asDigit)
		result = append(result, asDigit)
	}

	// fmt.Println(result)
	return result
}
