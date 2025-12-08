from AMMMGlobals import AMMMException

class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Required parameters
        paramList = [
            'instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',

            'K', 'minP', 'maxP', 'minC', 'maxC',

            'N', 'minDist', 'maxDist'
        ]

        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException(f"Parameter({paramName}) missing in config.dat")

        if data.numInstances <= 0:
            raise AMMMException("numInstances must be > 0")

        if data.K <= 0:
            raise AMMMException("K must be > 0")

        if data.N <= 0:
            raise AMMMException("N must be > 0")

        # Ranges validation
        ranges = [
            ('minP','maxP'),
            ('minC','maxC'),
            ('minDist','maxDist')
        ]

        for lo,hi in ranges:
            if getattr(data, lo) > getattr(data, hi):
                raise AMMMException(f"{hi} must be >= {lo}")
