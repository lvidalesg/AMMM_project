import os, random
from AMMMGlobals import AMMMException

class InstanceGenerator(object):

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        prefix = self.config.fileNamePrefix+"_K"+str(self.config.K)+"_N"+str(self.config.N)
        ext = self.config.fileNameExtension
        numInstances = self.config.numInstances

        K = self.config.K
        minP = self.config.minP
        maxP = self.config.maxP
        minC = self.config.minC
        maxC = self.config.maxC

        minR = 1
        maxR = 49

        minA = 2
        maxA = 6

        N = self.config.N
        minDist = self.config.minDist
        maxDist = self.config.maxDist

        if not os.path.isdir(instancesDirectory):
            raise AMMMException(f"Directory({instancesDirectory}) does not exist")

        for inst in range(numInstances):
            filePath = os.path.join(instancesDirectory, f"{prefix}_{inst}.{ext}")
            f = open(filePath, "w")

            # Generate K model parameters (TODOS reales con 2 decimales)
            P = [random.randint(minP, maxP) for _ in range(K)]   
            R = [random.randint(minR, maxR) for _ in range(K)]
            A = [random.randint(minA, maxA) for _ in range(K)]  
            C = [random.randint(minC, maxC) for _ in range(K)]

            # Generate M matrix (NxN symmetric distances)
            M = [[int(0)]*N for _ in range(N)]
            for i in range(N):
                for j in range(i+1, N):
                    d = min(random.randint(minDist, maxDist),50)
                    M[i][j] = d
                    M[j][i] = d

            # Write instance
            f.write(f"K={K};\n")
            f.write(f"N={N};\n")

            f.write("P=[%s];\n" % (" ".join(map(str,P))))
            f.write("R=[%s];\n" % (" ".join(map(str,R))))
            f.write("A=[%s];\n" % (" ".join(map(str,A))))
            f.write("C=[%s];\n" % (" ".join(map(str,C))))

            # Write matrix M with 2 decimals
            f.write("M=[\n")
            for i in range(N):
                row = "[ " + " ".join(f"{M[i][j]}" for j in range(N)) + " ]"
                f.write(f"{row}\n")
            f.write("];\n")

            f.close()
