import setuptools

with open("scout_pkg_readme.md", "r") as fh:
    long_description = fh.read()

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
        )
