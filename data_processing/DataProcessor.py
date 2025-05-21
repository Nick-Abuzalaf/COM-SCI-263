import argparse
import os

from datasets import load_dataset


class DataProcessor:
    def __init__(self):
        self.dataset_path = "greengerong/leetcode"

    def process(self, output: str):
        ds = load_dataset(self.dataset_path)
        df = ds["train"].to_pandas()

        df["cpp"] = df["c++"]
        df = df.drop(["c++"], axis=1)

        code_cols = ["java", "cpp", "python", "javascript"]
        for col in code_cols:
            new_code_col = f"{col}_code"
            new_desc_col = f"{col}_description"

            df[new_code_col] = df[col].apply(lambda x: self.get_code(x, col))
            df[new_desc_col] = df[col].apply(lambda x: self.get_description(x))

            df = df.drop([col], axis=1)

        if not os.path.exists(output):
            os.mkdir(output)

        df.to_csv(os.path.join(output, "lc_dataset_clean.csv"), index=False)

        return

    @staticmethod
    def get_code(val: str, col: str):
        new_val = val.split(f"```{col}")[-1]
        new_val = new_val.split(f"```")[0]
        new_val = new_val.strip()

        return new_val

    @staticmethod
    def get_description(val: str):
        new_val = val.split("```")[-1]
        new_val = new_val.strip()

        return new_val


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--output", help="Path to output dataset", default=os.path.join(os.getcwd(), "../output"))
    args = argparser.parse_args()

    dp = DataProcessor()
    dp.process(args.output)