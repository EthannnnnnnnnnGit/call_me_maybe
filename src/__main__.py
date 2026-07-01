from src.parsing.parse_data import get_json
from src.parsing.validate_data import data_validator
import src.generate as generator
from src.parsing.parse_flags import get_flags
from src.make_json import make_output_file
from src.summary import summary_print
from pydantic import ValidationError


def main() -> None:
    flags = get_flags()
    try:
        prompts = get_json(flags.input)
        functions = get_json(flags.functions_definition)
        data_validator(prompts, functions)
    except ValidationError as e:
        for error in e.errors():
            print(f"Parsing error: {error['msg']} at {error['loc']}")
        return
    except Exception as e:
        print(e)
        return
    default_func = {"name": "fn_null",
                    "description": "",
                    "parameters": {"null": {"type": "null"}},
                    "returns": {"type": "null"}}
    functions.append(default_func)
    ia = generator.CallMeMaybe(prompts, functions)
    lst_json = ia.thinker()
    make_output_file(lst_json, flags.output)
    summary_print(lst_json)


if __name__ == "__main__":
    main()
