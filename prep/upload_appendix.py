#!/bin/python
# This script is intended to be used with WordFish http://www.github.com/radinformatics/whatisit
# This script will upload the data for the US APPENDIX reports, including basic reports and ids. The labels are not included, they will be derived in the web interface.

# AllowedAnnotation objects store a label name and allowed value, and an Annotation combines one of these objects
# with a list of reports and a user, for easy query/filter

import os
import re
import pandas
import numpy
from whatisit.settings import BASE_DIR

from django.contrib.auth.models import User
from whatisit.apps.wordfish.models import (
    ReportCollection, 
    Report, 
)

# Input data was produced via 
# Data from David Larson @ Stanford Radiology

input_file = "%s/scripts/stanford-US-APPENDIX.tsv" %(BASE_DIR)

if os.path.exists(input_file):
    data = pandas.read_csv(input_file,sep="\t")
    # For the user, get the first (not anon) one
    user = User.objects.get(id=2) # @vsoch
    # First make a new collection
    collection,created = ReportCollection.objects.get_or_create(name="stanford-us-appendix",
                                                                owner=user)
    if created == True:
        collection.save()

    # Add the creator as an annotator
    collection.annotators.add(user)
    collection.save()

    # We don't have labels, just reports
    for row in data.iterrows():
        print("Parsing %s of %s" %(row[0],data.shape[0]))
        report_text = row[1].report_text
        report_id = row[1].report_id
        new_report, created = Report.objects.get_or_create(report_id=report_id,
                                                           report_text=report_text,
                                                           collection=collection)
        if created == True:
            new_report.save()

else:
    print("Cannot find file %s.\n It is not included in the repo, did you get it from @vsoch?" %(input_file))
