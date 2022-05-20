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

    # export an active environment (do this if you add or update packages)
    # __NOTE:__  The following will include a `prefix:` line that should be
    # manually removed from environment.yml
    # versions should be set to >= or removed from the file so that the
    # environment will build on mutlple platforms.
    conda env export --no-builds > environment.yml

    # updating requirements.txt, if needed/wanted, the conda env export is
    # sufficient.
    pip freeze > requirements.txt

## Example Use

See `example_use.py`

