# AMMM Instance Generator

This project generates random instances for the camera coverage problem on nodes. You can customize the size and parameters of the instances via the `config.dat` file.

## Getting Started

### Installation
1. Clone or download this repository
2. Edit `config.dat` to customize instance parameters


### How to Run

Open a terminal in the project folder and run the instance generator:
```bash
python -m InstanceGeneratorProject.Main
```

The generated instances will be saved in the folder specified by `instancesDirectory` in `config.dat`.

Generated instances will be saved to the output directory.

### Configuration (`config.dat`)

This file controls the parameters of the instance generator. You can modify these values to create instances of the size and difficulty you want.

| Section          | Parameter              | Description                                           | Example                         |
|------------------|------------------------|-------------------------------------------------------|---------------------------------|
| General Settings | `instancesDirectory`   | Folder where generated instances are saved            | InstanceGeneratorProject/output |
|                  | `fileNamePrefix`       | Prefix for generated files                            | camera                          |
|                  | `fileNameExtension`    | File extension                                        | dat                             |
|                  | `numInstances`         | Number of instances to generate                       | 1                               |
| Camera Models    | `K`                    | Number of camera types                                | 3                               |
|                  | `minP`                 | Minimum fixed cost per camera type                    | 200                             |
|                  | `maxP`                 | Maximum fixed cost per camera type                    | 1000                            |
|                  | `minC`                 | Minimum daily cost per camera type                    | 10                              |
|                  | `maxC`                 | Maximum daily cost per camera type                    | 70                              |
| Crossings        | `N`                    | Number of crossings                                   | 10                              |
|                  | `minDist`              | Minimum distance between crossings                    | 0                               |
|                  | `maxDist`              | Maximum distance between crossings                    | 100                             |


## Output
Instances are generated in a standard format compatible with optimization solvers.