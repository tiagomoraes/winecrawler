import re
from typing import List, Optional
import unidecode

separators = ['.', ',', '!', '?', '"', '\n', '\t', '(', ')', '|', ';', '>', '<', '[', ']', '\'', ':',
              '@', '*', '/', '=', '+']
numeric_regex = r'[-+]?(\d)*.?(\d)*'
reg = re.compile(numeric_regex)


def normalize_string(s: str) -> str:
    return unidecode.unidecode(s.lower().strip())


def tokenize(_input: Optional[str], accept_nums: bool = False) -> List[str]:
    if _input is None:
        return []

    _input = str(_input)

    for separator in separators:
        _input = _input.replace(separator, ' ')

    return [normalize_string(word) for word in _input.split(' ') if len(word)> 0 and (accept_nums or not reg.fullmatch(word))]
