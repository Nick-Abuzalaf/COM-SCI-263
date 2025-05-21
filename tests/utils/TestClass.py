import typing


class TestClass:
    def __init__(self, truth_code: str, gen_code: str, func_name: str, test_cases: typing.List):
        self.truth_code = truth_code
        self.gen_code = gen_code

        self.func_name = func_name
        self.test_cases = test_cases

    def evaluate(self):
        passed = 0

        for tc in self.test_cases:
            args = tc["input"]

            exec(self.truth_code, globals())
            result_truth = eval(f"{self.func_name}(**args)")

            exec(self.gen_code, globals())
            result_gen = eval(f"{self.func_name}(**args)")

            if result_truth == result_gen:
                passed += 1

        print(f"{self.func_name}: {passed}/{len(self.test_cases)}")
