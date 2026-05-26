from llm_sdk.llm_sdk import Small_LLM_Model
import json

llm = Small_LLM_Model()
print(llm.get_path_to_tokenizer_file())
for i in range(1, 10):
    print(llm.encode(f"-{i}"))
