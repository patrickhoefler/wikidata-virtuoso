#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import gzip
import os
import re
import subprocess
import sys


# Download file and save in cache directory, if it doesn't already exist
def download(url):
    # Define the file name
    outputfilename = 'cache/' + url.split('/')[-1]

    # Create the cache directory
    try:
        os.mkdir('cache')
    except:
        pass

    # Check if file already exists
    if os.path.isfile(outputfilename):
        print("%s already exists" % outputfilename)
        return outputfilename

    # Download file
    print("Downloading %s" % outputfilename)

    wget = subprocess.Popen(
        ['wget', url], cwd=outputfilename.split('/')[0], stdout=subprocess.PIPE
    )
    wget.communicate()

    print("\nDone")

    return outputfilename


# Throw away all triples with a language-tagged object
# where the language is not English.
def english_please(inputfilename):
    # Make sure the output folders exist
    try:
        os.mkdir('output')
    except:
        pass

    # Check if file already exists
    outputfilename = 'output/' + '-'.join(
        [inputfilename.split('/')[-1].split('-')[0]] +
        ['english'] +
        inputfilename.split('/')[-1].split('-')[1:]
    )
    if os.path.isfile(outputfilename):
        print("%s already exists" % outputfilename)
        return outputfilename

    print('Throwing away all triples containing non-English objects')

    # Open UTF-8 encoded, gzipped input file
    with codecs.getreader('utf-8')(gzip.open(inputfilename, 'rb')) \
            as inputfile:

        # Open UTF-8 encoded, gzipped output file
        with codecs.getreader('utf-8')(gzip.open(outputfilename, 'wb')) \
                as outputfile:

            counter = 0
            for line in inputfile:

                # Extract the language of the triple's object, if one is set
                language = re.search(r'\@([^ ]+) \.$', line)

                # If there is no language set or the language is English ...
                if not language or (language and language.group(1) == 'en'):
                    # ... write the line to the output file
                    outputfile.write(line)

                counter += 1
                if counter % 100000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()

    print('\nDone')

    return outputfilename


# Make wikidata-properties.nt.gz compatible with
# wikidata-simple-statements.nt.gz
def simple_properties(inputfilename):
    # Make sure the output folders exist
    try:
        os.mkdir('output')
    except:
        pass

    # Check if file already exists
    outputfilename = '-'.join(
        inputfilename.split('-')[0:2] + ['simple'] + inputfilename.split('-')[2:]
    )
    if os.path.isfile(outputfilename):
        print("%s already exists" % outputfilename)
        return outputfilename

    print('Making properties compatible with simple statements')

    # Open UTF-8 encoded, gzipped input file
    with codecs.getreader('utf-8')(gzip.open(inputfilename, 'rb')) \
            as inputfile:

        # Open UTF-8 encoded, gzipped output file
        with codecs.getreader('utf-8')(gzip.open(outputfilename, 'wb')) \
                as outputfile:

            counter = 0
            for line in inputfile:

                # Repair the subject and write the line to the output file
                outputfile.write(
                    re.sub(
                        r'/entity/P(\d+)',
                        r'/entity/P\1c',
                        line
                    )
                )

                counter += 1
                if counter % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()

    print('\nDone')
