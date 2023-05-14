import os


def write_to_file(path, x, y):
    folder_path = os.path.dirname(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(path, 'a') as f:
        f.write(f'x: {x}, y: {y}')
        f.write("\n")

