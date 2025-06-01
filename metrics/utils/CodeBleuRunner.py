import argparse
import json
import os

import pandas as pd
import sacrebleu
from tree_sitter import Parser
from tree_sitter_languages import get_language


class CodeBleuRunner:
    def run_codebleu(self, ds_path, output, lang="python"):
        df = pd.read_csv(ds_path)

        refs = df["python_code"].apply(lambda x: str(x).strip().replace("\n", " ")).tolist()
        hyps = df["python_translated"].apply(lambda x: str(x).strip().replace("\n", " ")).tolist()

        # Define keywords for weighted BLEU
        keywords = {'def', 'class', 'return', 'if', 'else', 'for', 'while', 'try', 'except', 'with', 'import', 'from', 'as'}

        # ----- BLEU -----
        bleu = sacrebleu.corpus_bleu(hyps, [refs]).score

        # ----- Weighted n-gram match -----
        scores = []
        for hyp, ref in zip(hyps, refs):
            hyp_tokens = hyp.split()
            ref_tokens = ref.split()
            match = sum(5 if tok in keywords else 1 for tok in hyp_tokens if tok in ref_tokens)
            total = sum(5 if tok in keywords else 1 for tok in hyp_tokens)
            scores.append(match / total if total else 0)
        weighted_bleu = sum(scores) / len(scores) * 100

        # ----- AST Match -----
        parser = Parser()
        parser.set_language(get_language(lang))

        def parse_tree(code):
            try:
                return str(parser.parse(bytes(code, "utf8")).root_node)
            except:
                return ""

        ast_matches = [1 if parse_tree(h) == parse_tree(r) else 0 for h, r in zip(hyps, refs)]
        ast_score = sum(ast_matches) / len(ast_matches) * 100

        # ----- Print scores -----
        print(f"BLEU: {round(bleu, 2)}")
        print(f"Weighted n-gram match: {round(weighted_bleu, 2)}")
        print(f"AST match: {round(ast_score, 2)}")

        results = {"bleu": bleu, "weighted": weighted_bleu, "ast": ast_score}

        with open(os.path.join(os.path.dirname(ds_path), f"{output}.json"), "w") as f:
            json.dump(results, f, indent=4)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset")
    argparser.add_argument("--output", help="Filename for CodeBLEU results output")

    args = argparser.parse_args()

    runner = CodeBleuRunner()
    runner.run_codebleu(args.ds_path, args.output)