"""
Format Nouns
------------

Formats the nouns queried from Wikidata using query_nouns.sparql.
"""

import collections
import sys

from scribe_data.utils import export_formatted_data, load_queried_data

LANGUAGE = "English"
QUERIED_DATA_TYPE = "nouns"

file_path = sys.argv[0]

nouns_list, update_data_in_use = load_queried_data(LANGUAGE, QUERIED_DATA_TYPE, file_path)

nouns_formatted = {}

for noun_vals in nouns_list:
    if "singular" in noun_vals.keys():
        if noun_vals["singular"] not in nouns_formatted:
            if "plural" in noun_vals.keys():
                nouns_formatted[noun_vals["singular"]] = {
                    "plural": noun_vals["plural"],
                    "form": "",
                }

                # Assign plural as a new entry after checking if it's its own plural.
                if noun_vals["plural"] not in nouns_formatted:
                    if noun_vals["singular"] != noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": "isPlural",
                            "form": "PL",
                        }

                    else:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": noun_vals["plural"],
                            "form": "PL",
                        }
                else:
                    # Mark plural as a possible form if it isn't already.
                    if nouns_formatted[noun_vals["plural"]]["form"] == "":
                        nouns_formatted[noun_vals["plural"]]["form"] = "PL"

                    # Assign itself as a plural if possible (maybe wasn't for prior versions).
                    if noun_vals["singular"] == noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]]["plural"] = noun_vals[
                            "plural"
                        ]
            else:
                nouns_formatted[noun_vals["singular"]] = {
                    "plural": "",
                    "form": "",
                }

    elif "plural" in noun_vals.keys():
        if noun_vals["plural"] not in nouns_formatted:
            nouns_formatted[noun_vals["plural"]] = {
                "plural": "isPlural",
                "form": "PL",
            }

        else:
            # Mark plural as a possible form if it isn't already.
            if (
                "PL" not in nouns_formatted[noun_vals["plural"]]["form"]
                and nouns_formatted[noun_vals["plural"]]["form"] != ""
            ):
                nouns_formatted[noun_vals["plural"]]["form"] = (
                    nouns_formatted[noun_vals["plural"]]["form"] + "/PL"
                )

            elif nouns_formatted[noun_vals["plural"]]["form"] == "":
                nouns_formatted[noun_vals["plural"]]["form"] = "PL"

nouns_formatted = collections.OrderedDict(sorted(nouns_formatted.items()))

export_formatted_data(LANGUAGE, QUERIED_DATA_TYPE, nouns_formatted, update_data_in_use)
