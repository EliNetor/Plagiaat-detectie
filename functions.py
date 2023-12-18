from pathlib import Path

def GetComments(file_paths):
    contents = []
    for path in file_paths:
        with open(path, 'r') as f:
            lines = f.readlines()
            contents.append([line.strip() for line in lines if line.startswith('#')])
    return contents