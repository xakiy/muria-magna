"""Pickles."""

import pickle


def _pickling(stuff, filename):
    with open(filename, 'wb') as f:
        pickle.dump(stuff, f, pickle.HIGHEST_PROTOCOL)


def _unpickling(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
