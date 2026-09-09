# MS-DIAL Console Lipidomics Workflow — VZ0000099

## Purpose

This document records the exact MS-DIAL Console workflow used during the test analysis of one human plasma sample, `VZ0000099`, in positive and negative ionization modes.

It is intentionally based on the commands, parameter files, observations, errors, fixes, and results from this workflow. No untested commands or hypothetical parameters are included.

---

# 1. Experimental / data context

- Instrument: Thermo Orbitrap Exploris 240
- Sample type: Human plasma
- Acquisition: DDA
- Separate positive and negative mzML files
- mzML contains MS1 and MS2 data
- RAW → mzML conversion was performed using ProteoWizard MSConvert 3.0.25025
- MSConvert settings used:
  - MS levels 1–2
  - Peak picking options selected
- Positive mzML:
  - `/home/shobita/Lipidomics/project/data/mzml_pos/VZ0000099_PL_Pos.mzML`
- Negative mzML:
  - `/home/shobita/Lipidomics/project/data/mzml_neg/VZ0000099_PL_Neg.mzML`

Verified spectra counts:

| Mode | MS1 | MS2 |
|---|---:|---:|
| POS | 1,777 | 5,294 |
| NEG | 1,813 | 3,715 |

---

# 2. MS-DIAL Console installation / startup commands

MS-DIAL Console had already been installed before this workflow.

Working directory:

```bash
cd ~/Lipidomics
```

The executable is directly inside `~/Lipidomics`:

```bash
./MSDIALCUI
```

The executable reported:

```text
Msdial Console App Version 5.5.251021
```

Usage shown by the program:

```text
MsdialConsoleApp.exe <analysisType> -i <input folder> -o <output folder> -m <method file> -p
```

Supported analysis types shown:

```text
gcms
lcms
```

For this lipidomics workflow, the command uses:

```text
lcms
```

Important: `MSDIALCUI` is an executable, not a directory.

---

# 3. Project directory created for this workflow

The working project structure was:

```text
~/Lipidomics/project/
├── data/
│   ├── mzml_pos/
│   └── mzml_neg/
├── libraries/
├── logs/
├── parameters/
├── results_pos/
└── results_neg/
```

Later, test-specific result folders were created:

```text
~/Lipidomics/project/results_pos_test/
~/Lipidomics/project/results_pos_msp/
~/Lipidomics/project/results_neg_msp/
~/Lipidomics/project/results_summary/
```

---

# 4. Initial parameter file and why it was not reused blindly

An older parameter file already existed:

```text
~/Lipidomics/param_pos.txt
```

Its contents were:

```text
Data type=Centroid
Ion mode=Positive
Target omics=Lipidomics
MS1 tolerance=0.01
MS2 tolerance=0.025
Adduct list=[M+H]+, [M+NH4]+, [M+Na]+
Identification cut-off=80
```

This older configuration was not used as the final workflow because the goal was to establish a current MS-DIAL 5 lipidomics workflow with an appropriate lipid MS/MS library and the required feature/annotation settings.

---

# 5. Library investigation

Initially, no usable lipid MSP library was found in the project.

Searches for `.msp` initially returned only unrelated package/test files.

Searches for `.lbm` / `.lbm2` initially found nothing useful.

A `.dbs` file was found:

```text
./data/mzml_pos/Project-2603091147_Loaded.msp2.dbs
```

The MS-DIAL installation directory also contained:

```text
~/Lipidomics/lib/Reifycs/
```

No usable lipid library was assumed from these files.

---

# 6. LBM2 library attempt

A lipid LBM2 library was obtained:

```text
LipidMsmsBinaryDB-VS68-FiehnO.lbm2
```

The filename initially contained an extra space and was corrected with:

```bash
mv 'LipidMsmsBinaryDB-VS68-FiehnO .lbm2' \
'LipidMsmsBinaryDB-VS68-FiehnO.lbm2'
```

The resulting file was:

```text
/home/shobita/Lipidomics/LipidMsmsBinaryDB-VS68-FiehnO.lbm2
```

The file size was approximately 121 MB.

Its MD5 was verified as:

```text
f7a8a0922be7d77c70f4af6be729ce0a
```

This matched the official library checksum.

---

# 7. First LBM2 run — failure

The initial positive-mode command was:

```bash
./MSDIALCUI lcms \
-i ~/Lipidomics/project/data/mzml_pos/ \
-o ~/Lipidomics/project/results_pos/ \
-m ~/Lipidomics/project/parameters/msdial5_lipidomics_POS.txt \
-p
```

It failed during library loading with:

```text
Loading analysis files..
-- code is invalid. code:167 format:fixstr --
at MessagePack.Decoders.InvalidArrayHeader.Read...
...
CompMs.Common.Parser.MspFileParser.ReadSerializedLbmLibrary
...
CompMs.MsdialCore.Utility.LibraryHandler.ReadLipidMsLibrary
```

The same failure occurred when the command was repeated without `-p`.

Important conclusion:

- The LBM2 file was not corrupt because its MD5 matched the official checksum.
- The failure occurred while deserializing/loading the LBM2 library.
- Therefore the problem was isolated to LBM2 loading rather than the mzML or general MS-DIAL processing.

---

# 8. No-library diagnostic run

To determine whether the mzML and general MS-DIAL configuration worked, a copy of the POS parameter file was made:

```text
~/Lipidomics/project/parameters/msdial5_lipidomics_POS_test_nolbm.txt
```

The only relevant change was:

```text
Lbm file path:
```

The LBM2 path was left blank.

The test result directory was recreated:

```bash
rm -rf ~/Lipidomics/project/results_pos_test
mkdir -p ~/Lipidomics/project/results_pos_test
```

The no-library test was run with:

```bash
./MSDIALCUI lcms \
-i ~/Lipidomics/project/data/mzml_pos/ \
-o ~/Lipidomics/project/results_pos_test/ \
-m ~/Lipidomics/project/parameters/msdial5_lipidomics_POS_test_nolbm.txt
```

This succeeded through:

```text
Loading analysis files..
Start processing..
Reading data...
Peak picking started
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
Deconvolution started
Annotation started
Reading data...
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
Reading data...
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
```

These messages did not stop processing.

Generated files:

```text
AlignResult-2026941253.mdalign
AlignResult-2026941253.mdmsp
AlignResult-2026941253.mzTabM
VZ0000099_PL_Pos.mdmsp
VZ0000099_PL_Pos.mdpeak
```

Conclusion:

> The mzML data and the MS-DIAL Console processing itself were working. The earlier failure was specifically associated with LBM2 loading.

---

# 9. Switch to official lipid MSP libraries

Instead of continuing with the problematic LBM2 file, the workflow used official MS-DIAL lipid MSP libraries.

Positive library:

```text
MSDIAL-InsilicoMSMS-Lipids-Pos.msp
```

Negative library:

```text
MSDIAL-InsilicoMSMS-Lipids-Neg.msp
```

The POS library was downloaded with:

```bash
cd ~/Lipidomics

wget -O MSDIAL-InsilicoMSMS-Lipids-Pos.msp \
https://zenodo.org/records/10953284/files/MSDIAL-InsilicoMSMS-Lipids-Pos.msp
```

The POS MD5 was verified:

```text
e8e13f90c77112801d1c801f1c4e50c1
```

The NEG library was also downloaded and verified:

```text
a4bc74b544be33aadfa5b88b1f2ad71d
```

The final library locations were:

```text
/home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Pos.msp
/home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Neg.msp
```

---

# 10. POS parameter file used

Final POS parameter file:

```text
~/Lipidomics/project/parameters/msdial5_lipidomics_POS_MSP.txt
```

Important settings used in the working POS configuration:

```text
Ion mode: Positive
Msp file path: /home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Pos.msp
Lbm file path:
Solvent type: HCOONH4
Mass slice width: 0.05
CorrDec execute: False
```

Global positive adduct list:

```text
[M+H]+,[M+NH4]+,[M+Na]+,[M+H-H2O]+
```

The searched lipid class line contained positive-mode lipid classes/adducts including:

```text
CAR [M+H]+
LPC [M+H]+
LPC [M+Na]+
LPE [M+H]+
PC [M+H]+
PC [M+Na]+
PE [M+H]+
PE [M+Na]+
PI [M+NH4]+
PI [M+Na]+
PS [M+H]+
PS [M+Na]+
PG [M+NH4]+
EtherLPC [M+H]+
EtherLPE [M+H]+
EtherPC [M+H]+
EtherPE [M+H]+
Sph [M+H]+
DHSph [M+H]+
PhytoSph [M+H]+
SM [M+H]+
SM [M+Na]+
NAE [M+H]+
GPNAE [M+H]+
MG [M+NH4]+
DG [M+NH4]+
DG [M+Na]+
TG [M+NH4]+
TG [M+Na]+
EtherDG [M+NH4]+
EtherTG [M+NH4]+
EtherTG [M+Na]+
CE [M+NH4]+
CoQ [M+H]+
Vitamin_D [M+H]+
Vitamin_D [M+Na]+
VAE [M+H]+
VAE [M+Na]+
```

The configuration also contained the ceramide, glycosphingolipid, sterol and other template-defined positive lipid classes that were retained in the parameter file.

Verified searched adducts included:

```text
[M+H-H2O]
[M+H]
[M+NH4]
[M+Na]
```

---

# 11. POS feature-detection settings used

```text
MS1 data type: Centroid
MS2 data type: Centroid
Smoothing method: LinearWeightedMovingAverage
Smoothing level: 3
Minimum peak height: 300
Minimum peak width: 5
Average peak width: 30
Mass slice width: 0.05
RT begin/end: 0–100
MS1/MS2 mass range: 0–2000
MS1 tolerance centroid: 0.01
MS2 tolerance centroid: 0.025
Accuracy type: IsAccurate
Max charge: 2
Max isotopes: 2
```

---

# 12. POS library annotation settings used

```text
RT tolerance: 2
Weighted/simple/reverse dot product: 0.1
Matched peaks %: 0
Min spectrum match: 1
Total score cutoff: 0.5
MS1 tolerance: 0.01
MS2 tolerance: 0.025
Retention info scoring/filtering: True
```

These settings were retained for the successful test rather than changed simply to increase the number of annotations.

---

# 13. POS filtering settings used

```text
Peak count filter: 0
N percent detected in one group: 0
Remove feature based on peak height fold-change: False
Blank filtering: SampleMaxOverBlankAve
Sample max / blank average: 5
Sample average / blank average: 5
Keep reference matched metabolites: True
Keep suggested metabolites: False
Keep removable features and assigned tag for checking: True
Replace true zero values with 1/2 minimum: False
```

Because this test was a single sample and no blank was available, blank filtering was noted as a consideration. However, no undocumented "off" value was invented, so the existing template setting was retained for this test.

---

# 14. Other POS settings

```text
CorrDec execute: False
CorrDec minimum number of detected samples: 3
Process option: All
Number of threads: 20
```

CorrDec was disabled because this test was a single sample.

No literal DDA parameter was added to the console method file. The mzML itself contained MS1/MS2 data from the DDA acquisition.

---

# 15. Successful POS MS-DIAL run

Output directory:

```text
~/Lipidomics/project/results_pos_msp/
```

Command:

```bash
rm -rf ~/Lipidomics/project/results_pos_msp
mkdir -p ~/Lipidomics/project/results_pos_msp

./MSDIALCUI lcms \
-i ~/Lipidomics/project/data/mzml_pos/ \
-o ~/Lipidomics/project/results_pos_msp/ \
-m ~/Lipidomics/project/parameters/msdial5_lipidomics_POS_MSP.txt
```

The run completed successfully.

Generated:

```text
AlignResult-2026941339.mdalign
AlignResult-2026941339.mdmsp
AlignResult-2026941339.mzTabM
VZ0000099_PL_Pos.mdmsp
VZ0000099_PL_Pos.mdpeak
```

Approximate file sizes observed:

```text
AlignResult-2026941339.mdalign  3632 KB
AlignResult-2026941339.mdmsp    2872 KB
AlignResult-2026941339.mzTabM   2308 KB
VZ0000099_PL_Pos.mdmsp          4900 KB
VZ0000099_PL_Pos.mdpeak         4656 KB
```

---

# 16. POS result statistics

From:

```text
VZ0000099_PL_Pos.mdpeak
```

Results:

```text
Total features: 13032
m/z matched: 2499
MS/MS matched: 472
m/z + MS/MS matched: 472
```

Percentages:

```text
m/z match: 19.18%
MS/MS match: 3.62%
```

MS/MS annotation score distribution:

```text
Minimum total score: 0.885
Median total score: 1.884
Maximum total score: 2.581

Score >= 0.5: 472
Score >= 1.0: 469
Score >= 1.5: 426
Score >= 2.0: 131
```

POS MS/MS-supported lipid classes:

```text
PC       206
TAG      131
SM        73
LPC       19
ACar      15
CE         6
HexCer-NS  6
PE         6
Cer        5
DAG        4
MAG        1
```

Fragment-count distribution for the 472 MS/MS-supported annotations:

```text
1 matched peak    51
2 matched peaks  165
3 matched peaks  146
4 matched peaks   73
5 matched peaks   28
6 matched peaks    8
7 matched peaks    1
```

Therefore:

```text
421 / 472 POS MS/MS annotations had >=2 matched peaks.
```

---

# 17. POS example annotations observed

Examples from the actual output included:

```text
ACar 10:1; [M]+
ACar 10:0; [M]+
ACar 12:1; [M]+
DAG 18:2; DAG 2:0-16:2; [M+NH4]+
ACar 13:1; [M]+
ACar 14:2; [M]+
ACar 12:0; [M]+
ACar 14:1; [M]+
LPC 20:5/0:0
```

High-scoring examples included several ether-PC and ceramide annotations, for example:

```text
PC O-62:8|PC O-40:4_22:4
PC O-50:1|PC O-34:1_16:0
PC O-62:11|PC O-42:7_20:4
Cer 64:1;O2|Cer 41:1;O2/23:0
```

Important interpretation:

These should be described as **MS/MS-supported putative lipid annotations**, not automatically as fully confirmed structural identifications. A high library score does not by itself establish every structural detail such as sn-position or double-bond position.

---

# 18. NEG parameter file

Final NEG parameter file:

```text
~/Lipidomics/project/parameters/msdial5_lipidomics_NEG_MSP.txt
```

Important verified settings:

```text
Ion mode: Negative
Msp file path: /home/shobita/Lipidomics/MSDIAL-InsilicoMSMS-Lipids-Neg.msp
Lbm file path:
adduct list: [M-H]-,[M+HCOO]-
Mass slice width: 0.05
Solvent type: HCOONH4
CorrDec execute: False
```

The searched lipid class line was retained from the official comprehensive template rather than manually deleting positive-mode entries.

The global negative adduct list was intentionally restricted for this run to:

```text
[M-H]-,[M+HCOO]-
```

No additional undocumented adducts were added.

---

# 19. Successful NEG MS-DIAL run

Output directory:

```text
~/Lipidomics/project/results_neg_msp/
```

Command:

```bash
rm -rf ~/Lipidomics/project/results_neg_msp
mkdir -p ~/Lipidomics/project/results_neg_msp

./MSDIALCUI lcms \
-i ~/Lipidomics/project/data/mzml_neg/ \
-o ~/Lipidomics/project/results_neg_msp/ \
-m ~/Lipidomics/project/parameters/msdial5_lipidomics_NEG_MSP.txt
```

The run completed successfully.

Observed messages:

```text
Loading analysis files..
Start processing..
Reading data...
Peak picking started
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
Deconvolution started
Annotation started
Reading data...
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
Reading data...
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
```

These warnings did not stop processing.

Generated:

```text
AlignResult-202697159.mdalign
AlignResult-202697159.mdmsp
AlignResult-202697159.mzTabM
VZ0000099_PL_Neg.mdmsp
VZ0000099_PL_Neg.mdpeak
```

Approximate file sizes:

```text
AlignResult-202697159.mdalign  3816 KB
AlignResult-202697159.mdmsp    2888 KB
AlignResult-202697159.mzTabM   2780 KB
VZ0000099_PL_Neg.mdmsp          4976 KB
VZ0000099_PL_Neg.mdpeak         4680 KB
```

---

# 20. NEG result statistics

From:

```text
VZ0000099_PL_Neg.mdpeak
```

Results:

```text
Total features: 16036
m/z matched: 3254
MS/MS matched: 248
m/z + MS/MS matched: 248
```

Percentages:

```text
m/z match: 20.29%
MS/MS match: 1.55%
```

NEG annotation score statistics:

```text
MS/MS-supported annotations: 248
Minimum total score: 0.869
Mean total score: 2.18708
Maximum total score: 2.606

Score >= 0.5: 248
Score >= 1.0: 244
Score >= 1.5: 235
Score >= 2.0: 122
```

NEG MS/MS-supported lipid classes:

```text
PC          66
SM          66
EtherPC     34
PI          15
LPC         12
AcylGlcADG  10
GlcCer_NS   10
GM3          9
EtherPE      7
LPE          6
GlcCer_AP    4
PE           3
Cer_NP       2
LPI          2
Cer_AS       1
FA           1
```

NEG fragment-count distribution:

```text
1 matched peak     8
2 matched peaks   15
3 matched peaks   73
4 matched peaks   42
5 matched peaks   21
6 matched peaks   10
7 matched peaks   11
8 matched peaks   52
9 matched peaks   13
12 matched peaks   3
```

Therefore:

```text
240 / 248 NEG MS/MS annotations had >=2 matched peaks.
```

---

# 21. NEG example annotations observed

Examples from the actual output included:

```text
LPC 18:1
LPC 16:1
LPC 18:0
LPC 18:2
LPC 14:0
LPC 16:0
LPC 20:3
SM 50:0;O2|SM 34:0;O2/16:0
SM 46:0;O2|SM 32:0;O2/14:0
PE O-52:5|PE O-34:3_18:2
```

Strong NEG matches were predominantly associated with:

```text
[M+HCOO]-
```

for LPC/SM examples and:

```text
[M-H]-
```

for PE examples.

Again, these are **MS/MS-supported putative lipid annotations**, not automatically fully confirmed structural identifications.

---

# 22. Important MS-DIAL output columns

The `.mdpeak` files contained 34 columns:

```text
1  Peak ID
2  Name
3  Scan
4  RT left(min)
5  RT (min)
6  RT right (min)
7  Precursor m/z
8  Height
9  Area
10 Model masses
11 Adduct
12 Isotope
13 Comment
14 Reference RT
15 Reference m/z
16 Formula
17 Ontology
18 InChIKey
19 SMILES
20 Annotation tag (VS1.0)
21 RT matched
22 m/z matched
23 MS/MS matched
24 RT similarity
25 m/z similarity
26 Simple dot product
27 Weighted dot product
28 Reverse dot product
29 Matched peaks count
30 Matched peaks percentage
31 Total score
32 S/N
33 MS1 isotopes
34 MSMS spectrum
```

The most important fields for the current annotation summary were:

```text
Name
RT (min)
Precursor m/z
Height
Area
Adduct
Formula
Ontology
InChIKey
m/z matched
MS/MS matched
Simple dot product
Weighted dot product
Reverse dot product
Matched peaks count
Matched peaks percentage
Total score
S/N
```

---

# 23. Important interpretation of the POS/NEG comparison

For the single test sample:

| Metric | POS | NEG |
|---|---:|---:|
| Total features | 13,032 | 16,036 |
| m/z matches | 2,499 | 3,254 |
| MS/MS-supported | 472 | 248 |
| m/z + MS/MS | 472 | 248 |
| m/z match % | 19.18% | 20.29% |
| MS/MS match % | 3.62% | 1.55% |
| MS/MS annotations with >=2 fragments | 421 | 240 |

Interpretation used during the workflow:

- NEG produced more total detected features.
- NEG produced more m/z matches.
- POS produced more MS/MS-supported annotations.
- NEG nevertheless had strong fragment support among its annotations.
- The difference between POS and NEG annotation counts was not treated as evidence of a processing failure.
- The workflow was not changed simply to maximize annotation counts.

---

# 24. The MS-DIAL warnings encountered

Both POS and NEG runs repeatedly produced:

```text
BinaryDataArrayConverter: cvParam MS:1000522 is not supported yet.
BinaryDataArrayConverter: cvParam (unit) UO:0000110 is not supported yet.
```

The important observation from this test is:

- They appeared during mzML reading.
- Processing continued.
- Peak picking continued.
- Deconvolution continued.
- Annotation continued.
- Output files were generated.

Therefore, for this particular workflow, these messages were treated as **warnings rather than fatal errors**.

They should nevertheless be retained in the run logs/documentation.

---

# 25. Annotation-quality conclusion from this test

The successful test established that:

1. The mzML files can be read by MS-DIAL Console.
2. Peak picking works.
3. Deconvolution works.
4. MSP-based lipid annotation works.
5. POS and NEG can be processed separately.
6. The official MSP libraries load successfully.
7. The LBM2 problem is isolated from the general MS-DIAL/mzML processing.
8. The generated `.mdpeak` files contain quantitative peak areas and annotation information.
9. Both polarities produce MS/MS-supported putative lipid annotations.
10. The workflow is suitable to proceed to the next stage without further parameter changes for this test.

The working annotation language should be:

> **MS/MS-supported putative lipid annotations**

rather than:

> **confirmed lipid identifications**

unless additional experimental evidence is available.

---

# 26. Reusable summary script created

A Python script was created at:

```text
~/Lipidomics/project/scripts/summarize_msdial.py
```

It reads `.mdpeak` files from:

```text
~/Lipidomics/project/results_pos_msp/
~/Lipidomics/project/results_neg_msp/
```

and writes:

```text
~/Lipidomics/project/results_summary/MSDIAL_sample_summary.tsv
~/Lipidomics/project/results_summary/MSDIAL_MSMS_annotations.tsv
```

It also writes per-sample lipid-class files:

```text
<sample>_lipid_classes.tsv
```

The script was run with:

```bash
python ~/Lipidomics/project/scripts/summarize_msdial.py
```

It completed with:

```text
MS-DIAL summary completed.

Sample summary:
/home/shobita/Lipidomics/project/results_summary/MSDIAL_sample_summary.tsv

MS/MS annotation table:
/home/shobita/Lipidomics/project/results_summary/MSDIAL_MSMS_annotations.tsv

Output directory:
/home/shobita/Lipidomics/project/results_summary
```

---

# 27. Summary table generated by the script

Command used:

```bash
column -t -s $'\t' \
~/Lipidomics/project/results_summary/MSDIAL_sample_summary.tsv
```

Actual result:

```text
Sample            Polarity  Total features  m/z matched  MS/MS matched  m/z + MS/MS matched  m/z match %  MS/MS match %
VZ0000099_PL_Pos  POS       13032           2499         472            472                  19.18        3.62
VZ0000099_PL_Neg  NEG       16036           3254         248            248                  20.29        1.55
```

---

# 28. Annotation table inspection command

Command used:

```bash
head -10 ~/Lipidomics/project/results_summary/MSDIAL_MSMS_annotations.tsv | column -t -s $'\t'
```

The resulting table included, among other fields:

```text
Sample
Polarity
Peak ID
Lipid name
RT (min)
Precursor m/z
Height
Area
Adduct
Formula
Ontology
InChIKey
Annotation tag
m/z matched
MS/MS matched
Simple dot product
Weighted dot product
Reverse dot product
Matched peaks count
Matched peaks percentage
Total score
S/N
```

This table is the basis for carrying the MS-DIAL annotations and quantitative peak information into downstream analysis.

---

# 29. Important notes / lessons from the troubleshooting

### Do not assume an LBM2 failure means the mzML is bad

The LBM2 run failed during library deserialization.

The same mzML successfully processed when the LBM2 path was removed.

Therefore, the diagnostic no-LBM run was useful for isolating the problem.

### Verify library integrity

The LBM2 file's MD5 matched the official checksum, so simply redownloading the same file was not considered the solution.

### The official MSP route worked

The official positive and negative MSP libraries loaded and allowed the complete MS-DIAL workflow to finish.

### Do not invent unsupported console parameters

A literal DDA parameter was not added to the method file because the working MS-DIAL Console template did not contain such a field.

### Do not arbitrarily increase annotation counts

The lower NEG annotation count was not used as a reason to loosen the workflow.

### Do not call every library match a confirmed lipid

MS/MS-supported library annotation is not equivalent to complete structural confirmation.

### Keep the warnings in the logs

The `BinaryDataArrayConverter` messages appeared in successful runs and should remain documented rather than hidden.

---

# 30. Current status

For sample `VZ0000099`, the working MS-DIAL stage is:

```text
Thermo RAW
    ↓
MSConvert
    ↓
mzML (MS1 + MS2)
    ↓
MS-DIAL Console 5.5.251021
    ↓
Peak picking
    ↓
Deconvolution
    ↓
MS/MS annotation using official MSP
    ↓
POS / NEG .mdpeak + .mdmsp + .mzTabM + alignment outputs
    ↓
Python summary table
```

The test workflow is working for both polarities.

Multiple-sample processing was intentionally deferred. This document therefore records the **single-sample validation workflow only** and does not introduce untested batch commands or parameters.
