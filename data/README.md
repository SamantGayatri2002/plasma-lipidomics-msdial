# Input Data

This directory contains the input mzML files used for the MS-DIAL lipidomics workflow.

The actual mass spectrometry data are intentionally excluded from the GitHub repository because of file size and data-sharing considerations.

Expected structure:

data/
├── mzml_pos/
│   └── sample_POS.mzML
└── mzml_neg/
    └── sample_NEG.mzML

The workflow processes positive and negative ionization modes separately.
