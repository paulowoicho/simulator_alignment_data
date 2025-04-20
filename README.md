# Simulator Alignment Data

This repository contains data used in the [Simulator Alignment Project](https://github.com/paulowoicho/simulator_alignment).

## Data

The data can be found in `/data`. It contains query, passage, relevance triplets (with some metadata) in `.jsonlines` format for the CAsT and iKAT collections.

If you would like to recreate the data...

1. Create a virtual environment and install dependencies:
```bash
uv venv --python 3.12.4
source .venv/bin/activate
uv sync
```

2. Then prepare the data with:
```bash
python3 scripts/prep_data.py
```