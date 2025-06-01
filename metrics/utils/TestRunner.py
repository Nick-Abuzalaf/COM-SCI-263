import argparse
import json
import os

import pandas as pd

from metrics.utils.TestClass import TestClass


class TestRunner:
    def evaluate(self, ds_path, output, test_dir):
        df = pd.read_csv(ds_path)

        test_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith(".json")]

        results = {
                    "easy": {
                        "correct": 0,
                        "errors": 0,
                        "total": 0
                    },
                    "medium": {
                        "correct": 0,
                        "errors": 0,
                        "total": 0
                    },
                    "hard": {
                        "correct": 0,
                        "errors": 0,
                        "total": 0,
                    },
                    "correct": 0,
                    "errors": 0,
                    "total": 0
                  }

        for file in test_files:
            with open(file, "r") as f:
                data = json.load(f)

                row = df[df["id"] == data["id"]]

                truth_code = row["python_code"].item()
                gen_code = row["python_translated"].item()

                difficulty = str(row["difficulty"].item()).lower()

                test_class = TestClass(truth_code, gen_code, data["func_name"], data["test_cases"])
                correct, errors, total = test_class.evaluate()

                results["correct"] += correct
                results["errors"] += errors
                results["total"] += total

                if difficulty != "nan":
                    results[difficulty]["correct"] += correct
                    results[difficulty]["errors"] += errors
                    results[difficulty]["total"] += total

        print(results)
        print(f"Accuracy (Overall): {round(results['correct']/results['total'], 4)}")
        print(f"Accuracy (Easy): {round(results['easy']['correct'] / results['easy']['total'], 4)}")
        print(f"Accuracy (Medium): {round(results['medium']['correct'] / results['medium']['total'], 4)}")
        print(f"Accuracy (Hard): {round(results['hard']['correct'] / results['hard']['total'], 4)}")

        with open(os.path.join(os.path.dirname(ds_path), f"{output}.json"), "w") as f:
            json.dump(results, f, indent=4)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset")
    argparser.add_argument("--output", help="Filename for output evaluation results")
    argparser.add_argument("--test_dir", help="Directory where test files are located.", default=os.path.join(os.getcwd(), "../unittests"))

    args = argparser.parse_args()

    tr = TestRunner()
    tr.evaluate(args.ds_path, args.output, args.test_dir)