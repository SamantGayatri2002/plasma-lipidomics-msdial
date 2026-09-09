#!/usr/bin/env python3

import csv
import glob
import os
from collections import Counter

BASE = os.path.expanduser("~/Lipidomics/project")

INPUTS = {
    "POS": os.path.join(BASE, "results_pos_msp", "*.mdpeak"),
    "NEG": os.path.join(BASE, "results_neg_msp", "*.mdpeak"),
}

OUTDIR = os.path.join(BASE, "results_summary")
os.makedirs(OUTDIR, exist_ok=True)

summary_rows = []
annotation_rows = []

for polarity, pattern in INPUTS.items():

    files = glob.glob(pattern)

    for filepath in files:

        sample = os.path.basename(filepath).replace(".mdpeak", "")

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")

            total = 0
            mz_matched = 0
            msms_matched = 0
            both_matched = 0

            class_counts = Counter()

            for row in reader:

                total += 1

                mz_match = row["m/z matched"] == "True"
                msms_match = row["MS/MS matched"] == "True"

                if mz_match:
                    mz_matched += 1

                if msms_match:
                    msms_matched += 1

                if mz_match and msms_match:
                    both_matched += 1

                    ontology = row["Ontology"].strip()

                    if ontology:
                        lipid_class = ontology.split(";")[0]
                        class_counts[lipid_class] += 1

                    annotation_rows.append({
                        "Sample": sample,
                        "Polarity": polarity,
                        "Peak ID": row["Peak ID"],
                        "Lipid name": row["Name"],
                        "RT (min)": row["RT (min)"],
                        "Precursor m/z": row["Precursor m/z"],
                        "Height": row["Height"],
                        "Area": row["Area"],
                        "Adduct": row["Adduct"],
                        "Formula": row["Formula"],
                        "Ontology": row["Ontology"],
                        "InChIKey": row["InChIKey"],
                        "Annotation tag": row["Annotation tag (VS1.0)"],
                        "m/z matched": row["m/z matched"],
                        "MS/MS matched": row["MS/MS matched"],
                        "Simple dot product": row["Simple dot product"],
                        "Weighted dot product": row["Weighted dot product"],
                        "Reverse dot product": row["Reverse dot product"],
                        "Matched peaks count": row["Matched peaks count"],
                        "Matched peaks percentage": row["Matched peaks percentage"],
                        "Total score": row["Total score"],
                        "S/N": row["S/N"],
                    })

            summary_rows.append({
                "Sample": sample,
                "Polarity": polarity,
                "Total features": total,
                "m/z matched": mz_matched,
                "MS/MS matched": msms_matched,
                "m/z + MS/MS matched": both_matched,
                "m/z match %": round(100 * mz_matched / total, 2) if total else 0,
                "MS/MS match %": round(100 * msms_matched / total, 2) if total else 0,
            })

            # Save class distribution for this sample
            class_file = os.path.join(
                OUTDIR,
                f"{sample}_lipid_classes.tsv"
            )

            with open(class_file, "w", newline="", encoding="utf-8") as cf:
                writer = csv.writer(cf, delimiter="\t")
                writer.writerow(["Lipid class", "MS/MS-supported annotations"])

                for lipid_class, count in class_counts.most_common():
                    writer.writerow([lipid_class, count])


# ---------------------------------------------------------
# Write sample-level summary
# ---------------------------------------------------------

summary_file = os.path.join(
    OUTDIR,
    "MSDIAL_sample_summary.tsv"
)

with open(summary_file, "w", newline="", encoding="utf-8") as f:

    fieldnames = [
        "Sample",
        "Polarity",
        "Total features",
        "m/z matched",
        "MS/MS matched",
        "m/z + MS/MS matched",
        "m/z match %",
        "MS/MS match %",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(summary_rows)


# ---------------------------------------------------------
# Write annotation table
# ---------------------------------------------------------

annotation_file = os.path.join(
    OUTDIR,
    "MSDIAL_MSMS_annotations.tsv"
)

with open(annotation_file, "w", newline="", encoding="utf-8") as f:

    if annotation_rows:

        fieldnames = list(annotation_rows[0].keys())

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter="\t"
        )

        writer.writeheader()
        writer.writerows(annotation_rows)


print()
print("MS-DIAL summary completed.")
print()
print("Sample summary:")
print(summary_file)
print()
print("MS/MS annotation table:")
print(annotation_file)
print()
print("Output directory:")
print(OUTDIR)
