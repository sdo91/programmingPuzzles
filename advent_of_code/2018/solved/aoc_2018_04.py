#!/usr/bin/env python3

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print('adding to path: {}'.format(dirToAdd))
        sys.path.insert(0, dirToAdd)
    else:
        print('already in path: {}'.format(dirToAdd))

addToPath('../../..')

### IMPORTS ###

from collections import defaultdict
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    240,
    0,
    0,
]

TEST_OUTPUT_2 = [
    4455,
    0,
    0,
]










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            8421,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            83359,
            self.solve_part_2(puzzle_input)
        )

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_test_case_1(self, test_input: str):
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}\n'.format(test_input))

        solver = Solver(test_input)
        return solver.p1()

    def solve_part_1(self, puzzle_input: str):
        part_1_result = self.solve_test_case_1(puzzle_input)

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_test_case_2(self, test_input: str):
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}\n'.format(test_input))

        solver = Solver(test_input)
        return solver.p2()

    def solve_part_2(self, puzzle_input: str):
        part_2_result = self.solve_test_case_2(puzzle_input)

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Guard(object):
    def __init__(self):
        self.counts = [0] * 60

    def get_sum(self):
        return sum(self.counts)

    def get_max_count(self):
        return max(self.counts)


class Solver(object):

    def __init__(self, text):
        self.text = text
        self.lines = list(sorted(aoc_util.stripped_lines(text)))

    def __repr__(self):
        return '{}: {}'.format(
            type(self).__name__, self.text)

    @staticmethod
    def get_minute(date):
        return aoc_util.ints(date)[-1]

    def parse_text(self):
        guards_by_id = defaultdict(Guard)

        guard_id = -1
        time_asleep = -1
        for line in self.lines:
            date, info = line.split(']')
            if 'Guard' in info:
                guard_id = aoc_util.ints(info)[0]
            elif 'asleep' in info:
                time_asleep = self.get_minute(date)
            elif 'wakes' in info:
                time_awake = self.get_minute(date)
                guard = guards_by_id[guard_id]
                for x in range(time_asleep, time_awake):
                    guard.counts[x] += 1
            else:
                assert False

        return guards_by_id

    def p1(self):
        """
        Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

        In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard
        #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days,
        whereas any other minute the guard was asleep was only seen on one day).

        While this example listed the entries in chronological order, your entries are in the order you found them.
        You'll need to organize them before they can be analyzed.

        What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer
        would be 10 * 24 = 240.)
        """
        guards_by_id = self.parse_text()

        # choose guard
        max_minutes = -1
        max_guard = -1
        for guard_id, guard in guards_by_id.items():
            total_minutes_asleep = guard.get_sum()
            if total_minutes_asleep > max_minutes:
                max_minutes = total_minutes_asleep
                max_guard = guard_id

        # choose minute
        guard = guards_by_id[max_guard]
        max_count = max(guard.counts)
        max_minute = guard.counts.index(max_count)

        # done
        result = max_guard * max_minute
        return result

    def p2(self):
        """
        Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

        In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in
        total. (In all other cases, any guard spent any minute asleep at most twice.)

        What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer
        would be 99 * 45 = 4455.) Returns:

        """
        guards_by_id = self.parse_text()

        # choose guard
        max_count = -1
        max_guard = -1
        for guard_id, guard in guards_by_id.items():
            count = guard.get_max_count()
            if count > max_count:
                max_count = count
                max_guard = guard_id

        # choose minute
        guard = guards_by_id[max_guard]
        max_minute = guard.counts.index(max_count)

        # done
        result = max_guard * max_minute
        return result









if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




