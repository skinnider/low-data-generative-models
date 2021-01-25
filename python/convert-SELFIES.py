"""
Convert a line-delimited list of SMILES into the SELFIES format described by
Krenn et al.
"""

import os
import sys
import selfies
from selfies import encoder
from tqdm import tqdm
print("SELFIES version: %s" % selfies.__version__)

# set working directory
git_dir = os.path.expanduser("~/git/low-data-generative-models")
python_dir = git_dir + "/python"
os.chdir(python_dir)

# parse arguments
smiles_file = sys.argv[1]
output_file = sys.argv[2]

# create directory
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# read cleaned SMILES
smiles = []
with open(smiles_file, 'r') as f:
    smiles = [line.strip() for line in f.readlines()]

# encode to SELFIES
encoded = [encoder(sm) for sm in tqdm(smiles)]

# write to line-delimited file
with open(output_file, 'w') as f:
    for idx, selfie in enumerate(encoded):
        if selfie is None:
            print("could not convert SMILES: {}".format(smiles[idx]))
        else:
            _ = f.write(selfie + '\n')

print("wrote " + str(len(encoded)) + " SELFIES to output file: " + \
      output_file)
