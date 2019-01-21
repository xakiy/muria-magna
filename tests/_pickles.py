"""Pickles."""

import pickle
import os

dir = 'tests/.cache'


def _pickling(stuff, filename):
    with open(os.path.join(dir, filename), 'wb') as f:
        pickle.dump(stuff, f, pickle.HIGHEST_PROTOCOL)


def _unpickling(filename):
    with open(os.path.join(dir, filename), 'rb') as f:
        return pickle.load(f)
