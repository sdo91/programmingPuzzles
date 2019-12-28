#!/usr/bin/env python3



### IMPORTS ###

import time
import numpy as np

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer





### CONSTANTS ###

TEST_INPUT = [
    """

    """, """

    """, """

    """
]





class Nic(IntcodeComputer):

    is_done = False
    nat_packet = None
    idle_nics = set()
    network = []
    last_y_sent_to_0 = -1

    def __init__(self, initial_memory, address):
        super().__init__(initial_memory)

        self.address = address
        self.queue_input(self.address)

        self.network.append(self)

    @classmethod
    def send_packet(cls, packet):
        dest_addr = packet[0]

        if dest_addr > len(cls.network) - 1:
            print('NAT packet: {}'.format(packet))
            cls.nat_packet = packet
            # raise RuntimeError('part 1: {}'.format(packet[2]))
            return

        cls.network[dest_addr].queue_input(packet[1])
        cls.network[dest_addr].queue_input(packet[2])
        cls.idle_nics.discard(dest_addr)

    @classmethod
    def process_nat(cls):
        if len(cls.idle_nics) == 50:
            if cls.nat_packet[2] == cls.last_y_sent_to_0:
                raise RuntimeError('part 2: {}'.format(cls.last_y_sent_to_0))
            cls.last_y_sent_to_0 = cls.nat_packet[2]
            packet = (0, cls.nat_packet[1], cls.nat_packet[2])
            cls.send_packet(packet)

    def process(self):
        is_first_input = True

        while True:
            self.run()

            if self.is_state(self.STATE_HALTED):
                print('{}: halted'.format(self.address))
                break
            elif self.is_state(self.STATE_INPUT_NEEDED):
                if is_first_input:
                    print('{}: no input x1'.format(self.address))
                    self.queue_input(-1)
                    # todo: break here?
                    is_first_input = False
                else:
                    print('{}: no input x2'.format(self.address))
                    self.idle_nics.add(self.address)
                    break
            elif self.is_state(self.STATE_OUTPUT):
                if self.get_output_size() == 3:
                    packet = tuple(self.get_all_output())
                    self.clear_output()
                    self.send_packet(packet)
                    print('{}: sent packet {}'.format(self.address, packet))
                    break


        z=0






def main():
    print('starting {}'.format(__file__.split('/')[-1]))
    start_time = time.time()

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    # AocLogger.verbose = True
    # run_tests()

    AocLogger.verbose = False

    solve_part_1(puzzle_input)

    # aoc_util.assert_equal(
    #     0,
    #     solve_part_1(puzzle_input)
    # )

    elapsed_time = time.time() - start_time
    print('elapsed_time: {:.2f} sec'.format(elapsed_time))


# def run_tests():
#     aoc_util.assert_equal(
#         42,
#         solve_test_case(TEST_INPUT[0])
#     )
#
#
# def solve_test_case(test_input):
#     test_input = test_input.strip()
#     AocLogger.log('test_input:\n{}'.format(test_input))
#
#     result = 0
#
#     print('solve_test_case: {}'.format(result))
#     return result


def solve_part_1(puzzle_input):
    """
    --- Part Two ---
    Packets sent to address 255 are handled by a device called a NAT (Not Always Transmitting).
    he NAT is responsible for managing power consumption of the network by blocking certain packets and watching for
    idle periods in the computers.

    If a packet would be sent to address 255, the NAT receives it instead.
    The NAT remembers only the last packet it receives; that is,
    the data in each packet it receives overwrites the NAT's packet memory with the new packet's X and Y values.

    The NAT also monitors all computers on the network. If all computers have empty incoming packet queues and are
    continuously trying to receive packets without sending packets, the network is considered idle.

    Once the network is idle, the NAT sends only the last packet it received to address 0;
    this will cause the computers on the network to resume activity.
    In this way, the NAT can throttle power consumption of the network when the ship needs power in other areas.

    Monitor packets released to the computer at address 0 by the NAT.
    What is the first Y value delivered by the NAT to the computer at address 0 twice in a row?
    """
    puzzle_input = puzzle_input.strip()
    AocLogger.log('puzzle_input:\n{}'.format(puzzle_input))

    for x in range(50):
        Nic(puzzle_input, x)

    while not Nic.is_done:
        for nic in Nic.network:
            if Nic.is_done:
                break

            nic.process()

            # check if idle
            Nic.process_nat()


    result = 0

    print('solve_part_1: {}'.format(result))
    return result





if __name__ == '__main__':
    main()




