import random


class Fringe(object):
    def __init__(self):
        self.unsat = list()
        self.errored = list()
        self.avoided = list()
        self._deferred = dict()
        self.last_added = None

    def __str__(self):
        return "<Fringe id: 0x%x, unsat: %d, errored: %d, avoided: %d, deferred: %d>" % (
            id(self), len(self.unsat), len(self.errored), len(
                self.avoided), len(self.deferred)
        )

    def __repr__(self):
        return self.__str__()

    @property
    def deferred(self):
        res = list()
        for addr in self._deferred:
            res.extend(self._deferred[addr])
        return res

    @property
    def num_states(self):
        return len(self.unsat) + len(self.errored) + \
            len(self.avoided) + len(self.deferred)

    def is_empty(self):
        return len(self._deferred) == 0

    def get_deferred_by_address(self, address):
        if address in self._deferred:
            res = self._deferred[address].pop()
            if len(self._deferred[address]) == 0:
                del self._deferred[address]
            return res
        return None

    def get_all_deferred_by_address(self, address):
        if address in self._deferred:
            res = self._deferred[address]
            del self._deferred[address]
            return res
        return None

    def get_one_deferred(self):
        assert not self.is_empty()
        addr, states = self._deferred.popitem()
        state = states.pop()
        if states:
            self._deferred[addr] = states
        return state

    def get_random_deferred(self):
        assert not self.is_empty()
        addresses = list(self._deferred.keys())
        random.shuffle(addresses)
        random_address = addresses[0]
        states = self._deferred[random_address]
        random.shuffle(states)
        random_state = states.pop()
        if not states:
            del self._deferred[random_address]

        return random_state

    def add_deferred(self, state):
        self.last_added = state
        if state.get_ip() not in self._deferred:
            self._deferred[state.get_ip()] = [state]
        else:
            self._deferred[state.get_ip()].append(state)

    def add_errored(self, state):
        self.errored.append(state)

    def add_unsat(self, state):
        self.unsat.append(state)

    def add_avoided(self, state):
        self.avoided.append(state)
