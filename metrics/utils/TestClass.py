import time
import threading
import typing
from typing import List, Optional


class TestClass:
    def __init__(self, truth_code: str, gen_code: str, func_name: str, test_cases: typing.List):
        self.truth_code = truth_code
        self.gen_code = gen_code

        self.func_name = func_name
        self.test_cases = test_cases

    def evaluate(self):
        correct = 0
        errors = 0

        for tc in self.test_cases:
            args = tc["input"]

            exec(self.truth_code, globals())
            result_truth = eval(f"{self.func_name}(**args)")

            try:
                exec(self.gen_code, globals())
                result_gen = self.eval_with_timeout(f"{self.func_name}(**args)", args, 1)

                if result_truth == result_gen:
                    correct += 1
            except:
                errors += 1

        print(f"{self.func_name}: {correct}/{len(self.test_cases)}")
        return correct, errors, len(self.test_cases)

    @staticmethod
    def eval_with_timeout(code, args, timeout):
        def execute_with_timeout(code, args, timeout):
            result = {"value": None}

            def target(args):
                try:
                    result["value"] = eval(code)
                except Exception as e:
                    result["value"] = e

            thread = threading.Thread(target=target, args=(args,))
            thread.daemon = True
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
                return TimeoutError("Code execution timed out")
            return result["value"]

        result = execute_with_timeout(code, args, timeout)
        return result