from srcs.parsing.parse_data import get_json
from srcs.parsing.validate_data import data_validator
import srcs.generate as generator
from srcs.parsing.parse_flags import get_flags
from srcs.make_json import make_output_file
from srcs.summary import summary_print


def main() -> None:
    flags = get_flags()
    try:
        prompts = get_json(flags.input)
        functions = get_json(flags.functions_definition)
        data_validator(prompts, functions)
    except Exception as e:
        print(e)
        return
    ia = generator.CallMeMaybe(prompts, functions)
    lst_json = ia.thinker()
    make_output_file(lst_json, flags.output)
    summary_print(lst_json)


if __name__ == "__main__":
    main()
