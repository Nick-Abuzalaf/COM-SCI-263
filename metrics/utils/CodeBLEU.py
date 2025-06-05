import argparse
import os

import pandas as pd
import sacrebleu
from tree_sitter import Parser
from tree_sitter_languages import get_language
import zss
from tqdm import tqdm

# Define keywords for weighted n-gram match
KEYWORDS = {'def', 'class', 'return', 'if', 'else', 'for', 'while', 'try', 'except', 'with', 'import', 'from', 'as'}

def tokenize_code(code):
    if not isinstance(code, str):
        return []
    return code.strip().replace("\n", " ").split()

def weighted_ngram_score(hyp, ref):
    hyp_tokens = tokenize_code(hyp)
    ref_tokens = set(tokenize_code(ref))
    match = sum(5 if tok in KEYWORDS else 1 for tok in hyp_tokens if tok in ref_tokens)
    total = sum(5 if tok in KEYWORDS else 1 for tok in hyp_tokens)
    return match / total if total else 0

class ASTNode:
    def __init__(self, node):
        self.label = node.type
        self.children = [ASTNode(child) for child in node.children]

    def get_children(self):
        return self.children

    def get_label(self):
        return self.label

def tree_edit_sim_score(hyp_code, ref_code, parser, tree_cache):
    try:
        if hyp_code not in tree_cache:
            tree_cache[hyp_code] = parser.parse(bytes(hyp_code, "utf8")).root_node
        if ref_code not in tree_cache:
            tree_cache[ref_code] = parser.parse(bytes(ref_code, "utf8")).root_node

        hyp_tree = tree_cache[hyp_code]
        ref_tree = tree_cache[ref_code]

        hyp_ast = ASTNode(hyp_tree)
        ref_ast = ASTNode(ref_tree)

        dist = zss.simple_distance(
            hyp_ast, ref_ast,
            get_children=lambda node: node.get_children(),
            get_label=lambda node: node.get_label()
        )

        max_size = max(hyp_tree.end_byte, ref_tree.end_byte)
        return 1 - dist / max_size if max_size else 0
    except Exception:
        return 0

def run_codebleu(refs, hyps, lang="python"):
    refs = [str(r) if r is not None else "" for r in refs]
    hyps = [str(h) if h is not None else "" for h in hyps]

    # BLEU
    if all(r == "" for r in refs) or all(h == "" for h in hyps):
        bleu = 0.0
    else:
        bleu = sacrebleu.corpus_bleu(hyps, [refs]).score

    # Weighted n-gram match
    weighted_scores = [weighted_ngram_score(h, r) for h, r in zip(hyps, refs)]
    weighted_bleu = sum(weighted_scores) / len(weighted_scores) * 100

    # AST match
    parser = Parser()
    parser.set_language(get_language(lang))
    tree_cache = {}

    ast_scores = []
    for h, r in tqdm(zip(hyps, refs), total=len(hyps), desc="Computing AST scores"):
        ast_scores.append(tree_edit_sim_score(h, r, parser, tree_cache))
    ast_score = sum(ast_scores) / len(ast_scores) * 100

    # Print results
    print(f"BLEU: {round(bleu, 2)}")
    print(f"Weighted n-gram match: {round(weighted_bleu, 2)}")
    print(f"AST match (tree edit similarity): {round(ast_score, 2)}")

    return {
        "bleu": bleu,
        "weighted": weighted_bleu,
        "ast": ast_score
    }

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--ds_path", help="Path to dataset with 'python_translated' column. Intended for use on "
                                             "the output file from TransCoderRunner.py")

    args=argparser.parse_args()

    df = pd.read_csv(args.ds_path)
    files = [f for f in os.listdir("../unittests/") if os.path.isfile(os.path.join(os.getcwd(), "../unittests/", f))]
    ids = sorted([int(f.split("id")[-1].split(".json")[0]) for f in files])
    df = df[df["id"].isin(ids)]

    refs = df["python_code"].apply(lambda x: str(x).strip().replace("\n", " ")).tolist()
    hyps = df["python_translated"].apply(lambda x: str(x).strip().replace("\n", " ")).tolist()

    result = run_codebleu(refs, hyps)
    print(result)