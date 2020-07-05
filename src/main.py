import argparse
import os
from pydicom import dcmread
from src.dicom.files import load_scan_from_dir, load_scan_from_files
from src.dicom.processing import process, savefig
from src.conf import settings


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def list_files(file):
    if not file.endswith('.dcm'):
        raise Exception("All files must be a dicom file")
    return file


def get_dicom():
    parser = argparse.ArgumentParser(
        description='Intracranial Hemorrhage Detection Algorithm')
    parser.add_argument('-f', '--files', type=list_files,
                        nargs='+', help='--files file1.dcm file2.dcm')
    parser.add_argument('-p', '--path', type=dir_path,
                        help='--path directory/')

    args = parser.parse_args()

    files = []

    if args.files:
        files = load_scan_from_files(args.files)
    elif args.path:
        files = load_scan_from_dir(args.path)
    else:
        parser.error('No action, insert --file or --path')

    fig_paths = []
    for _filename in files:
        for processed_files in process(_filename):
            fig_paths.append(savefig(
                image=processed_files['image'],
                processname=processed_files['name'],
                contour=processed_files['contour'],
                filename=_filename,
            ))

    return fig_paths


if __name__ == "__main__":
    print(get_dicom())
