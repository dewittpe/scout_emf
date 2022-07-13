# scout_emf
Possible extension/refactor for [scout](https://github.com/trynthink/scout)

## A python package
[![scout-package-tests](https://github.com/dewittpe/scout_emf/actions/workflows/tox.yml/badge.svg?branch=main)](https://github.com/dewittpe/scout_emf/actions/workflows/tox.yml)
[![codecov](https://codecov.io/gh/dewittpe/scout_emf/branch/main/graph/badge.svg?token=zUXw1hToQa)](https://codecov.io/gh/dewittpe/scout_emf)

The python package scout has been built to give end users access to the tools
needed to estimate the impacts of various energy conservation measures (ECMs) in
the U.S. residential and commercial building sectors. Scout evaluates the energy
savings, avoided CO<sub>2</sub> emissions, operating cost reductions, and
cost-effectiveness (using several metrics) of each ECM under multiple technology
adoption scenarios. These results are obtained for the entire U.S., and also
broken out by climate zone, building class (i.e., new/existing,
residential/commercial), and end use.

To install the development version:
1. Clone this repo.
3. Evaluate `python setup.py install`

## Development Environment

The `environment.yml` file defines a conda environment with the needed modules
and packages for working on scout and this possible emf extension.

    # build the environment
    conda env create -f environment.yml

    # activate the environment
    conda activate scout

## Example Use

### Dash App

An interactive [Dash](https://plotly.com/dash/) application is being developed
to allow end users to explore results of the `ecm_prep` and `ecm_results` json
files graphically.

```bash
./dash-test.py -r <path to a ecm_result file> -p <path to ecm_prep file>
```

More details can be found the help:
```bash
./dash-test.py -h
```


