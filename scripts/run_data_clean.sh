#!/bin/bash

PATH_TO_SCRIPT="$(realpath "${BASH_SOURCE[-1]}")"
SCRIPT_DIRECTORY="$(dirname "$PATH_TO_SCRIPT")"

source "${SCRIPT_DIRECTORY}/config.conf"

source "${SCRIPT_DIRECTORY}/../venv/Scripts/activate"
export PATH="`python3 -m site --user-base`/bin:$PATH"
export PYTHONPATH="${SCRIPT_DIRECTORY}/../"

which python3

python3 "${SCRIPT_DIRECTORY}/../data_processing/DataProcessor.py" --output "${DATASET_PATH}"