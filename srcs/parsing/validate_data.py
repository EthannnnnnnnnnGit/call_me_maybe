
from pydantic import BaseModel, Field, model_validator
from typing import Self


class FunctionValidator(BaseModel):
    name: str = Field(min_length=1)
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    @model_validator(mode="after")
    def naming_check(self) -> Self:
        authorized = {"string", "integer", "hex",
                      "number", "boolean", "null", "array"}
        if self.returns.__len__() != 1:
            raise ValueError("Returns dict should have precisely one value.")
        if list(self.returns.keys())[0] != "type":
            raise ValueError("The key of the returns dict should be \"type\"")
        for key, value in self.parameters.items():
            if len(key) < 1:
                raise ValueError("A key of dict should be at least "
                                 "a letter long")
            if value.__len__() != 1:
                raise ValueError("Parameters dict should have "
                                 "precisely one value.")
            if list(value.keys())[0] != "type":
                raise ValueError("The key of the parameters dict "
                                 "should be \"type\"")
            if list(value.values())[0] not in authorized:
                raise ValueError("Type not supported,"
                                 f"types should be one in {authorized}")
        return self


class Prompt(BaseModel):
    prompt: str = Field(min_length=1)


def data_validator(lst_prompts, lst_funcs) -> None:
    for prompt in lst_prompts:
        Prompt(**prompt)
    for func in lst_funcs:
        FunctionValidator(**func)
