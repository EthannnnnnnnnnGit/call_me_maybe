import srcs.get_data as parsing
import srcs.generate as generator
# from typing import Any


def main() -> None:
    try:
        prompts = parsing.get_json_data("data/input/"
                                        "function_calling_tests.json")
        functions = parsing.get_json_data("data/input/"
                                          "functions_definition.json")
        parsing.functions_validator(functions)
        parsing.tests_validator(prompts)
    except Exception as e:
        print(e)
        return
    generator.thinker(prompts, functions)


if __name__ == "__main__":
    main()
