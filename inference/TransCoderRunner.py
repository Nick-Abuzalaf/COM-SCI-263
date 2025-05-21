import argparse
import os

import pandas as pd

from codegen_sources.model.translate import Translator

class TransCoderRunner:
    def __init__(self, model_path, use_gpu=True):
        self.translator = Translator(model_path=model_path, BPE_path=model_path, gpu=use_gpu)

    def run(self, ds_path: str, src_lang: str, tgt_lang: str):
        df = pd.read_csv(ds_path)

        print("")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset", default=os.path.join(os.getcwd(), "../output/lc_dataset_clean.csv"))
    argparser.add_argument("--model_path", help="Path to model")
    argparser.add_argument("--src_lang", help="Source code language ('java', 'python', or 'cpp')")
    argparser.add_argument("--tgt_lang", help="Translation language ('java', 'python', or 'cpp')")
    argparser.add_argument("--use_gpu", help="Whether to use GPU", type=bool)

    args = argparser.parse_args()

    runner = TransCoderRunner(args.model_path, args.use_gpu)
    runner.run(args.ds_path, args.src_lang, args.tgt_lang)
