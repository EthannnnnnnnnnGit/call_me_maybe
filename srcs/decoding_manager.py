from srcs.type_constrained import (
    StringDecoding,
    IntegerDecoding,
    HexDecoding,
    NumberDecoding,
    SpecialDecoding,
    ObjectDecoding,
    ArrayDecoding
)


class DecodingManager:
    def __init__(self):
        self.pipelines = {
            "string": StringDecoding(),
            "integer": IntegerDecoding(),
            "hexadecimal": HexDecoding(),
            "number": NumberDecoding(),
            "bool": SpecialDecoding(),
            "null": SpecialDecoding(),
            "object": ObjectDecoding(),
            "array": ArrayDecoding()
        }
        self.decoder = None

    def choose_decoder(self, type: list[str] | str) -> None:
        if isinstance(type, list):
            try:
                self.decoder = self.pipelines[type[0]]
                if type[0] == "array":
                    self.decoder.reset_settings(type[1])
                elif type[0] == "object":
                    self.decoder.reset_settings(type[1], type[2])
                else:
                    raise KeyError("Types not valid")
            except KeyError as e:
                print("Unknown type", e)
                return
        else:
            try:
                self.decoder[self.pipelines[type]]
            except KeyError as e:
                print("Unknow type:", e)
        if type == "bool" or type == "null":
            self.decoder.reset_settings(type)
        else:
            self.decoder.reset_settings()
