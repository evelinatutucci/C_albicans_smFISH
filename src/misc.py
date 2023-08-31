import re
from glob import glob
from typing import Tuple

import numpy as np
from skimage import io
import os, shutil
from urllib.request import urlretrieve
import progressbar

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def download_sample_data(target_dir, url):

    urlretrieve(url, f"{target_dir}/temp.zip", MyProgressBar())
    shutil.unpack_archive(f"{target_dir}/temp.zip", extract_dir=target_dir)
    os.remove(f"{target_dir}/temp.zip")

def ensure_files_exist(root_dir):
    """
    checks if the files required to run the processing notebooks are present.
    Optionally downloads a minimal dataset from zenodo
    """

    experiments = group_experiments(root_dir)

    for identifier, replicates in experiments.items():

        for replicate, paths in replicates.items():
            print(f"testing {identifier} {replicate}")
            for pattern in ['CY\d', 'cell_mask', 'nuclear_mask', 'DAPI', 'DIC']:
                pattern_found = False
                for file in paths.keys():
                    if re.findall(pattern, file):
                        pattern_found = True
                if not pattern_found:
                    print(f'could not find {pattern} in {identifier} {replicate}')
                    break
            else:
                print('ok')
            print(50 * '-')




def find_high_density_patch(mask: np.ndarray, patch_size: Tuple = (200, 200), attempts: int = 20):
    """

    randomly samples patches on the mask image and returns the coordinates of the top-left corner
    of the densest patch

    :param mask: segmentation image expected to have dimension (h * w)
    :param patch_size: height and width of the patch
    :param attempts: how many patches to try

    :return: coordinates of top left corner of densest patch found
    :rtype: Tuple[int, int]

    """
    h, w = mask.shape
    h_patch, w_patch = patch_size

    cell_pixels = 0
    selected_patch = (None, None)  # top left corner
    for attempt in range(attempts):

        row_sample = np.random.randint(0, h - h_patch)
        col_sample = np.random.randint(0, w - w_patch)

        sample_patch = mask[row_sample:row_sample + h_patch, col_sample:col_sample + w_patch]
        if np.sum(sample_patch > 0) > cell_pixels:
            cell_pixels = np.sum(sample_patch > 0)
            selected_patch = (row_sample, col_sample)

    return selected_patch


def find_in_focus_indices(focus: np.ndarray, adjustment_bottom: int = 5, adjustment_top: int = 10):
    """

    find the in-focus indices of calculated focus scores

    :param focus: series of values representing max intensity along z-axis
    :param adjustment_bottom: controls by how much the resulting range should be padded (bottom)
    :param adjustment_top: controls by how much the resulting range should be padded (top)

    :return: low and high z-level between which the spots are in focus
    :rtype: Tuple[int,int]
    """

    # find the inflection points of the smoothed curve
    ifx_1 = min([np.diff(focus).argmax(), np.diff(focus).argmin()])
    ifx_2 = max([np.diff(focus).argmax(), np.diff(focus).argmin()])

    # add a little cushion to one side.
    ifx_1 -= adjustment_bottom
    ifx_2 += adjustment_top

    return ifx_1, ifx_2


def group_experiments(root_dir):
    mask_folder = f"{root_dir}/Masks"
    spot_folder = f"{root_dir}/Spots"
    dense_folder = f"{root_dir}/Spots decomposition"
    experiments = {}

    for file in glob(f'{root_dir}/*'):
        match = re.findall(f'{root_dir}(?:\\\|/)(.*)_(CY\d+|DAPI|DIC)_(\d.+)\.tif', file)

        if match:
            identifier, channel, exp_number = match[0]
            exp_number = int(exp_number)

            if not identifier in experiments:
                experiments[identifier] = {}
            if not exp_number in experiments[identifier]:
                experiments[identifier][exp_number] = {}
            experiments[identifier][exp_number][channel] = file

            nuclear_mask_candidate = glob(f"{mask_folder}/*{identifier}_DAPI_{exp_number:02d}_seg.tif")
            if nuclear_mask_candidate:
                experiments[identifier][exp_number]['nuclear_mask'] = nuclear_mask_candidate[0]

            mask_candidate = glob(f"{mask_folder}/*{identifier}_DIC_{exp_number:02d}_seg.tif")
            if mask_candidate:
                experiments[identifier][exp_number]['cell_mask'] = mask_candidate[0]

            # this will break if there are spots from more than one channel
            spot_candidate = glob(f"{spot_folder}/*{identifier}*{exp_number:02d}*spots*")
            if spot_candidate:
                experiments[identifier][exp_number]['spots'] = spot_candidate[0]

            dense_candidate = glob(f"{dense_folder}/*{identifier}*{exp_number:02d}*spots*dd*")
            if dense_candidate:
                experiments[identifier][exp_number]['dense'] = dense_candidate[0]

            if 'CY' in channel:
                experiments[identifier][exp_number]['output_name'] = f'{identifier}_{channel}_{exp_number:02d}'

    return experiments


def load_data(paths):
    output = {}
    for name, path in paths.items():
        if path.endswith('.npy'):
            output[name] = np.load(path)
        if path.endswith('.tif'):
            output[name] = io.imread(path)

    return output


