import setuptools

long_description = "Scout is a python package that estimates the impacts of various energy conservation measures (ECMs) in the U.S. residential and commercial building sectors. Scout evaluates the energy savings, avoided CO<sub>2</sub> emissions, operating cost reductions, and cost-effectiveness (using several metrics) of each ECM under multiple technology adoption scenarios. These results are obtained for the entire U.S., and also broken out by climate zone, building class (i.e., new/existing, residential/commercial), and end use."

setuptools.setup(
        name = "scout",
        version = "0.0.1",
        author = "Peter E. DeWitt, Chioke Harris, Jared Langevin",
        author_email = "peter.dewitt@nrel.gov, chioke.harris@nrel.gov, jarad.langevin@lbl.gov",
        description = "Estimate impacts of Energy Conservation Measures in the U.S. residential and commercial building sectors.",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/dewittpe/scout_emf",
        packages = setuptools.find_packages(),
        python_requires = '>=3.6',
        package_data = {'': ['supporting_data/convert_data/*.json', 'supporting_data/stock_energy_tech_data/*.gz', 'Results_Files_3/*.gz']},
        )
