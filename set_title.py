import argparse
import glob
import os
import re


TITLE_REGEX = re.compile(r'(?P<open_tag><[^>\w]*title[^>]*>)(?P<old_title>[^<]*)(?P<close_tag><[^>]*/[^>]*title[^>]*>)')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path to file to replace (glob-patterns supported)')
    args = parser.parse_args()

    return args


def replace_title(path_glob):
    count = 0
    for path in glob.iglob(path_glob):
        print(f'{path} -> ', end='')
        name = os.path.splitext(os.path.basename(path))[0]
        print(f'"{name}"')

        with open(path, 'r') as fp:
            old_text = fp.read()

        new_text = TITLE_REGEX.sub(f'\\1{name}\\3', old_text)

        with open(path, 'w') as fp:
            fp.write(new_text)
        count += 1
    print(f'{count} files modified')


def main():
    args = get_args()
    for path in glob.iglob(args.path):
        replace_title(path)


if __name__ == '__main__':
    main()
