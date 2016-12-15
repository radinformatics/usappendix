#!/usr/bin/env python

import os
import pandas
from glob import glob
import re

# What do the files look like?
file_prefix = 'CLanglotz_finalrad'

# What are we searching for?
exam_name = "US APPENDIX"
search_field = "PROC_DESC" 
data_dir = '/home/vanessa/Documents/Work/Reports'
os.chdir(data_dir)

# Make sure in PWD with data files
files = glob("*")
files = [f for f in files if re.search(file_prefix,f)]

# We want to keep the patient de-id, and the report itself
# WordFish looks report_text and report_id for batch import
subset = pandas.DataFrame()


########################################################################
# SUPPORTING FUNCTIONS
########################################################################


def read_lines(input_file,mode='r',N=2):
    '''function to read raw lines for a header
    :param input_file: the input file to read
    :param mode: the mode to use (read is default)
    :param N: the number of lines to read (2 is default)
    '''
    lines = []
    with open(input_file, mode) as f:
        for x in range(N):
            lines.append(f.readline())
    return lines


def format_header(lines,regex=None):
    '''returns field names that don't correspond to a regular
    expression of interest (default is CHR(* or C
    :param lines: the output from read_lines
    '''
    if regex == None:
        regex = '^CHR[(]|^C'
    header = ''.join([x.strip('\n') for x in lines]).split('||')
    return [x for x in header if not re.search('^CHR[(]|^C',x)]


def apply_header(data,header):
    '''apply_header generates missing header columns
    (always at the end, DX9 and DX10) for a dataset
    this was checked for each dataset by @vsoch
    :param data: the dataset in a pandas df
    :param header: the header, a list of labels
    '''
    difference = len(data.columns) - len(header)
    last_dx = [x for x in header if re.search('DX',x)][-1]
    next_dx = int(re.findall('[0-9]',last_dx)[0]) + 1
    while len(header) < len(data.columns):
        header.append("DX%s" %(next_dx))
        next_dx = next_dx + 1
    data.columns = header
    return data


########################################################################
# MAIN PARSING
########################################################################


for input_file in files:
    print("Adding records from %s..." %(input_file))
    lines = read_lines(input_file)
    header = format_header(lines)
    data = pandas.read_csv(input_file,
                           sep='\t',
                           skiprows=3,
                           low_memory=False,
                           header=None)

    # Add on missing DX* diagnoses    
    data = apply_header(data,header)

    # Search for records we want!
    nonan = data[search_field].str.contains(exam_name).dropna().index
    data = data.loc[nonan]
    records = data[data[search_field].str.contains(exam_name)]
    print("Found %s records!" %(records.shape[0]))
    subset = subset.append(records)


# Are there duplicates, based on patient id?
unique_records = len(subset['DE_PAT_ID'].unique())
total_records = subset.shape[0]
print('Found %s unique records, and %s total' %(unique_records,total_records))
# Found 4930 unique records, and 5914 total

# Save file for now, may want to better format later
subset.to_csv('records-US-APPENDIX.tsv',sep='\t')
