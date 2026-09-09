# Plasma Lipidomics – MS-DIAL Console Workflow

A reproducible command-line workflow for untargeted human plasma lipidomics using MS-DIAL Console.

## Overview

This project documents an MS-DIAL Console workflow for processing Thermo Orbitrap Exploris 240 human plasma lipidomics data acquired using data-dependent acquisition (DDA).

Positive and negative ionization modes are processed separately.

The workflow is designed to be:

- Command-line based
- Reproducible
- Suitable for future automation and Nextflow integration
- Based on MS1 and MS/MS information
- Focused on lipid annotation and summary reporting

## Experimental Setup

| Parameter | Setting |
|---|---|
| Sample type | Human plasma |
| Instrument | Thermo Orbitrap Exploris 240 |
| Acquisition | DDA |
| Ionization | Positive and Negative |
| Mobile phase additive | 10 mM ammonium formate + 0.1% formic acid |
| Input format | mzML |
| MS levels | MS1–MS2 |
| Processing software | MS-DIAL Console |
| Spectral library | MSP lipid spectral library |

## Workflow

```text
Thermo RAW
    |
    v
ProteoWizard MSConvert
    |
    v
mzML
    |
    +-------------------+
    |                   |
    v                   v
Positive              Negative
ion mode              ion mode
    |                   |
    v                   v
MS-DIAL Console       MS-DIAL Console
    |                   |
    v                   v
Feature detection     Feature detection
    |                   |
    v                   v
MS/MS annotation      MS/MS annotation
    |                   |
    +---------+---------+
              |
              v
       Summary tables

```


# Repository Structure
```
project/
├── data/
│   ├── mzml_pos/
│   ├── mzml_neg/
│   └── README.md
│
├── docs/
│   └── MSDIAL_Console_Lipidomics_Workflow_VZ0000099.md
│
├── libraries/
│   └── README.md
│
├── parameters/
│   ├── msdial5_lipidomics_POS_MSP.txt
│   └── msdial5_lipidomics_NEG_MSP.txt
│
├── results/
│   ├── MSDIAL_MSMS_annotations.tsv
│   ├── MSDIAL_sample_summary.tsv
│   ├── VZ0000099_PL_Neg_lipid_classes.tsv
│   └── VZ0000099_PL_Pos_lipid_classes.tsv
│
├── scripts/
│   └── summarize_msdial.py
│
├── .gitignore
└── README.md
```

#Processing

The workflow consists of:

- Conversion of Thermo RAW files to mzML using ProteoWizard MSConvert.
- Separate processing of positive and negative ionization data.
- MS-DIAL feature detection.
- MS/MS-based lipid annotation using MSP spectral libraries.
- Generation of summary tables.
- Lipid-class level summarization.

#Test Sample

The workflow was validated using sample:
```
VZ0000099
```

with separate positive and negative mzML files.

The current results are intended for workflow validation and should not be interpreted as biological conclusions.

# Results

The example results include:

- Total detected features
- MS1 m/z-matched features
- MS/MS-matched features
- MS1 + MS/MS matched features
- Lipid-class summaries
- MS/MS-supported lipid annotations

The lipid annotations should be considered putative annotations supported by the available MS/MS evidence, rather than definitive structural identifications.

#Parameters

Final MS-DIAL parameter files are provided for each polarity:
```
msdial5_lipidomics_POS_MSP.txt
msdial5_lipidomics_NEG_MSP.txt
```
The positive and negative modes use polarity-specific adduct lists and lipid-class settings.

#LBM2 Library Test

An LBM2 lipid library was tested during workflow development.

The LBM2 loading step produced a MessagePack format error in the MS-DIAL Console workflow. Therefore, the final validated workflow uses the MSP spectral library approach.

#Reproducibility

Large raw data files, mzML files, spectral libraries, and generated MS-DIAL files are excluded from the repository using .gitignore.

The detailed workflow documentation is available in:

docs/MSDIAL_Console_Lipidomics_Workflow_VZ0000099.md
Repository Structure
project/
├── data/
│   ├── mzml_pos/
│   ├── mzml_neg/
│   └── README.md
│
├── docs/
│   └── MSDIAL_Console_Lipidomics_Workflow_VZ0000099.md
│
├── libraries/
│   └── README.md
│
├── parameters/
│   ├── msdial5_lipidomics_POS_MSP.txt
│   └── msdial5_lipidomics_NEG_MSP.txt
│
├── results/
│   ├── MSDIAL_MSMS_annotations.tsv
│   ├── MSDIAL_sample_summary.tsv
│   ├── VZ0000099_PL_Neg_lipid_classes.tsv
│   └── VZ0000099_PL_Pos_lipid_classes.tsv
│
├── scripts/
│   └── summarize_msdial.py
│
├── .gitignore
└── README.md
Processing

The workflow consists of:

Conversion of Thermo RAW files to mzML using ProteoWizard MSConvert.
Separate processing of positive and negative ionization data.
MS-DIAL feature detection.
MS/MS-based lipid annotation using MSP spectral libraries.
Generation of summary tables.
Lipid-class level summarization.
Test Sample

The workflow was validated using sample:

VZ0000099

with separate positive and negative mzML files.

The current results are intended for workflow validation and should not be interpreted as biological conclusions.

Results

The example results include:

Total detected features
MS1 m/z-matched features
MS/MS-matched features
MS1 + MS/MS matched features
Lipid-class summaries
MS/MS-supported lipid annotations

The lipid annotations should be considered putative annotations supported by the available MS/MS evidence, rather than definitive structural identifications.

Parameters

Final MS-DIAL parameter files are provided for each polarity:

msdial5_lipidomics_POS_MSP.txt
msdial5_lipidomics_NEG_MSP.txt

The positive and negative modes use polarity-specific adduct lists and lipid-class settings.

LBM2 Library Test

An LBM2 lipid library was tested during workflow development.

The LBM2 loading step produced a MessagePack format error in the MS-DIAL Console workflow. Therefore, the final validated workflow uses the MSP spectral library approach.

#Reproducibility

Large raw data files, mzML files, spectral libraries, and generated MS-DIAL files are excluded from the repository using .gitignore.

The detailed workflow documentation is available in:
```
docs/MSDIAL_Console_Lipidomics_Workflow_VZ0000099.md
```

#Future Development

Planned extensions include:

- Processing multiple patient samples
- Automated batch processing
- Population-level lipidomics analysis
- Quality-control reporting
- Statistical analysis across sample groups
- Pathway/enrichment analysis where an appropriate comparison design is available
- Nextflow workflow implementation


#Author

Gayatri Samant

Bioinformatics – Lipidomics


