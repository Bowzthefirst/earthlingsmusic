import re
import os
from pytube import cipher

def patch_pytube():
    cipher_file = cipher.__file__
    with open(cipher_file, 'r') as file:
        content = file.read()

    patched_content = re.sub(
        r'def get_throttling_function_name\(js: str\) -> str:[\s\S]+?raise RegexMatchError\(',
        r"""
def get_throttling_function_name(js: str) -> str:
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]
    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )
        """,
        content
    )

    with open(cipher_file, 'w') as file:
        file.write(patched_content)

if __name__ == '__main__':
    patch_pytube()
