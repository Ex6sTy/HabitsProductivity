import os


def print_tree(start_path=".", depth=3, prefix=""):
    if depth == 0:
        return
    for item in sorted(os.listdir(start_path)):
        path = os.path.join(start_path, item)
        print(prefix + "|-- " + item)
        if os.path.isdir(path):
            print_tree(path, depth - 1, prefix + "|   ")


print_tree(".", depth=3)
