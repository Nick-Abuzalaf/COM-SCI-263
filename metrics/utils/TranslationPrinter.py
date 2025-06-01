import argparse
import os

import pandas as pd

class TranslationPrinter:
    def __init__(self):
        pass

    def print(self, ds_path, output, src_lang=None):
        df = pd.read_csv(ds_path)

        files = [f for f in os.listdir("../unittests/") if os.path.isfile(os.path.join(os.getcwd(), "../unittests/", f))]
        ids = sorted([int(f.split("id")[-1].split(".json")[0]) for f in files])

        df = df[df["id"].isin(ids)]

        with open(os.path.join(os.path.dirname(ds_path), f"{output}.txt"), "w") as f:
            for _, row in df.iterrows():
                self.formatted_print(row, f, src_lang)

    @staticmethod
    def formatted_print(row, f, src_lang=None):
        print("".join(["#"]*120), file=f)
        print(f"ID: {row['id']}", file=f)
        print(f"Title: {row['title']}", file=f)
        print(f"Difficulty: {row['difficulty']}", file=f)
        print("".join(["-"]*120), file=f)
        if src_lang:
            print("Original Code:", file=f)
            print("".join(["-"]*120), file=f)
            print(f"{row[f'{src_lang}_code']}", file=f)
            print("".join(["-"]*120), file=f)
        print("Translated Code:", file=f)
        print("".join(["-"]*120), file=f)
        print(f"{row['python_translated']}", file=f)
        print("".join(["-"]*120), file=f)
        print("Reference Code:", file=f)
        print("".join(["-"]*120), file=f)
        print(f"{row['python_code']}", file=f)
        print("".join(["-"] * 120), file=f)
        print("".join(["#"] * 120) + "\n", file=f)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset")
    argparser.add_argument("--output", help="Filename for translation output")
    argparser.add_argument("--src_lang", help="Optional source language code was translated from")

    args = argparser.parse_args()

    printer = TranslationPrinter()
    printer.print(args.ds_path, args.output, args.src_lang)