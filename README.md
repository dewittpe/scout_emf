# scout_emf
possible extension for scout

## Preliminary work

The `EMF_Scout.py` and `EMF_Scout_Functions.py` files are the original outline
for the needed work to be done.  `EMF_Scout.py.log` is a log file from running
the `EMF_Scout.py` script.

The provided scripts and example data files _do not_ run to completion.
Specifically, running:

    time python EMF_Scout.py > EMF_Scout.py.log

results in:

    Traceback (most recent call last):
      File "/Users/pdewitt/opt/anaconda3/envs/scout/lib/python3.9/site-packages/pandas/core/indexes/base.py", line 3361, in get_loc
        return self._engine.get_loc(casted_key)
      File "pandas/_libs/index.pyx", line 76, in pandas._libs.index.IndexEngine.get_loc
      File "pandas/_libs/index.pyx", line 108, in pandas._libs.index.IndexEngine.get_loc
      File "pandas/_libs/hashtable_class_helper.pxi", line 5198, in pandas._libs.hashtable.PyObjectHashTable.get_item
      File "pandas/_libs/hashtable_class_helper.pxi", line 5206, in pandas._libs.hashtable.PyObjectHashTable.get_item
    KeyError: 'Unnamed: 1'

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
      File "/Users/pdewitt/scout_emf/EMF_Scout.py", line 1248, in <module>
        df_filter = df[df['Unnamed: 1']=='Final Energy|Buildings|Commercial|Other|Gas']
      File "/Users/pdewitt/opt/anaconda3/envs/scout/lib/python3.9/site-packages/pandas/core/frame.py", line 3458, in __getitem__
        indexer = self.columns.get_loc(key)
      File "/Users/pdewitt/opt/anaconda3/envs/scout/lib/python3.9/site-packages/pandas/core/indexes/base.py", line 3363, in get_loc
        raise KeyError(key) from err
    KeyError: 'Unnamed: 1'

    real	63m26.338s
    user	63m23.662s
    sys	0m2.018s

## Updated work

@dewittpe was provided with the initial files noted above and has started to
refactor the project.

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
    conda env export --from-history > environment.yml
