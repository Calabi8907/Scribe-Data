"""
Format Prepositions
-------------------

Formats the prepositions queried from Wikidata using query_prepositions.sparql.
"""

import collections
import json
import os
import sys

LANGUAGE = "Russian"
PATH_TO_SCRIBE_ORG = os.path.dirname(sys.path[0]).split("Scribe-Data")[0]
LANGUAGES_DIR_PATH = (
    f"{PATH_TO_SCRIBE_ORG}/Scribe-Data/src/scribe_data/extract_transform/languages"
)

file_path = sys.argv[0]

update_data_in_use = False  # check if update_data.py is being used
if f"languages/{LANGUAGE}/prepositions/" not in file_path:
    with open("prepositions_queried.json", encoding="utf-8") as f:
        prepositions_list = json.load(f)
else:
    update_data_in_use = True
    with open(
        f"{LANGUAGES_DIR_PATH}/{LANGUAGE}/prepositions/prepositions_queried.json",
        encoding="utf-8",
    ) as f:
        prepositions_list = json.load(f)


def convert_cases(case):
    """
    Converts cases as found on Wikidata to more succinct versions.
    """
    case = case.split(" case")[0]
    if case in ["accusative", "Q146078"]:
        return "Acc"
    elif case in ["dative", "Q145599"]:
        return "Dat"
    elif case in ["genitive", "Q146233"]:
        return "Gen"
    elif case in ["instrumental", "Q192997"]:
        return "Ins"
    elif case in ["prepositional", "Q2114906"]:
        return "Pre"
    elif case in ["locative", "Q202142"]:
        return "Loc"
    else:
        return ""


def order_annotations(annotation):
    """
    Standardizes the annotations that are presented to users where more than one is applicable.

    Parameters
    ----------
        annotation : str
            The annotation to be returned to the user in the command bar.
    """
    single_annotations = ["Akk", "Dat", "Gen", "Ins", "Pre", "Loc", "Nom"]
    if annotation in single_annotations:
        return annotation

    annotation_split = sorted(annotation.split("/"))

    return "/".join(annotation_split)


prepositions_formatted = {}

for prep_vals in prepositions_list:
    if "preposition" in prep_vals.keys() and "case" in prep_vals.keys():
        if prep_vals["preposition"] not in prepositions_formatted:
            prepositions_formatted[prep_vals["preposition"]] = convert_cases(
                prep_vals["case"]
            )

        else:
            prepositions_formatted[prep_vals["preposition"]] += "/" + convert_cases(
                prep_vals["case"]
            )

for k in prepositions_formatted:
    prepositions_formatted[k] = order_annotations(prepositions_formatted[k])

prepositions_formatted = collections.OrderedDict(sorted(prepositions_formatted.items()))

export_dir = "../formatted_data/"
export_path = os.path.join(export_dir, "prepositions.json")
if update_data_in_use:
    export_path = f"{LANGUAGES_DIR_PATH}/{LANGUAGE}/formatted_data/prepositions.json"

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

with open(
    export_path,
    "w",
    encoding="utf-8",
) as file:
    json.dump(prepositions_formatted, file, ensure_ascii=False, indent=0)

print(f"Wrote file prepositions.json with {len(prepositions_formatted)} prepositions.")
