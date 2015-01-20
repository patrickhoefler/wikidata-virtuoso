#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikidata


# The data (= ID) of the Wikidata dump
dump_id = '20150105'

# The files to download
download_urls = [
    "https://tools.wmflabs.org/wikidata-exports/rdf/exports/%s/wikidata-terms.nt.gz" % dump_id,
    "https://tools.wmflabs.org/wikidata-exports/rdf/exports/%s/wikidata-properties.nt.gz" % dump_id,
    "https://tools.wmflabs.org/wikidata-exports/rdf/exports/%s/wikidata-simple-statements.nt.gz" % dump_id
]

# Download and process the files
for url in download_urls:
    filename = wikidata.download(url)
    filename = wikidata.english_please(filename)
    if 'properties' in filename:
        wikidata.simple_properties(filename)
