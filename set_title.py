import argparse
import glob
import os
import re


TITLE_REGEX = re.compile(r'(?P<open_tag><[^>\w]*title[^>]*>)(?P<old_title>[^<]*)(?P<close_tag><[^>]*/[^>]*title[^>]*>)')
QUIET = False


def log(*args, **kwargs):
    if not QUIET:
        print(*args, **kwargs)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path to file to replace (glob-patterns supported)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Silence output')
    args = parser.parse_args()

    return args


def replace_title(path_glob):
    count = 0
    for path in glob.iglob(path_glob):
        log(f'{path} -> ', end='')
        name = os.path.splitext(os.path.basename(path))[0]
        log(f'"{name}"')

        with open(path, 'r') as fp:
            old_text = fp.read()

        new_text = TITLE_REGEX.sub(f'\\1{name}\\3', old_text)

        with open(path, 'w') as fp:
            fp.write(new_text)
        count += 1
    log(f'{count} files modified')


def main():
    global QUIET

    args = get_args()

    QUIET = args.quiet

    for path in glob.iglob(args.path):
        replace_title(path)


if __name__ == '__main__':
    main()
