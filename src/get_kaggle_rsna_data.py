'''
What should I expect the data format to be?
The training data is provided as a set of
image Ids and multiple labels, one for each
of five sub-types of hemorrhage, plus an
additional label for any, which should always
be true if any of the sub-type labels is true.

There is also a target column, Label, indicating
the probability of whether that type of hemorrhage
exists in the indicated image.

There will be 6 rows per image Id. The label indicated
by a particular row will look like [Image Id]_[Sub-type Name],
as follows:

Id,Label
1_epidural_hemorrhage,0
1_intraparenchymal_hemorrhage,0
1_intraventricular_hemorrhage,0
1_subarachnoid_hemorrhage,0.6
1_subdural_hemorrhage,0
1_any,0.9
'''

import csv
import os

INPUT_PATH = '/media/herlanassis/Arquivos/rsna-intracranial-hemorrhage-detection'
TRAIN_DATA_PATH = '{}/stage_2_train'.format(INPUT_PATH)
TARGET_FILE_PATH = '{}/stage_2_train.csv'.format(INPUT_PATH)
OUTPUT_PATH = '../examples'


def get_sample_info_by(id):
    info = []
    with open('../kaggle/stage_2_train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:

            if line_count > 0:
                id_image, label = row

                image_id, subtype_hemorrhage = split_rsna_info_from(id_image)

                if id in "ID_{}".format(image_id):
                    info.append(row)

            line_count += 1

    return info


def split_rsna_info_from(id_image):
    _, image_id, subtype_hemorrhage = id_image.split('_')

    return image_id, subtype_hemorrhage


def save_samples(sample_path):
    cmd = 'cp {} {}'.format(sample_path, OUTPUT_PATH)
    os.system(cmd)


def _get_samples(csv_reader, number_of_samples, subtype, minimun_change, maximum_change):
    line_count = number_of_samples_count = 0

    for row in csv_reader:
        id_image, label = row

        if line_count > 0:
            image_id, subtype_hemorrhage = split_rsna_info_from(id_image)

            is_sample_target = float(label) >= minimun_change and float(
                label) <= maximum_change
            if subtype_hemorrhage == subtype and is_sample_target:
                save_samples(
                    '{}/ID_{}.dcm'.format(TRAIN_DATA_PATH, image_id))
                number_of_samples_count += 1

        line_count += 1

        if number_of_samples_count == number_of_samples:
            return


def get_samples():
    with open(TARGET_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # save 10 samples with any type of hemorrhage
        _get_samples(csv_reader, 10, 'any', 1.0, 1.0)

        # save 10 samples without any type of hemorrhage
        _get_samples(csv_reader, 10, 'any', 0, 0)

    return 'ok'


if __name__ == "__main__":
    print(get_samples())
