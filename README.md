# data-downloader

A simple data processor for the [DesInventar](https://www.desinventar.net).

## Installation

```bash
git clone https://github.com/COMP0016-IFRC-Team5/data-downloader.git
cd data-processor
```

## Requirements

Install dependencies in any preferred way

- Using conda ([Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
```bash
conda env create -f conda_env.yml
conda activate data-processor
```

- Using pip ([Python 3.10+](https://www.python.org/downloads/))
```bash
pip install -r requirements.txt
```

## Usage

This module provides functionality for downloading data from DesInventar to the 
target directory.

You need to download xml and csv files from DesInventar using its corresponding
module.
Then you need to convert xml to csv using `record_converter` module. This step 
may use 60 GB of memory.
Finally, you can use `categoriser` module to generate categorisations for the 
events.

### Note for the `csv_downloader` module
In this code snippet, `target_dir` is the directory where the csv files will be
downloaded to.
```python
import csv_downloader
csv_downloader.start_download(target_dir='./data', mode=0b000)
```

`mode` is an integer from 0 to 7, whose highest bit determines whether ignore
existing spreadsheets and last two bits determine the level of ignoring of
caches.

Let `ignore_cache = mode & 0b011`  
If `ignore_cache` is greater than 0, the crawler will ignore cache in
`caches/disasters.pkl`. If `ignore_cache` is greater than 1, the crawler will
ignore cache in `caches/disasters.pkl` and `caches/disasters/*`.
If `ignore_cache` is greater than 2, all caches will be ignored.

### Example:
See `example.py` for detail.

```bash
python3 example.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- Dekun Zhang    [@DekunZhang](https://www.github.com/DekunZhang)