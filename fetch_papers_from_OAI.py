"""
Queries the Open Archive Initiative (OAI) API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.
"""

import os
import time
import pickle
import random
import argparse
import urllib.request
import xml.etree.ElementTree as ElementTree

from utils import Config, safe_pickle_dump

if __name__ == "__main__":

    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--categories', type=str,
                        default='cs,econ,math,eess,physics',
                        help='Comma separated list of categories to search in. See http://export.arxiv.org/oai2?verb=ListSets for full list of categories.')
    parser.add_argument('--wait-time', type=float, default=5.0, help='Seconds to wait between queries.')
    args = parser.parse_args()

    # misc hardcoded variables
    base_url = 'http://export.arxiv.org/oai2?verb=ListRecords&'  # base api query url
    print('Searching arXiv for the following categoriess: %s' % (args.categories,))

    # lets load the existing database to memory
    try:
        db = pickle.load(open(Config.db_path, 'rb'))
    except Exception as e:
        print('error loading existing database:')
        print(e)
        print('starting from an empty database')
        db = {}

    # -----------------------------------------------------------------------------
    # main loop where we fetch the new results
    print('database has %d entries at start' % (len(db),))
    num_added_total = 0

    for category in args.categories.split(","):
        first_in_category = True
        query = 'set=%s&metadataPrefix=arXivRaw' % (category,)
        while (first_in_category or resumption_token is not None):
            with urllib.request.urlopen(base_url + query) as url:
                response = url.read()

            root = ElementTree.fromstring(response)
            elements = root[2]

            num_added = 0
            num_skipped = 0

            resumption_token = elements.find('{http://www.openarchives.org/OAI/2.0/}resumptionToken')
            if (resumption_token is not None):
                elements = elements[0:-2]

            for i in range(len(elements)):
                element = elements[i]
                j = dict()
                rawid = elements[1][0][0].text
                j['_rawid'] = rawid
                versions = element.findall(".//{http://arxiv.org/OAI/arXivRaw/}version")
                if (len(versions) == 0):
                    break;
                max_version = max(map(lambda x: int(x.attrib['version'][1:]), versions))
                j['_version'] = 'v' + str(max_version)

                # add to our database if we didn't have it before, or if this is a new version
                if not rawid in db or j['_version'] > db[rawid]['_version']:
                    db[rawid] = j
                    num_added += 1
                    num_added_total += 1
                else:
                    num_skipped += 1

            # print some information
            print('Added %d papers, already had %d.' % (num_added, num_skipped))

            print('Sleeping for %i seconds' % (args.wait_time,))
            time.sleep(args.wait_time + random.uniform(0, 3))

            if resumption_token is not None:
                query = 'resumptionToken=%s' % (resumption_token.text,)

                # save the database before we quit, if we found anything new
    if num_added_total > 0:
        print('Saving database with %d papers to %s' % (len(db), Config.db_path))
        safe_pickle_dump(db, Config.db_path)
