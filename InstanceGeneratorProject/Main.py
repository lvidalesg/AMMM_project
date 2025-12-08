import sys
from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from InstanceGeneratorProject.ValidateConfig import ValidateConfig
from InstanceGeneratorProject.InstanceGenerator import InstanceGenerator

def run():
    try:
        configFile = "InstanceGeneratorProject/config/config.dat"
        print("AMMM Instance Generator")
        print("-----------------------")
        print(f"Reading config file {configFile}...")

        config = DATParser.parse(configFile)
        ValidateConfig.validate(config)

        print("Generating instances...")
        inst = InstanceGenerator(config)
        inst.generate()

        print("Done.")
        return 0

    except AMMMException as e:
        print("Exception: %s" % e)
        return 1

if __name__ == '__main__':
    sys.exit(run())
