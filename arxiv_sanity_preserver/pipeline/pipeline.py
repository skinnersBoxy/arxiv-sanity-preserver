from urllib.request import urlopen
import multiprocessing
import os
import pickle
import random
import shutil
import sys
import time

from arxiv_sanity_preserver.pipeline.utils import Config

timeout_secs = 10  # after this many seconds we give up on a paper

def process_item(j, numtot, numok, existing_pdfs):
    pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
    assert len(pdfs) == 1
    pdf_url = pdfs[0] + '.pdf'
    basename = pdf_url.split('/')[-1]
    fname = os.path.join(Config.pdf_dir, basename)

    # try retrieve the pdf
    numtot.set(numtot.get() + 1)
    try:
        if not basename in existing_pds:
            print('fetching %s into %s' % (pdf_url, fname))
            req = urlopen(pdf_url, None, timeout_secs)
            with open(fname, 'wb') as fp:
                shutil.copyfileobj(req, fp)
            time.sleep(0.05 + random.uniform(0, 0.1))
        else:
            print('%s exists, skipping' % (fname,))
        numok.set(numok.get() + 1)
    except Exception as e:
        print('error downloading: ', pdf_url)
        print(e)

    print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    pool = multiprocessing.Pool()

    if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
    existing_pds = manager.set(os.listdir(Config.pdf_dir))  # get list of all pdfs we already have

    numok = manager.Value(int, 0)
    numtot = manager.Value(int, 0)
    db = manager.dict(pickle.load(open(Config.db_path, 'rb')))

    num_papers = len(db)

    pool.mapstar(process_item, zip(db.values(), [numtot]*num_papers, [numok]*num_papers, [existing_pdfs]*num_papers)

    print('final number of papers downloaded okay: %d/%d' % (numok.get(), len(db)))

    """
    Very simple script that simply iterates over all files data/pdf/f.pdf
    and create a file data/txt/f.pdf.txt that contains the raw text, extracted
    using the "pdftotext" command. If a pdf cannot be converted, this
    script will not produce the output file.
    """

    # make sure pdftotext is installed
    if not shutil.which('pdftotext'):  # needs Python 3.3+
        print('ERROR: you don\'t have pdftotext installed. Install it first before calling this script')
        sys.exit()

    if not os.path.exists(Config.txt_dir):
        print('creating ', Config.txt_dir)
        os.makedirs(Config.txt_dir)

    existing_texts = manager.set(os.listdir(Config.txt_dir))
    files = os.listdir(Config.pdf_dir)

    for i, f in enumerate(files):  # there was a ,start=1 here that I removed, can't remember why it would be there. shouldn't be, i think.
        txt_basename = f + '.txt'
        if txt_basename in existing_texts:
            print('%d/%d skipping %s, already exists.' % (i, len(files), txt_basename,))
            continue

        pdf_path = os.path.join(Config.pdf_dir, f)
        txt_path = os.path.join(Config.txt_dir, txt_basename)
        cmd = "pdftotext %s %s" % (pdf_path, txt_path)
        os.system(cmd)

        print('%d/%d %s' % (i, len(files), cmd))

        # check output was made
        if not os.path.isfile(txt_path):
            # there was an error with converting the pdf
            print('there was a problem with parsing %s to text, creating an empty text file.' % (pdf_path,))
            os.system('touch ' + txt_path)  # create empty file, but it's a record of having tried to convert

        time.sleep(0.01)  # silly way for allowing for ctrl+c termination

"""
Use imagemagick to convert all pfds to a sequence of thumbnail images
requires: sudo apt-get install imagemagick
"""
import sys
import os
import time
import shutil
from subprocess import Popen

from arxiv_sanity_preserver.pipeline.utils import Config

# make sure imagemagick is installed
if not shutil.which('convert'):  # shutil.which needs Python 3.3+
    print("ERROR: you don\'t have imagemagick installed. Install it first before calling this script")
    sys.exit()

# create if necessary the directories we're using for processing and output
pdf_dir = os.path.join('data', 'pdf')
if not os.path.exists(Config.thumbs_dir): os.makedirs(Config.thumbs_dir)
if not os.path.exists(Config.tmp_dir): os.makedirs(Config.tmp_dir)

# fetch all pdf filenames in the pdf directory
files_in_pdf_dir = os.listdir(pdf_dir)
pdf_files = [x for x in files_in_pdf_dir if x.endswith('.pdf')]  # filter to just pdfs, just in case

# iterate over all pdf files and create the thumbnails
for i, p in enumerate(pdf_files):
    pdf_path = os.path.join(pdf_dir, p)
    thumb_path = os.path.join(Config.thumbs_dir, p + '.jpg')

    if os.path.isfile(thumb_path):
        print("skipping %s, thumbnail already exists." % (pdf_path,))
        continue

    print("%d/%d processing %s" % (i, len(pdf_files), p))

    # take first 8 pages of the pdf ([0-7]), since 9th page are references
    # tile them horizontally, use JPEG compression 80, trim the borders for each image
    # cmd = "montage %s[0-7] -mode Concatenate -tile x1 -quality 80 -resize x230 -trim %s" % (pdf_path, "thumbs/" + f + ".jpg")
    # print "EXEC: " + cmd

    # nvm, below using a roundabout alternative that is worse and requires temporary files, yuck!
    # but i found that it succeeds more often. I can't remember wha thappened anymore but I remember
    # that the version above, while more elegant, had some problem with it on some pdfs. I think.

    # erase previous intermediate files thumb-*.png in the tmp directory
    if os.path.isfile(os.path.join(Config.tmp_dir, 'thumb-0.png')):
        for i in range(8):
            f = os.path.join(Config.tmp_dir, 'thumb-%d.png' % (i,))
            f2 = os.path.join(Config.tmp_dir, 'thumbbuf-%d.png' % (i,))
            if os.path.isfile(f):
                cmd = 'mv %s %s' % (f, f2)
                os.system(cmd)
                # okay originally I was going to issue an rm call, but I am too terrified of
                # running scripted rm queries, so what we will do is instead issue a "mv" call
                # to rename the files. That's a bit safer, right? We have to do this because if
                # some papers are shorter than 8 pages, then results from previous paper will
                # "leek" over to this result, through the intermediate files.

    # spawn async. convert can unfortunately enter an infinite loop, have to handle this.
    # this command will generate 8 independent images thumb-0.png ... thumb-7.png of the thumbnails
    pp = Popen(['convert', '%s[0-7]' % (pdf_path,), '-thumbnail', 'x156', os.path.join(Config.tmp_dir, 'thumb.png')])
    t0 = time.time()
    while time.time() - t0 < 20:  # give it 15 seconds deadline
        ret = pp.poll()
        if not (ret is None):
            # process terminated
            break
        time.sleep(0.1)
    ret = pp.poll()
    if ret is None:
        print("convert command did not terminate in 20 seconds, terminating.")
        pp.terminate()  # give up

    if not os.path.isfile(os.path.join(Config.tmp_dir, 'thumb-0.png')):
        # failed to render pdf, replace with missing image
        missing_thumb_path = os.path.join('arxiv_sanity_preserver/server/static', 'missing.jpg')
        os.system('cp %s %s' % (missing_thumb_path, thumb_path))
        print("could not render pdf, creating a missing image placeholder")
    else:
        cmd = "montage -mode concatenate -quality 80 -tile x1 %s %s" % (os.path.join(Config.tmp_dir, 'thumb-*.png'), thumb_path)
        print(cmd)
        os.system(cmd)

    time.sleep(0.01)  # silly way for allowing for ctrl+c termination
