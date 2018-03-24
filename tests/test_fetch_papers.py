import unittest
from pipeline import fetch_papers
import feedparser

class TestFetchPapers(unittest.TestCase):

    def test_encode_feedparser_dict(self):
        sample_arxiv_api_response = open("tests/sample_arxiv_api_response","rb")
        parse = feedparser.parse(sample_arxiv_api_response.read())
        sample_arxiv_api_response.close()
        encoded = fetch_papers.encode_feedparser_dict(parse.entries[0])
        print(parse)
        print()
        print(encoded)

if __name__ == '__main__':
    unittest.main()
