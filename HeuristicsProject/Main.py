from argparse import ArgumentParser
from pathlib import Path

import sys

from HeuristicsProject.datParser import DATParser
from AMMMGlobals import AMMMException
from HeuristicsProject.BRKGA_fwk.solver_BRKGA import Solver_BRKGA
from HeuristicsProject.validateInputDataP2 import ValidateInputData
from HeuristicsProject.ValidateConfig import ValidateConfig
from HeuristicsProject.solvers.solver_Greedy import Solver_Greedy
from HeuristicsProject.solvers.solver_GRASP import Solver_GRASP
from HeuristicsProject.solvers.decoder_BRKGA import Decoder
from HeuristicsProject.problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    solver = Solver_Greedy(self.config, instance)
                elif self.config.solver == 'GRASP':
                    solver = Solver_GRASP(self.config, instance)
                elif self.config.solver == 'BRKGA':
                    verbose = self.config.verbose
                    self.config.verbose = False
                    greedy = Solver_Greedy(self.config, instance)
                    initialSolution = greedy.solve(solver='Greedy', localSearch=False)
                    self.config.verbose = verbose
                    decoder = Decoder(self.config, instance)
                    solver = Solver_BRKGA(decoder, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                solution = solver.solve(solution=initialSolution)

                print('Solution:')
                if hasattr(solution, 'assignments'):
                    for idx, (modelId, crossingId, pattern) in enumerate(solution.assignments):
                        days_on = [str(i+1) for i, val in enumerate(pattern) if val == 1]
                        print(f'  Assignment {idx+1}: Model {modelId+1} -> Crossing {crossingId+1}, Days: {", ".join(days_on)} (pattern: {pattern})')
                
                if hasattr(solution, 'coveredCrossingDays'):
                    covered = len(solution.coveredCrossingDays)
                    total = len(solution.crossings) * solution.DAYS
                    print('Covered crossing-day pairs: %d / %d' % (covered, total))

                solution.saveToFile(self.config.solutionFile)
            else:
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Lab Heuristics')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))
