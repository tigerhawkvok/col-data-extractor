# col-data-extractor


## What it does

There are several sub-files:

### `clean_source_data.py`

This is the workhorse peice of code. It can be manually configured by changing the defaults at the top. 
This file will read a [delimiter] separated file and clean the input, returning an optional subset of columns.

It can:

- Run specified columns through cleaner functions
- Rename specific columns
- Output only a subset of columns
- Returns a sorted list based on `canonicalColumn`

### `create_csv.py`

This function will walk you through CLI prompts to bring in an input file, and spit out a subsetted output. To run it, run

```
python3 create_csv.py
```

(or just `python` if Python 3.0+ is your default)

### `concat_data.py`

This function will search your directory for all valid filetypes (`xprs`, `csv`, and `tsv`) not created by the application itself and return a single CSV file with the columns side-by-side.

To run it, run

```
python3 concat_data.py
```

(or just `python` if Python 3.0+ is your default)


## TODO

- Mixed filetypes in a directory can cause `concat_data.py` to intermittently crap out
- the `[Y/N]` inputs can require the button to be pressed twice on some systems due to a behaviour change in Python 3.2
- `clean_source_data.py` and `concat_data.py` needs to take in CLI arguments to be wholly called by script
