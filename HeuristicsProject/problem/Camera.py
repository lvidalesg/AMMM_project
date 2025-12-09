class Camera(object):
    def __init__(self, cameraId, price, cameraRange, autonomy, cost):
        self._cameraId = cameraId
        self._price = price
        self._range = cameraRange
        self._autonomy = autonomy
        self._cost = cost

    def getId(self):
        return self._cameraId

    def getPrice(self):
        return self._price

    def getRange(self):
        return self._range

    def getAutonomy(self):
        return self._autonomy

    def getCost(self):
        return self._cost

    def __str__(self):
        return "cameraId: %d (price: %f, range: %f, autonomy: %f, cost: %f)" % (self._cameraId, self._price, self._range, self._autonomy, self._cost)
