import argparse

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class CodeT5Runner:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base-codexglue-translate-java-cs")

    def run(self):
        java_code = "public class Main { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }"

        input_ids = self.tokenizer.encode(java_code, return_tensors="pt")
        output_ids = self.model.generate(input_ids)
        cs_code = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(cs_code)


if __name__ == "__main__":
    # argparser = argparse.ArgumentParser()
    #
    # argparser.add_argument("--data")
    #
    # args = argparser.parse_args()

    runner = CodeT5Runner()
    runner.run()