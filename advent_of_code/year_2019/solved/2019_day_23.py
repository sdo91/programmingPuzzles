#!/usr/bin/env python3



### IMPORTS ###

import time

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.intcode_computer import IntcodeComputer










class Nic(IntcodeComputer):

    part = ''
    nat_packet = None
    idle_nics = set()
    network = []
    last_y_sent_to_0 = -1

    @classmethod
    def setup(cls, part):
        cls.part = part
        cls.nat_packet = None
        cls.idle_nics.clear()
        cls.network.clear()
        cls.last_y_sent_to_0 = -1

    def __init__(self, initial_memory, address):
        super().__init__(initial_memory)

        self.address = address
        self.queue_input(self.address)

        self.network.append(self)

    @classmethod
    def send_packet(cls, packet):
        dest_addr = packet[0]

        if dest_addr > len(cls.network) - 1:
            AocLogger.log('NAT packet: {}'.format(packet))
            cls.nat_packet = packet
            if cls.part == 'p1':
                raise RuntimeError(packet[2])
            return

        cls.network[dest_addr].queue_input(packet[1])
        cls.network[dest_addr].queue_input(packet[2])
        cls.idle_nics.discard(dest_addr)

    @classmethod
    def process_nat(cls):
        if len(cls.idle_nics) == 50:
            if cls.nat_packet[2] == cls.last_y_sent_to_0 and cls.part == 'p2':
                raise RuntimeError(cls.last_y_sent_to_0)
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
                    # AocLogger.log('{}: no input x1'.format(self.address))
                    self.queue_input(-1)
                    is_first_input = False
                else:
                    # AocLogger.log('{}: no input x2'.format(self.address))
                    self.idle_nics.add(self.address)
                    break
            elif self.is_state(self.STATE_OUTPUT):
                if self.get_output_size() == 3:
                    packet = tuple(self.get_all_output())
                    self.clear_output()
                    self.send_packet(packet)
                    AocLogger.log('{}: sent packet {}'.format(self.address, packet))
                    break










def main():
    print('starting {}'.format(__file__.split('/')[-1]))
    start_time = time.time()

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    aoc_util.assert_equal(
        21664,
        run(puzzle_input)
    )

    AocLogger.verbose = False
    aoc_util.assert_equal(
        16150,
        run(puzzle_input, part='p2')
    )

    elapsed_time = time.time() - start_time
    print('elapsed_time: {:.2f} sec'.format(elapsed_time))


def run(puzzle_input, part='p1'):
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
    AocLogger.log('\npuzzle_input:\n{}\n'.format(puzzle_input))

    # set up the network
    Nic.setup(part)
    for x in range(50):
        Nic(puzzle_input, x)

    # run the network
    try:
        while True:
            for nic in Nic.network:
                nic.process()
                Nic.process_nat()  # check if idle
    except RuntimeError as e:
        result = e.args[0]

    print('{} result: {}\n'.format(part, result))
    return result










if __name__ == '__main__':
    main()




