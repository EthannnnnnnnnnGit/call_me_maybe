*This project has been created as part of the 42 curriculum by eel-kerc.*


## Description


## Instructions


## Resources
Qwen: https://qwen.readthedocs.io/en/latest/getting_started/concepts.html  
Json format: https://www.json.org/json-fr.html   

### Functions names's prompt

```python
"""
<|im_start|>system
{"name":"fn_add_numbers","description":"Add two numbers together and return their sum."}
{"name":"fn_greet","description":"Generate a greeting message for a person by name."}
{"name":"fn_reverse_string","description":"Reverse a string and return the reversed result."}
{"name":"fn_get_square_root","description":"Calculate the square root of a number."}
{"name":"fn_substitute_string_with_regex","description":"Replace all occurrences matching a regex pattern in a string."}
{"name":"fn_null","description":""}
IMPORTANT : Choose fn_null if no description correspond
<|im_end|>
<im_start>user
Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'
<im_end>
<im_start>assistant
{"name":
"""
```
### Parameters's prompt

```python
"""
<im_start>system
{'name': 'fn_add_numbers', 'description': 'Add two numbers together and return their sum.', 'parameters': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'returns': {'type': 'number'}}
<im_end>
<im_start>user
What is the sum of 2 and 3?
 <im_end>
<im_start>assistant
{"parameters": {"a": 
"""
```