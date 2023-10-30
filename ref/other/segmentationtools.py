from enum import Enum

import numpy as np


class Segment:
    def __init__(self, init_vars=None):
        self.status_flags = Enum("status_flag", ["ERROR", "INITIALIZING", "IDLE", "ACTIVATED"])
        self.status = self.status_flags.INITIALIZING
        self.window_len = 200

        # Noise calculation
        self.NOISE_FLOOR_FOUND = False
        self.noise_floor_search_powers = []
        self.noise_floor_search_idx = 0
        self.NOISE_FLOOR_SEARCH_WINDOW_COUNT = 30
        self.NOISE_FLOOR_AVE_COUNT = 3
        self.MIN_POWER_THRESH = 0
        self.MIN_SNR = 4  # Note this is just v/v ratio, not dB

    def run(self, sig):
        if len(sig) < self.window_len / 2:
            self.status = self.status_flags.ERROR
        else:
            # 1. Determine noise floor before advancing to the next stage
            if not self.NOISE_FLOOR_FOUND:
                self.noise_floor_search_powers.append(np.var(sig))
                self.noise_floor_search_idx += 1
                if self.noise_floor_search_idx > self.NOISE_FLOOR_SEARCH_WINDOW_COUNT:
                    self.noise_floor_search_idx = 0
                    self.NOISE_FLOOR_FOUND = True
                    noise_floor_search_powers_sorted = np.sort(self.noise_floor_search_powers)
                    noise_floor_ave_power = \
                        np.mean(noise_floor_search_powers_sorted[:self.NOISE_FLOOR_AVE_COUNT])

                    # Compute threshold and advance program to next stage
                    self.MIN_POWER_THRESH = noise_floor_ave_power * self.MIN_SNR
                    self.noise_floor_search_powers = []

                    self.status = self.status_flags.IDLE
                else:
                    self.status = self.status_flags.INITIALIZING

            # 2. Start segmenting once noise floor has been determined
            else:
                this_window_var = np.var(sig)
                if self.status is self.status_flags.IDLE and this_window_var > self.MIN_POWER_THRESH:
                    self.status = self.status_flags.ACTIVATED
                elif self.status is self.status_flags.ACTIVATED and this_window_var <= self.MIN_POWER_THRESH:
                    self.status = self.status_flags.IDLE

        return self.status
