# MS-DIAL Console Lipidomics Workflow
## Technical Documentation and Reproducible Handover

**Human Plasma • DDA • Positive and Negative Ionization**

**Prepared by:** Gayatri Samant  
**Role:** Bioinformatics – Lipidomics

---

## 1. Purpose and Scope

This document records the MS-DIAL Console workflow that was implemented and tested for untargeted human plasma lipidomics. It is intended as a technical handover and reproducibility document, covering installation, library setup, command-line execution, processing parameters, troubleshooting, result generation, and post-processing.

**Scope:** MS-DIAL Console processing and MS/MS-supported lipid annotation only.

**Out of scope:** LipidSearch, LIPID MAPS, LIPEA, and other unrelated lipidomics workflows are intentionally not included.

**Interpretation:** The VZ0000099 results are workflow-validation results. The annotations are putative MS/MS-supported annotations and are not presented as definitive structural identifications or biological conclusions.

---

## 2. Experimental and Computational Setup

| Parameter | Setting |
|---|---|
| Sample type | Human plasma |
| Instrument | Thermo Orbitrap Exploris 240 |
| Acquisition | Data-dependent acquisition (DDA) |
| Ionization | Positive and Negative |
| Mobile phase additive | 10 mM ammonium formate + 0.1% formic acid |
| Input format | mzML |
| MS levels | MS1–MS2 |
| Processing software | MS-DIAL Console |
| Annotation library | MSP lipid spectral library |
| Operating environment | Ubuntu/WSL |

---

## 3. End-to-End Workflow

The implemented workflow separates positive and negative ionization data so that polarity-specific adduct lists, libraries, and processing parameters can be applied independently.

```text
Thermo RAW
    |
    v
ProteoWizard MSConvert
    |
    v
mzML (MS1–MS2)
    |
    +-----------------------+
    |                       |
    v                       v
Positive                  Negative
ion mode                  ion mode
    |                       |
    v                       v
MS-DIAL Console           MS-DIAL Console
    |                       |
    v                       v
Feature detection         Feature detection
    |                       |
    v                       v
MS/MS annotation          MS/MS annotation
    |                       |
    +-----------+-----------+
                |
                v
        MS-DIAL output files
                |
                v
     Python post-processing
                |
                v
 Summary + MS/MS annotations
 + lipid-class distributions
```

---

## 4. MS-DIAL Console Installation and Verification

The MS-DIAL Console package used in the tested workflow was:

```text
MSDIAL.console.v5.5.251021-linux-net8.zip
```

The extracted executable was `MSDIALCUI`.

### Installation / setup commands

```bash
cd ~/Lipidomics
unzip MSDIAL.console.v5.5.251021-linux-net8.zip
chmod +x MSDIALCUI
./MSDIALCUI --help
```

### Verified installed version

```text
Msdial Console App Version 5.5.251021
```

The installed console returned the following command-line usage:

```text
Msdial Console App requires the following args:
MsdialConsoleApp.exe <analysisType> -i <input folder> -o <output folder> -m <method file> -p (option)

Where:
<analysisType> is one of gcms, lcms
<input folder> is the folder containing the files to be processed
<output folder> is the folder to save results
<method file> is a file holding processing properties
<option -p> is an option to generate MTB file to be loaded in MSDIAL GUI application.
```

**Version verification:** The installed executable, rather than the current MS-DIAL website release, is the version documented here: **5.5.251021**.

---

## 5. Spectral Library Setup

Three library files were present in the MS-DIAL working directory. The MSP files were used for the final validated workflow.

An LBM2 library was also tested during workflow development but was not retained as the final library route because the LBM2 loading step produced a MessagePack format error.

| Library | Observed size | Workflow status |
|---|---:|---|
| `MSDIAL-InsilicoMSMS-Lipids-Pos.msp` | 70 MB | Used for positive-mode MSP annotation |
| `MSDIAL-InsilicoMSMS-Lipids-Neg.msp` | 177 MB | Used for negative-mode MSP annotation |
| `LipidMsmsBinaryDB-VS68-FiehnO.lbm2` | 121 MB | Tested; MessagePack loading error; not final |

### Check library files

```bash
ls -lh ~/Lipidomics/*.msp ~/Lipidomics/*.lbm2
```

### Library paths used by the parameter files

```text
/home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Pos.msp
/home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Neg.msp
```

### Final library decision

The final validated workflow uses the **MSP spectral library approach**. The LBM2 route was tested but not used because of the observed MessagePack format loading error.

---

## 6. Project and Data Organization

The working environment contains the MS-DIAL software and libraries, while the organized Git project separates data, parameters, documentation, results, and scripts.

```text
~/Lipidomics/
├── MSDIALCUI
├── MSDIAL-InsilicoMSMS-Lipids-Pos.msp
├── MSDIAL-InsilicoMSMS-Lipids-Neg.msp
├── LipidMsmsBinaryDB-VS68-FiehnO.lbm2
├── param_pos.txt
├── data/
│   ├── mzml_pos/
│   └── mzml_neg/
├── results_pos/
└── project/
    ├── data/
    ├── docs/
    ├── libraries/
    ├── parameters/
    ├── results/
    └── scripts/
```

The Git-based project contains the reproducibility layer for the workflow.

---

## 7. MS-DIAL Parameter Configuration

### 7.1 Positive mode

| Parameter | Value |
|---|---|
| Data type | Centroid |
| Ion mode | Positive |
| Target omics | Lipidomics |
| Ionization | ESI |
| MS1 tolerance | 0.01 |
| MS2 tolerance | 0.025 |
| Adducts | `[M+H]+`, `[M+NH4]+`, `[M+Na]+`, `[M+H-H2O]+` |
| MSP library | `MSDIAL-InsilicoMSMS-Lipids-Pos.msp` |
| Identification cut-off (basic method file) | 80 |
| Minimum peak height | 300 |
| Minimum peak width | 5 |
| Average peak width | 30 |
| Mass slice width | 0.05 |
| RT range | 0–100 min |
| MS1/MS2 mass range | 0–2000 |
| Maximum charge | 2 |
| Maximum isotopes | 2 |
| Smoothing | 3 |
| Deconvolution sigma | 0.5 |
| Threads | 20 |
| Solvent | HCOONH4 |

### 7.2 Negative mode

| Parameter | Value |
|---|---|
| Data type | Centroid |
| Ion mode | Negative |
| Target omics | Lipidomics |
| Ionization | ESI |
| MS1 tolerance | 0.01 |
| MS2 tolerance | 0.025 |
| Adducts | `[M-H]-`, `[M+HCOO]-` |
| MSP library | `MSDIAL-InsilicoMSMS-Lipids-Neg.msp` |
| Minimum peak height | 300 |
| Minimum peak width | 5 |
| Average peak width | 30 |
| Mass slice width | 0.05 |
| RT range | 0–100 min |
| MS1/MS2 mass range | 0–2000 |
| Maximum charge | 2 |
| Maximum isotopes | 2 |
| Smoothing | 3 |
| Deconvolution sigma | 0.5 |
| Threads | 20 |
| Solvent | HCOONH4 |

The detailed final parameter files are retained separately in the project repository as:

```text
msdial5_lipidomics_POS_MSP.txt
msdial5_lipidomics_NEG_MSP.txt
```

They contain the complete searched lipid-class lists and additional annotation, alignment, and filtering settings.

---

## 8. Command-Line Execution

The actual command history shows an initial attempt using `lcmsdda`, followed by the final `lcms` command supported by the installed console.

### Commands recorded during development

```bash
./MsdialConsoleApp lcmsdda -i ./data/mzml_pos/ -o ./results_pos/ -m param_pos.txt -p
chmod +x MSDIALCUI
./MSDIALCUI lcmsdda -i ./data/mzml_pos/ -o ./results_pos/ -m param_pos.txt -p
./MSDIALCUI lcms -i ./data/mzml_pos/ -o ./results_pos/ -m param_pos.txt -p
```

The installed `--help` output verifies `lcms` as a supported analysis type.

### Positive-mode execution

The positive-mode command explicitly recorded in the command history was:

```bash
cd ~/Lipidomics
./MSDIALCUI lcms -i ./data/mzml_pos/ -o ./results_pos/ -m param_pos.txt -p
```

### Negative-mode execution pattern

The organized project is designed to use the same verified console syntax with the polarity-specific input, output, and method files:

```bash
./MSDIALCUI lcms -i ./data/mzml_neg/ -o ./results_neg/ -m param_neg.txt -p
```

**Important:** The positive command above is the command explicitly recorded in the command history. The negative command follows the same verified console syntax with negative-mode directories and method configuration.

---

## 9. mzML Input Verification and Troubleshooting

During workflow development, mzML files were inspected from the Ubuntu environment. Checks included spectrum counts, MS-level annotations, centroid/profile descriptors, and positive/negative scan descriptors.

### Commands used

```bash
grep -m1 -A1 "spectrumList count" NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML
grep -m1 -A1 "spectrumList count" NewTrialMay19_MZML/VZ0000162_PL_Neg.mzML

grep -i "centroid spectrum" NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML | head
grep -i "profile spectrum" NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML | head

grep 'name="ms level"' NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML | head
grep 'value="2"' NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML | wc -l

grep "<spectrum " NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML | wc -l

msconvert NewTrialMay19_MZML/VZ0000162_PL_Pos.mzML \
  --filter "scanNumber [1 1]" --64 --outfile spectrum.txt
```

These checks were used to inspect the mzML structure and MS-level content while diagnosing processing and annotation behavior.

---

## 10. MS-DIAL Output Files

The MS-DIAL run produced standard MS-DIAL project/result files, including project, peak, MS/MS, alignment-related, and mzTabM output.

| Output type | Purpose |
|---|---|
| `.mdproject` | MS-DIAL project information |
| `.mdpeak` | Peak/feature table used for downstream summary extraction |
| `.mdmsp` | MS/MS spectral information |
| `.mdalign` | Alignment result file when generated |
| `.mzTabM` | Molecular feature/metabolomics result export |
| TSV summary files | Human-readable post-processing summaries |

The organized project uses the `.mdpeak` files as the source for Python-based summary generation.

---

## 11. Python Post-Processing

The script:

```text
scripts/summarize_msdial.py
```

reads polarity-specific `.mdpeak` files and generates:

1. Sample-level feature and matching statistics.
2. MS/MS-supported annotation tables.
3. Lipid-class distributions.

### 11.1 Processing logic

For each `.mdpeak` file:

```text
1. Count all features.
2. Count rows where "m/z matched" == True.
3. Count rows where "MS/MS matched" == True.
4. Count rows where both are True.
5. For rows with both matches, extract annotation fields.
6. Extract the first ontology component as the lipid class.
7. Write sample-level and lipid-class TSV files.
```

### 11.2 Annotation fields retained

The generated MS/MS annotation table retains:

- Sample
- Polarity
- Peak ID
- Lipid name
- RT
- Precursor m/z
- Height
- Area
- Adduct
- Formula
- Ontology
- InChIKey
- Annotation tag
- m/z matching status
- MS/MS matching status
- Simple dot product
- Weighted dot product
- Reverse dot product
- Matched peak count
- Matched peak percentage
- Total score
- S/N

### 11.3 Output files

```text
~/Lipidomics/project/results_summary/
    MSDIAL_sample_summary.tsv
    MSDIAL_MSMS_annotations.tsv
    <sample>_lipid_classes.tsv
```

**Important implementation detail:** The script adds a feature to the MS/MS annotation table only when both `m/z matched == True` and `MS/MS matched == True`.

---

## 12. Validation Results — VZ0000099

The example workflow was validated using sample **VZ0000099**, with separate positive and negative mzML files.

| Polarity | Total features | m/z matched | MS/MS matched | Both matched | m/z match % | MS/MS match % |
|---|---:|---:|---:|---:|---:|---:|
| Positive | 13,032 | 2,499 | 472 | 472 | 19.18% | 3.62% |
| Negative | 16,036 | 3,254 | 248 | 248 | 20.29% | 1.55% |

The equality of the MS/MS-matched and m/z + MS/MS-matched counts reflects the post-processing logic and the observed result table: the MS/MS-supported entries retained for annotation were also m/z matched.

---

## 13. Lipid-Class Distribution

### 13.1 Positive ionization

| Lipid class | MS/MS-supported annotations |
|---|---:|
| TAG | 131 |
| EtherPC | 106 |
| PC | 100 |
| SM | 73 |
| LPC | 19 |
| ACar | 15 |
| GlcCer_NS | 6 |
| CE | 6 |
| EtherPE | 5 |
| Cer_NS | 5 |
| DAG | 4 |
| MAG | 1 |
| PE | 1 |

### 13.2 Negative ionization

| Lipid class | MS/MS-supported annotations |
|---|---:|
| SM | 66 |
| PC | 66 |
| EtherPC | 34 |
| PI | 15 |
| LPC | 12 |
| AcylGlcADG | 10 |
| GlcCer_NS | 10 |
| GM3 | 9 |
| EtherPE | 7 |
| LPE | 6 |
| GlcCer_AP | 4 |
| PE | 3 |
| LPI | 2 |
| Cer_NP | 2 |
| FA | 1 |
| Cer_AS | 1 |

These counts represent MS/MS-supported annotation records, not necessarily unique molecular species. They should therefore be used as a workflow summary rather than as a quantitative biological abundance result.

---

## 14. Annotation Evidence and Interpretation

The annotation table retains evidence fields available from the MS-DIAL `.mdpeak` output, including:

- Lipid name
- Retention time
- Precursor m/z
- Peak height
- Peak area
- Adduct
- Molecular formula
- Ontology
- InChIKey
- Annotation tag
- m/z matching status
- MS/MS matching status
- Dot-product scores
- Matched peak count and percentage
- Total score
- Signal-to-noise ratio

### Reporting level

Annotations are reported as **putative MS/MS-supported lipid annotations**.

### Biological interpretation

No case/control comparison, p-value analysis, FDR analysis, or pathway-enrichment conclusion is part of this validation workflow.

---

## 15. Reproducibility and Repository Structure

The organized project contains:

```text
project/
├── data/
│   ├── mzml_pos/
│   ├── mzml_neg/
│   └── README.md
├── docs/
│   └── MSDIAL_Console_Lipidomics_Workflow_VZ0000099.md
├── libraries/
│   └── README.md
├── parameters/
│   ├── msdial5_lipidomics_POS_MSP.txt
│   └── msdial5_lipidomics_NEG_MSP.txt
├── results/
│   ├── MSDIAL_MSMS_annotations.tsv
│   ├── MSDIAL_sample_summary.tsv
│   ├── VZ0000099_PL_Neg_lipid_classes.tsv
│   └── VZ0000099_PL_Pos_lipid_classes.tsv
├── scripts/
│   └── summarize_msdial.py
├── .gitignore
└── README.md
```

Large raw data, mzML files, spectral libraries, and generated MS-DIAL files are excluded from the repository. The parameter files and post-processing script are retained so that the workflow can be reproduced and later automated.

---

## 16. Troubleshooting Record

| Issue / observation | Action or resolution |
|---|---|
| Console executable required execution permission | Used `chmod +x MSDIALCUI`. |
| Initial `lcmsdda` command was attempted | Installed `--help` output showed supported analysis types as `gcms` and `lcms`; final command used `lcms`. |
| Need to verify mzML structure | Used `grep` checks for spectrum count, MS level, centroid/profile descriptors, and scan counts. |
| LBM2 library loading produced MessagePack format error | LBM2 route was not used in the final validated workflow; MSP libraries were used instead. |
| Need reproducible result summaries | Created `summarize_msdial.py` to extract matching statistics, annotations, and lipid-class counts from `.mdpeak` files. |

---

## 17. Final Reproducible Workflow

For a new sample, the intended reproducible sequence is:

1. Convert Thermo RAW to mzML containing the required MS1–MS2 data.
2. Place positive and negative mzML files in separate input directories.
3. Confirm the MS-DIAL Console executable and version with `./MSDIALCUI --help`.
4. Confirm that the polarity-specific MSP library is available.
5. Use the polarity-specific MS-DIAL method file.
6. Run positive and negative modes separately with the MS-DIAL `lcms` console command.
7. Inspect the resulting `.mdpeak`, `.mdmsp`, and `.mdproject` outputs.
8. Run `summarize_msdial.py` on the resulting `.mdpeak` files.
9. Review sample-level matching statistics and lipid-class summaries.
10. Treat annotations as putative MS/MS-supported annotations unless additional orthogonal evidence is available.

---

## 18. Future Development

The project README identifies the following future extensions:

- Processing multiple patient samples
- Automated batch processing
- Population-level lipidomics analysis
- Quality-control reporting
- Statistical analysis across sample groups
- Pathway/enrichment analysis when an appropriate comparison design is available
- Nextflow workflow implementation

These are future extensions and are not represented as completed parts of the current validation workflow.

---

# Appendix A — Key Commands

### Enter MS-DIAL working directory

```bash
cd ~/Lipidomics
```

### Extract the MS-DIAL Console package

```bash
unzip MSDIAL.console.v5.5.251021-linux-net8.zip
```

### Make executable

```bash
chmod +x MSDIALCUI
```

### Verify installation

```bash
./MSDIALCUI --help
```

### Check spectral libraries

```bash
ls -lh ~/Lipidomics/*.msp ~/Lipidomics/*.lbm2
```

### Positive-mode run

```bash
./MSDIALCUI lcms \
  -i ./data/mzml_pos/ \
  -o ./results_pos/ \
  -m param_pos.txt \
  -p
```

### Negative-mode run pattern

```bash
./MSDIALCUI lcms \
  -i ./data/mzml_neg/ \
  -o ./results_neg/ \
  -m param_neg.txt \
  -p
```

### Example mzML checks

```bash
grep -m1 -A1 "spectrumList count" <file>.mzML
grep 'name="ms level"' <file>.mzML | head
grep 'value="2"' <file>.mzML | wc -l
grep "<spectrum " <file>.mzML | wc -l
```

---

# Appendix B — Key Files

| File | Function |
|---|---|
| `MSDIALCUI` | MS-DIAL Console executable |
| `MSDIAL-InsilicoMSMS-Lipids-Pos.msp` | Positive-mode lipid MSP library |
| `MSDIAL-InsilicoMSMS-Lipids-Neg.msp` | Negative-mode lipid MSP library |
| `param_pos.txt` | Positive-mode method file used in the recorded run |
| `msdial5_lipidomics_POS_MSP.txt` | Organized positive-mode parameter file |
| `msdial5_lipidomics_NEG_MSP.txt` | Organized negative-mode parameter file |
| `summarize_msdial.py` | Post-processing and summary-generation script |
| `MSDIAL_sample_summary.tsv` | Sample-level feature/matching summary |
| `MSDIAL_MSMS_annotations.tsv` | MS/MS-supported annotation table |

---

# Appendix C — Technical Notes

The basic positive parameter file recorded an identification cut-off of 80, while the detailed MSP annotation settings use explicit matching tolerances and scoring parameters. For reproducibility, the full parameter files should be treated as the authoritative configuration rather than manually re-entering individual settings.

The workflow deliberately keeps positive and negative modes separate. This avoids mixing polarity-specific adduct definitions and spectral libraries and makes the workflow suitable for later automation.

