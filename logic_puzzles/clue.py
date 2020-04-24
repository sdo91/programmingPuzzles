#!/usr/bin/env python3

import time
from itertools import permutations










class Solver(object):

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        self.solve()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def solve(self):
        """
        One rainy evening, Mr. Body killed 5 people at Clue Mansion. The people killed were Mrs. White, Mr. Green,
        Professor Plum, Colonel Mustard, and Ms. Scarlet. The murders took place in the kitchen, billiards room,
        conservatory, hall, and library. No two people were murdered with the same weapon. The weapons were
        candlestick, rope, revolver, knife, and lead pipe. From the clues given, try to determine the room in which
        each person was killed and the weapon used.

        1. The murder with the lead pipe was not done in the hall or the library.
        2. Mr. Green was not murdered in the kitchen.
        3. The rope was not the murder weapon used in the library.
        4. Neither Mrs. White nor Ms. Scarlet were murdered with the candlestick, the revolver, or the lead pipe.
        5. The person who was murdered in the billiards room had just finished having dinner with Ms. Scarlet,
                Mr. Green, the person done in with the candlestick, and the victim of the rope.
        6. Neither Mr. Green nor Professor Plum were killed with the lead pipe, in the hall, or in the library.
        """

        people = ('white', 'green', 'plum', 'mustard', 'scarlet')
        places_start = ['kitchen', 'billiards', 'conservatory', 'hall', 'library']
        things_start = ['candlestick', 'rope', 'revolver', 'knife', 'pipe']

        matches = []

        white_idx = people.index('white')
        green_idx = people.index('green')
        plum_idx = people.index('plum')
        scarlet_idx = people.index('scarlet')

        for places in permutations(places_start):
            kitchen_idx = places.index('kitchen')
            billiards_idx = places.index('billiards')
            hall_idx = places.index('hall')
            library_idx = places.index('library')

            for things in permutations(things_start):
                candlestick_idx = things.index('candlestick')
                rope_idx = things.index('rope')
                revolver_idx = things.index('revolver')
                pipe_idx = things.index('pipe')

                # rule 1
                if pipe_idx == hall_idx or pipe_idx == library_idx:
                    continue

                # rule 2
                if green_idx == kitchen_idx:
                    continue

                # rule 3
                if rope_idx == library_idx:
                    continue

                # rule 4
                blacklist = {candlestick_idx, revolver_idx, pipe_idx}
                if white_idx in blacklist or scarlet_idx in blacklist:
                    continue

                # rule 5
                dinner_guests = {billiards_idx, scarlet_idx, green_idx, candlestick_idx, rope_idx}
                if len(dinner_guests) != 5:
                    continue

                # rule 6
                blacklist = {pipe_idx, hall_idx, library_idx}
                if green_idx in blacklist or plum_idx in blacklist:
                    continue

                # found a match
                print(people)
                print(places)
                print(things)
                matches.append((people, places, things))

        num_matches = len(matches)
        print('num_matches: {}'.format(num_matches))
        assert num_matches == 1













if __name__ == '__main__':
    instance = Solver()
    instance.run()




