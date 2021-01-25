"""
Sample databases of different sizes from a line-delimited list of chemical
structures to be used in training a language model of chemical structure.
"""

import numpy as np
import os
import re
import sys
from itertools import chain

# set working directory
git_dir = os.path.expanduser("~/git/low-data-generative-models")
python_dir = git_dir + "/python"
os.chdir(python_dir)

# import functions
from functions import write_smiles

# parse arguments
smiles_file = sys.argv[1]
output_dir = sys.argv[2]
n_samples = 10

# set maximum length
## determined by analyzing distribution in R
max_len = 250
## for SELFIES, we need to calculate this on  the number of tokens
is_selfies = "selfies" in smiles_file.lower()

# check output directory exists
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

# read SMILES
smiles = []
with open(smiles_file, 'r') as f:
    smiles = [line.strip() for line in f.readlines()]

# filter on length (characters for SMILES, tokens for SELFIES)
before = len(smiles)
if is_selfies:
    smiles = [selfie for selfie in smiles if \
              len(re.findall(r'\[.*?\]|\.', selfie)) <= max_len]
else:
    smiles = [sm for sm in smiles if len(sm) <= max_len]
print("sampling " + str(len(smiles)) + " of " + str(before) + " SMILES " + \
      "with nchar <= " + str(max_len))
# convert to numpy array
smiles = np.asarray(smiles)

# define sample sizes
sample_sizes = list(chain(*[[10 ** power, 5 * 10 ** power] for power in \
                            range(2, 6)]))
sample_sizes.pop(0) ## remove n=100
sample_sizes.append(250000) ## add 250k

# keep only sample sizes smaller than the number of SMILES
sample_sizes = [size for size in sample_sizes if size < len(smiles)]

# repeatedly sample to estimate variance
for sample_idx in range(n_samples):
    np.random.seed(sample_idx)

    # take random samples
    for sample_size in sample_sizes:
        sample = np.random.choice(smiles, size=sample_size)

        # define output file
        base = os.path.basename(smiles_file).split(".txt")[0]
        filename = base + "-n=" + str(sample_size) + "-sample_idx=" + \
            str(sample_idx + 1) + ".txt"
        output_file = os.path.join(output_dir, filename)

        # write to line-delimited file
        write_smiles(sample, output_file)
        print("wrote " + str(sample_size) + " SMILES to output file: " + \
              output_file)

# also write the entire set of filtered SMILES
base = os.path.basename(smiles_file).split(".txt")[0]
filename = base + "-max_len=" + str(max_len) + ".txt"
output_file = os.path.join(output_dir, filename)
write_smiles(smiles, output_file)
