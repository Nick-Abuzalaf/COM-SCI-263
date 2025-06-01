import argparse
import os
import subprocess

import pandas as pd

from external.CodeGen.codegen_sources.model.translate import Translator


class TransCoderRunner:
    def __init__(self, model_path, BPE_path, use_gpu=True):
        self.model_path = model_path
        self.translator = Translator(model_path=model_path, BPE_path=BPE_path, gpu=use_gpu)

    def run(self, ds_path: str, output: str, src_lang: str, tgt_lang: str, beam_size: int = 1):
        df = pd.read_csv(ds_path)

        src_col = f"{src_lang}_code"
        tgt_col = f"{tgt_lang}_translated"

        translations = []
        for idx, row in df.iterrows():
            print(f"Translating: {row[src_col]}")
            try:
                translation = self.translator.translate(row[src_col],
                                                        lang1=src_lang,
                                                        lang2=tgt_lang,
                                                        beam_size=beam_size)
                translation = "".join(translation)
            except:
                translation = ""

            print(f"Translation: {translation}")

            translations.append(translation)

        df[tgt_col] = translations

        if os.path.exists(os.path.join(os.path.dirname(ds_path), "output")):
            os.mkdir(os.path.join(os.path.dirname(ds_path), "output"))

        output_path = os.path.join(os.path.dirname(ds_path), "..", "output", f"{output}.csv")
        df.to_csv(output_path, index=False)

    def translate(self, input_code: str, src_lang: str, tgt_lang: str, beam_size: int):
        translation = subprocess.run(args=["python",
                                           "-m", "codegen_sources.model.translate",
                                           "--src_lang", src_lang,
                                           "--tgt_lang", tgt_lang,
                                           "--model_path", self.model_path,
                                           "--beam_size", beam_size],
                                     stdin=input_code,
                                     capture_output=True).returncode
        return translation


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset",
                           default=os.path.join(os.getcwd(), "../dataset/lc_dataset_clean.csv"))
    argparser.add_argument("--output", help="Filename for translation output")

    argparser.add_argument("--model_path", help="Path to model")
    argparser.add_argument("--bpe_path", help="Path to BPE codes",
                           default=os.path.join(os.getcwd(), "external/CodeGen/data/bpe/cpp-java-python/codes"))

    argparser.add_argument("--src_lang", help="Source code language ('java', 'python', or 'cpp')")
    argparser.add_argument("--tgt_lang", help="Translation language ('java', 'python', or 'cpp')")
    argparser.add_argument("--beam_size", help="Beam size", default=1, type=int)
    argparser.add_argument("--use_gpu", help="Whether to use GPU", action="store_true")

    args = argparser.parse_args()

    runner = TransCoderRunner(args.model_path, args.bpe_path, args.use_gpu)
    runner.run(args.ds_path, args.output, args.src_lang, args.tgt_lang)
