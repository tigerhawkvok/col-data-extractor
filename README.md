# col-data-extractor

## Dependencies

The only thing you should need to install is Python 3.5+. To check if you have it, run `python --version` at your terminal. If that isn't 3.5+, try `python3 --version`. If this second command throws an error, you don't have Python 3.x installed.

Install it with Homebrew:

```
brew install python3
```

If you for some reason really can't install Python 3.5+, it should run OK on Python 2, but it has not been extensively debugged and you will miss some functionality (like recursive directory searching).

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

The other two helper functions call this. **If you want to change global behaviour, change the configuration options at the top of this file**.

### `create_csv.py`

This function will walk you through CLI prompts to bring in an input file, and spit out a subsetted output. To run it, run

```
python3 create_csv.py
```

(or just `python` if Python 3.0+ is your default)

### `concat_data.py`

This function will search your directory for all valid filetypes (`xprs`, `csv`, and `tsv`) not created by the application itself and return a single CSV file with the columns side-by-side.

#### Features

- Map a column header automatically based on files found
- Crawls a directory either recursively or shallowly, verifying the file list at runtime

To run it, run

```
python3 concat_data.py
```

(or just `python` if Python 3.0+ is your default)


## TODO

- `clean_source_data.py` and `concat_data.py` needs to take in CLI arguments to be wholly called by script
