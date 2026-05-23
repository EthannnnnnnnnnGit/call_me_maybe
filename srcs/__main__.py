import srcs.parsing.get_data as parsing
import srcs.generate as generator
from srcs.parsing.parsing import get_args
# from typing import Any


def main() -> None:
    args = get_args()
    try:
        prompts = parsing.get_json_data(args.input)
        functions = parsing.get_json_data(args.functions_definition)
        parsing.functions_validator(functions)
        parsing.tests_validator(prompts)
    except Exception as e:
        print(e)
        return
    ia = generator.CallMeMaybe(prompts, functions)
    ia.thinker()

if __name__ == "__main__":
    main()
