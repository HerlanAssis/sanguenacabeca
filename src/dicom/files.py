import os


def load_scan_from_files(fileList):
    files = []
    for filename in fileList:
        if filename.endswith('.dcm'):
            files.append(filename)
    return files


def load_scan_from_dir(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        for filename in fileList:
            files.append(os.path.join(dirName, filename))
    return load_scan_from_files(files)
