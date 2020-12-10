from pathlib import Path
from typing import Union
import sys
# prefix components:
space = '    '
branch = '│   '
# pointers:
tee = '├── '
last = '└── '
headline_high_start = '┌'
headline_low_start = '└'
headline_body = '─'
headline_high_end = '┐'
headline_low_end = '┘'
headline_sides = '│'


def tree(dir_path: Path, prefix: str = '    '):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """

    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


def create_tree(dir_path: Path, prefix: str = '    ', category=None):
    name = 'Name: ' + dir_path.name
    if category is not None:
        category = 'Category: ' + category.upper()
        length_name = max([len(name), len(category)])
        length_dif = length_name - min([len(name), len(category)])
    else:
        length_name = len(name)
    yield headline_high_start + headline_body * length_name + headline_high_end
    if category is not None and len(name) < len(category):
        yield headline_sides + name + ' ' * length_dif + headline_sides
    else:
        yield headline_sides + name + headline_sides
    if category is not None:
        if len(category) < len(name):
            yield headline_sides + category + ' ' * length_dif + headline_sides
        else:
            yield headline_sides + category + headline_sides
    yield headline_low_start + headline_body * length_name + headline_low_end
    yield from tree(dir_path, prefix)


def print_tree(dir_path: Union[Path, str], category=None):
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)
    for line in create_tree(dir_path, '    ', category):
        print(line)


if __name__ == '__main__':
    print_tree(sys.argv[1])
