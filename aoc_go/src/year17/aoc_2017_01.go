package year17

import (
	"aoc_go/inputs17"
	"aoc_go/util"
	"fmt"
)

var testInputs1 = []string{
	"1122",
	"1111",
	"1234",
	"91212129",
}

var testOutputs1 = []int{
	3,
	4,
	0,
	9,
}

var testInputs2 = []string{
	"1212",
	"1221",
	"123425",
	"123123",
	"12131415",
}

var testOutputs2 = []int{
	6,
	0,
	4,
	12,
	4,
}

func SolveDay01() {
	//fmt.Printf("testInputs1: %v \n", testInputs1)
	//fmt.Printf("testOutputs1: %v \n", testOutputs1)

	for i := range testInputs1 {
		util.TestSolver(p1, testInputs1[i], testOutputs1[i])
	}
	p1Result := p1(inputs17.PuzzleInput01)
    fmt.Printf("p1Result: %d \n", p1Result)

	for i := range testInputs1 {
		util.TestSolver(p2, testInputs2[i], testOutputs2[i])
	}
	p2Result := p2(inputs17.PuzzleInput01)
    fmt.Printf("p2Result: %d \n", p2Result)
}

func p1(text string) int {
	// find the sum of all digits that match the next digit in the list

	// 1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
	// 1111 produces 4 because each digit (all 1) matches the next.
	// 1234 produces 0 because no digit matches the next.
	// 91212129 produces 9 because the only digit that matches the next one is the last digit, 9.

	// fmt.Printf("text: %v \n", text)

	digits := util.ToDigits(text)

	// fmt.Printf("digits: %v \n", digits)

	sum := 0

	for i := range digits {

		digit := digits[i]

		var nextDigit int
		if i == len(digits)-1 {
			nextDigit = digits[0]
		} else {
			nextDigit = digits[i+1]
		}

		// fmt.Printf("digit: %v, next: %v \n", digit, nextDigit)

		if digit == nextDigit {
			sum += digit
		}
	}

	//fmt.Println("sum:", sum)
	return sum
}

func p2(text string) int {
	// Now, instead of considering the next digit, it wants you to consider the digit halfway around the circular list.

	// 1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
	// 1221 produces 0, because every comparison is between a 1 and a 2.
	// 123425 produces 4, because both 2s match each other, but no other digit has a match.
	// 123123 produces 12.
	// 12131415 produces 4.

	digits := util.ToDigits(text)
	numDigits := len(digits)

	sum := 0

	for i := range digits {
		digit := digits[i]
		otherDigitIdx := (i + numDigits / 2) % numDigits
		otherDigit := digits[otherDigitIdx]

		if digit == otherDigit {
			sum += digit
		}
	}

	//fmt.Println("sum:", sum)
	return sum
}
