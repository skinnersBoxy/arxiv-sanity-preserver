from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='arxiv-sanity-preserver',
   version='1.0',
   description='',
   license="MIT",
   long_description=long_description,
   author='kaparthy,skinnersboxy,vluzko', # What's the norm for who to list as author when you fork something?
   author_email='jordan.jack.schneider@gmail.com',
   url="https://github.com/skinnersBoxy/arxiv-sanity-preserver",
   packages=['arxiv-sanity-preserver'],  #same as name
   install_requires=[], # TODO(skinnersboxy): Figure out which of the packages in requirments.txt are actually minimal.
)
