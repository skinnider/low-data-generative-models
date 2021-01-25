"""
Convert a line-delimited list of SMILES into the DeepSMILES format described by
O'Boyle and Dalke.
"""

import os
import sys
import deepsmiles
from tqdm import tqdm
print("DeepSMILES version: %s" % deepsmiles.__version__)

# set working directory
git_dir = os.path.expanduser("~/git/low-data-generative-models")
python_dir = git_dir + "/python"
os.chdir(python_dir)

# parse arguments
smiles_file = sys.argv[1]
output_file = sys.argv[2]

# read cleaned SMILES
smiles = []
with open(smiles_file, 'r') as f:
    smiles = [line.strip() for line in f.readlines()]

# encode to DeepSMILES
converter = deepsmiles.Converter(rings=True, branches=True)
dsmiles = [converter.encode(sm) for sm in tqdm(smiles)]

# write to line-delimited file
with open(output_file, 'w') as f:
    for sm in dsmiles:
        _ = f.write(sm + '\n')

print("wrote " + str(len(dsmiles)) + " DeepSMILES to output file: " + \
      output_file)
