import re
from typing import List, Optional

separators = ['.', ',', '!', '?', '"', '\n', '\t', '(', ')', '|', ';', '>', '<', '[', ']', '\'', ':',
              '@', '*', '/', '=', '+']
numeric_regex = r'[-+]?(\d)*.?(\d)*'
reg = re.compile(numeric_regex)


def tokenize(_input: Optional[str], accept_nums: bool = False) -> List[str]:
    if _input is None:
        return []

    _input = str(_input)

    for separator in separators:
        _input = _input.replace(separator, ' ')

    return [word for word in _input.split(' ') if len(word)> 0 and (accept_nums or not reg.fullmatch(word))]
