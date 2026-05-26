from typing import Any


def define_name_prompt(prompts: list[dict[str, str]],
                       functions: list[dict[str, Any]]) -> list[str]:
    lst_prompts: list[str] = []
    prompts_function: str = ""
    for func in functions:
        prompts_function += "\n{\"name\":" + func["name"] + "}"
        # prompts_function += ",\"description\":" + func["description"] + "}"
    system = f"""<|im_start|>system{prompts_function}\n<|im_end|>\n"""
    for prompt in prompts:
        temp = (system + "<im_start>user\n" +
                prompt["prompt"] + "\n<im_end>" + "\n<im_start>assistant"
                "\n{\"name\":")
        lst_prompts.append(temp)
    return lst_prompts


# define_name_prompt([{"prompt": "YO"}, {"prompt": "YO"}],
#                    [{"name": "jsp", "description": "jsp"},
#                     {"name": "jsp", "description": "jsp"}])
