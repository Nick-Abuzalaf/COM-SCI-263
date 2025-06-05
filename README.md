# COM-SCI-263 Final Project
## Evaluating the Limitations of Code Translation LLMs
Nick Abuzalaf, Jett Appel, Yu Chan, Liam Mohan


## Enviornment Setup
For any issues setting up the environment, please reach out to Nick at: nabuzalaf1@g.ucla.edu

This project was set up on a Windows machine using Windows Subsystem for Linux. All dependencies are documented but 
environment setup may be slightly different for a different operating system.

This project extends upon the CodeGen project in order to perform inference using the TransCoder model. The CodeGen 
project is included in the top-level "external" folder. As such, both the source of this project (/path/to/COM-SCI-263)
and the path to CodeGen (/path/to/COM-SCI-263/external/CodeGen) need to be added to the PYTHONPATH environment variable
for the code to function properly, such as with:

> export PYTHONPATH=$PYTHONPATH:/path/to/COM-SCI-263:/path/to/COM-SCI-263/external/CodeGen

External dependencies for this project are listed in the requirements.txt file at the top level of this project. These 
dependencies should be installed using pip/pip3 as follows:

> pip install -r requirements.txt

Some other dependencies are required for using the CodeGen project. Instructions for setting up the environment for 
CodeGen can be found at "/path/to/COM-SCI-263/external/CodeGen/README.md"

## Models

The TransCoder models can be downloaded using the following links:
 - [TransCoder_model_1](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth) for Java -> Python
 - [TransCoder_model_2](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_2.pth) for C++ -> Python
 - [translator_transcoder_size_from_DOBF](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/translator_transcoder_size_from_DOBF.pth) for better Java -> Python results

No model downloaded is needed for GPT as these make use of the available APIs.

## Dataset

The Leetcode dataset is obtained automatically from HuggingFace via the script at 
/path/to/COM-SCI-263/data_procesing/DataProcessor.py

This script accepts one argument "--output," which defaults to /path/to/COM-SCI-263/dataset/lc_dataset_clean.csv, 
though this can changed if desired. However, the instructions in this README will assume this file is at the default 
location, so make note if modifying this argument.

## Reproducing Our Results

### GPT

For running inference and metric evaluation for GPT, a Python notebook is available at 
/path/to/COM-SCI-263/inference/CS263_Final_Project_to_Python_w_GPT.ipynb. This notebook expects to be run from Google 
Colab as well as to have the cleaned dataset (by default at /path/to/COM-SCI-263/dataset/lc_dataset_clean.csv) uploaded.
Otherwise, the notebook does not require additional set up and will install external packages as needed.

*Note that there is a minimal financial cost in order to use the GPT APIs within this notebook.

### TransCoder

Separate scripts are used for running inference, unittest-based accuracy, and CodeBLEU metrics for TransCoder.

#### Inference

The inference script for TransCoder is located at /path/to/COM-SCI-263/inference/TransCoderRunner.py and accepts the 
following arguments (with default paths relative to the inference script).

| Arg          | Description                                       | Default                                            |
|--------------|---------------------------------------------------|----------------------------------------------------|
| --ds_path    | Path to cleaned dataset                           | ../dataset/lc_dataset_clean.csv                    |
| --output     | Filename for translation output                   | n/a                                                |
| --model_path | Path to TransCoder ".pth" file                    | n/a                                                |
| --bpe_path   | Path to BPE codes from CodeGen                    | ../external/CodeGen/data/bpe/cpp-java-python/codes |
| --src_lang   | Source code language ('java', 'python', or 'cpp') | n/a                                                |
| --tgt_lang   | Translation language ('java', 'python', or 'cpp') | n/a                                                |
| --beam_size  | Beam size to use in translation                   | 1                                                  |
| --use_gpu    | Flag for whether to use GPU for inference         | False                                              |

A minimal example for invoking this script for translation from Java to Python would be as follows:

> python /path/to/COM-SCI-263/inference/TransCoderRunner.py --output /path/to/dataset/lc_translated_java_python.csv --model_path /path/to/model.pth --src_lang java --tgt_lang python

#### Unittest Accuracy

The unittest accuracy script is located at /path/to/COM-SCI-263/metrics/utils/TestRunner.py and accepts the following 
arguments (with default paths relative to the test script).


| Arg        | Description                                   | Default      |
|------------|-----------------------------------------------|--------------|
| --ds_path  | Path to translated dataset                    | n/a          |
| --output   | Filename for output evaluation results output | n/a          |
| --test_dir | Directory where test files are located        | ../unittests |       

A minimal example for invoking this script for evaluating translations from Java to Python would be as follows:

> python /path/to/COM-SCI-263/metrics/utils/TestRunner.py --ds_path /path/to/dataset/lc_translated_java_python.csv --output java_python_results

This command will print accuracy scores based on question difficult to the console as well as save a file to 
/path/to/dataset/java_python_results.json containing the counts of correct translations, error translations, 
total translations for further information.

#### CodeBLEU

The CodeBLEU metrics script is located at /path/to/COM-SCI-263/metrics/utils/CodeBLEU.py and accepts the following 
argument.

| Arg        | Description                                   | Default      |
|------------|-----------------------------------------------|--------------|
| --ds_path  | Path to translated dataset                    | n/a          |

A minimal example for invoking this script for evaluating translations from Java to Python would be as follows:

> python /path/to/COM-SCI-263/metrics/utils/CodeBLEU.py --ds_path /path/to/dataset/lc_translated_java_python.csv

This command will evaluate the CodeBLEU metrics for the given input and print the results to console.

#### Visualization

Additionally, a visualization script is available at /path/to/COM-SCI-263/metrics/utils/TranslationPrinter.py and 
accepts the following arguments.


| Arg        | Description                                            | Default |
|------------|--------------------------------------------------------|---------|
| --ds_path  | Path to translated dataset                             | n/a     |
| --output   | Filename for translation output                        | n/a     |
| --src_lang | Optional source language that code was translated from | n/a     |   

A minimal example for invoking this script for visualizing translations from Java to Python would be as follows:

> python /path/to/COM-SCI-263/metrics/utils/TranslationPrinter.py --ds_path /path/to/dataset/lc_translated_java_python.csv --output java_python_translations --src_lang java

This command will produce a file at /path/to/dataset/java_python_translations.txt that contains grouped sets of source 
language code, translated code, and original target language code for easier qualitative analysis of translation output.

