import argparse
import re
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0
    extensions = set([fn.rsplit('.', 1)[-1] for fn in args.filenames])
    if 'sql' in extensions and len(extensions) > 1:
        print("发现commit文件混合着SQL和其他类型文件, 请单独提交SQL文件")
        return 1

    return retv


if __name__ == '__main__':
    exit(main())
