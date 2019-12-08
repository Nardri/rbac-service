"""FireBase fancy ID generator"""

import random
import time
import numpy


class PushID(object):
    """FireBase fancy ID generator"""
    # Modeled after base64 web-safe chars, but ordered by ASCII.
    PUSH_CHARS = ('-0123456789'
                  '_ABCDEFGHIJKlmnopqrstuvwxyz'
                  'abcdefghijkLMNOPQRSTUVWXYZ')

    def __init__(self):

        # Timestamp of last push, used to prevent local collisions if you
        # pushtwice in one ms.
        self.lastPushTime = 0

        # We generate 72-bits of randomness which get turned into 12
        # characters and appended to the timestamp to prevent
        # collisions with other clients.  We store the last characters
        # we generated because in the event of a collision, we'll use
        # those same characters except "incremented" by one.
        self.lastRandChars = numpy.empty(12, dtype=int)

    def next_id(self):
        """

        Returns:
            String

        """
        now = int(time.time() * 1000)
        duplicate_time = (now == self.lastPushTime)
        self.lastPushTime = now
        time_stamp_chars = numpy.empty(8, dtype=str)

        for i in range(7, -1, -1):
            time_stamp_chars[i] = self.PUSH_CHARS[now % 64]
            now = int(now / 64)

        if now != 0:
            raise ValueError('We should have converted the entire timestamp.')

        unique_id = ''.join(time_stamp_chars)

        if not duplicate_time:
            for i in range(12):
                self.lastRandChars[i] = int(random.random() * 64)
        else:
            # If the timestamp hasn't changed since last push, use the
            # same random number, except incremented by 1.
            for i in range(11, -1, -1):
                if self.lastRandChars[i] == 63:
                    self.lastRandChars[i] = 0
                else:
                    break
            self.lastRandChars[i] += 1

        for i in range(12):
            unique_id += self.PUSH_CHARS[self.lastRandChars[i]]

        if len(unique_id) != 20:
            raise ValueError('Length should be 20.')

        return unique_id
