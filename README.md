# Simulator Alignment Data

This repository contains data used in the [Simulator Alignment Project](https://github.com/paulowoicho/simulator_alignment).

## Data

The data can be found in `/data`. It contains 7500 query, passage, relevance triplets each (with some metadata) in `.jsonlines` format for the CAsT and iKAT collections.

If you would like to recreate the data...

1. Create a virtual environment and install dependencies:
```bash
uv venv --python 3.12.4
source .venv/bin/activate
uv sync
```

2. Then prepare the data with (ensure to set the relevant paths to queries, qrels, and indices for benchmarks you want to generate data for):
```bash
python3 prep_data.py
```