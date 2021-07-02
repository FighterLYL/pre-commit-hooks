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
    re_groups = [m for m in re.finditer(r'"""', contents)]
    if len(re_groups) % 2 != 0:
        print(f'"""分割符不匹配')

    db_delimiters = []
    replaceable_dates = []
    for i in range(0, len(re_groups), 2):
        start_index = re_groups[i].start()
        end_index = re_groups[i+1].end()
        sql_string = contents[start_index:end_index]
        # 数据库分割符
        results = DELIMITER_PATTERN.findall(sql_string)
        # 日期未替换
        dates = re.findall(r"202\d{5,7}", sql_string)
        db_delimiters.extend(results)
        replaceable_dates.extend(dates)

    if len(db_delimiters) > 0:
        for line in db_delimiters:
            print(f"Find INVALID delimiter: {line}")
        return 1
    if replaceable_dates:
        print(f"Find Replaceable dates: {replaceable_dates}")
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
