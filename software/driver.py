#! /usr/bin/
from serial import Serial
from enum import Enum
import struct

class Otamatone_State(Enum):
    IDLE = 0
    PRESS = 1
    HOLD = 2
    RELEASE = 3

class Otamatone:

    STABLE_COUNTDOWN = 32
    RELEASE_COUNTDOWN = 8
    AVG_WINDOW = 1/4 # start averaging at STABLE_COUNTDOWN * (1-AVG_WiNDOW)

    def __init__(self, port):
        self.s = Serial(port, timeout = 0.1)
        self.pos = [0] * 2 # updated on press or release
        self.pos_tmp = 0 # updated on every feedback
        self.pos_sum = 0
        self.stable_cnt = self.STABLE_COUNTDOWN
        self.release_cnt = self.RELEASE_COUNTDOWN

    def read(self):
        rx = self.s.read(2)
        if rx and len(rx) == 2:
            pos = struct.unpack("<H", rx)[0]
            self.pos_tmp = 0
            if pos > 0:
                if self.stable_cnt:
                    # not yet stable
                    self.stable_cnt -= 1
                    if self.stable_cnt < self.STABLE_COUNTDOWN * self.AVG_WINDOW:
                        # accumlate pos
                        self.pos_sum += pos
                elif self.pos[0] == 0:
                    # pressed and stable
                    # print('pressed', pos)
                    self.release_cnt = self.RELEASE_COUNTDOWN
                    pos = int(self.pos_sum / (self.STABLE_COUNTDOWN * self.AVG_WINDOW))
                    self.pos = [pos] + self.pos[0:-1]
                    self.pos_sum = 0
                    return (Otamatone_State.PRESS, pos)
                else:
                    return (Otamatone_State.HOLD, (self.pos[0], pos))
            else:
                if self.release_cnt:
                    self.release_cnt -= 1
                    if self.pos[0] > 0:
                        return (Otamatone_State.HOLD, (self.pos[0], pos))
                    else:
                        return (Otamatone_State.IDLE, 0)
                else:
                    # released
                    self.stable_cnt = self.STABLE_COUNTDOWN
                    self.pos_sum = 0
                    if self.pos[0]:
                        self.pos = [0] + self.pos[0:-1]
                        return (Otamatone_State.RELEASE, 0)
        return (Otamatone_State.IDLE, 0)