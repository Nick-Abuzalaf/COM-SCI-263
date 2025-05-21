import argparse
import json
import os

import pandas as pd

from tests.utils.TestClass import TestClass


class TestRunner:
    def evaluate(self, dataset, test_dir):
        df = pd.read_csv(dataset)

        test_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith(".json")]

        for file in test_files:
            with open(file, "r") as f:
                data = json.load(f)

                row = df[df["id"] == data["id"]]
                truth_code = row["python_code"].item()
                gen_code = row["python_code"].item()

                test_class = TestClass(truth_code, gen_code, data["func_name"], data["test_cases"])
                test_class.evaluate()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--dataset", help="Path to dataset", default=os.path.join(os.getcwd(), "..", "..", "dataset", "lc_dataset_clean.csv"))
    argparser.add_argument("--test_dir", help="Directory where test files are located.", default=os.path.join(os.getcwd(), ".."))

    args = argparser.parse_args()

    tr = TestRunner()
    tr.evaluate(args.dataset, args.test_dir)