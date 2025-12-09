
class Crossing(object):
    def __init__(self, crossingId):
        self._crossingId = crossingId
        self.gene = 1

    def getId(self):
        return self._crossingId

    def __str__(self):
        return "crossingId: %d" % self._crossingId
