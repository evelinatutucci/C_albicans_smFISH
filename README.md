# C.albicans smFISH pipeline

This GitHub repository consists of .ipynb files used for the data analysis of the VU systems biology O2 building ET laboratory C.albicans project. These notebooks were used in the analysis of the article titled: "single-molecule Fluorescent In Situ Hybridization (smFISH) for RNA detection in the fungal pathogen Candida albicans".
It consists of the following notebooks:

Notebooks
  1. 01-npy_to_tif_conversion
  2. 02-spot_detection
  3. 03-spot_decomposition
  4. 04-spot_assignment
  5. 05-plotting

For a description of the code look at the corresponding number underneath:

 1. Cellpose outputs its segmentation masks as .npy files. These can be converted to the easier-to-work-with tiff format using this notebook. 
 
 
 2. In order to quantify the number of RNAs in your images a Laplacian of Gaussian kernel is applied to detect high-intensity spots from the background.
 

 3. Dense or high-intensity spots can be composed of several RNAs. Here, the median spot intensity is used to decompose these dense regions into an estimate of the number of RNAs.
 
 
 4. The assignment of detected RNAs to a cell-mask id. Cellpose outputs a Mask file in which every cell is given a unique cell mask value. Here, the detected RNA coordinates are used to count the number of RNAs per unique cell mask ID.

 5. Plotting of generated data.

Example of FISH image (scalebar 5 µm):
![example of FISH on the CLB2 mRNA for the SC5314 WT strain grown in SPIDER36 medium](CET111_CLB2Q670_SPIDER37_CY5_01_MAXcrop_filt_5um.png)
Spots (yellow) indicate fluorescently labelled CLB2 mRNA in the SC5314 WT strain grown in SPIDER medium at 37 °C. The blue signal indicates DAPI (DNA stain). Both fluorescent channels are overlayed on a DIC image. 

# Requirements and installation
In order to install the necessary packages and start jupyter notebook type in your terminal:

1. cd /this/cloned or downloaded/github/repo
2. conda env create --name FISH --file FISH.yml
3. conda activate FISH
4. cd notebooks 
5. jupyter notebook
 
# Example dataset
An example dataset is available at https://zenodo.org/record/8308244. For the full dataset used for the analysis performed in the linked article see https://zenodo.org/record/8260668.
