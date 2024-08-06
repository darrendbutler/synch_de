# synch_de

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Investigating Distance Learning

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│   │                     the creator's initials, and a short `-` delimited description, e.g.
│   │                     `1.0-jqp-initial-data-exploration`.
│   ├── exploratory    <- Contains initial explorations
│   └── for_reports    <- Contains more polished work that can be exported as html or PDF to  
│                         the reports/ directory
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         synch_de and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── synch_de   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes synch_de a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## Installation Instructions

This code base follows practices from version 2 of the [cookie cutter data science](https://cookiecutter-data-science.drivendata.org/) practices. Please conduct the following steps:

### Clone the repository

```{sh}
git clone <repository link>
```

### Create conda environment

Please install [Conda](https://docs.conda.io/projects/conda/en/stable/index.html) if not already installed.
Conda provides package, dependency, and environment management for any language. You must be familiar with managing conda environments and installing packages.

#### Using the Makefile

We use [Make](https://www.gnu.org/software/make/) to manage steps that depend on each other. We strongly recommend using the Makefile to manage setup for consistency and reproducibility across machines.

GNU Make is a tool which controls the generation of executables and other non-source files of a program from the program's source files. Make gets its knowledge of how to build your program from a file called the makefile, which lists each of the non-source files and how to compute it from other files. When you write a program, you should write a makefile for it, so that it is possible to use Make to build and install the program.

Make is typically preinstalled on Mac. Windows users should install Make first if not already installed using [chocolatey](https://community.chocolatey.org/packages/make).

```{sh}
make create_environment       # Set up and enter python interpreter environment
make requirements             # Install Python Dependencies
```

## Best Practices

We follow best practices for maintaining code and communicating. Please refer to the following articles.

Please read the [opinions](https://cookiecutter-data-science.drivendata.org/opinions/) of cookie cutter data science.

- Start from source code.
- [nbautoexport](https://github.com/drivendataorg/nbautoexport)- Converting Exploratory Notebooks to Scripts for Code Review
- Clean Code ML - Best practices on writing maintainable and clear data science code
  - [8 min article](https://www.thoughtworks.com/insights/blog/coding-habits-data-scientists)
  - [Tutorial on Github](https://github.com/davified/clean-code-ml?tab=readme-ov-file)
