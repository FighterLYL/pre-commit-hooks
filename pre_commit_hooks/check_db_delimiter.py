import argparse
import re
from typing import Optional
from typing import Sequence

DELIMITER_PATTERN = re.compile(r'\bfrom \w+\.\w+\b')


def is_tdw_script(contents: str):
    if "def TDW_PL" in contents:
        return True
    return False


def check_delimiter(contents: str):
    start_index = contents.find("main_sql")
    end_index = contents.find(".format(target_tb=target_tb, iDate=iDate)")
    main_sql_string = contents[start_index:end_index]
    results = DELIMITER_PATTERN.findall(main_sql_string)
    if len(results) > 0:
        for line in results:
            print(f"Find INVALID delimiter: {line}")
        return 1
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'r') as f:
            contents = f.read()
            if is_tdw_script(contents):
                return_value = check_delimiter(contents)
                retv |= return_value

    return retv


if __name__ == '__main__':
    exit(main())
