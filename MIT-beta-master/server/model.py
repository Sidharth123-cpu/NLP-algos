
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from waitress import serve
from flask import Flask, request, jsonify

app = Flask(__name__)

LANGUAGE = "english"

@app.route("/summarization",methods=[ 'POST'])
def main():
    
    try:
        url =  request.get_json()["url"]
        number_of_sentences =  request.get_json()["num"]
    except:
        return "Error: QUERY not included in REQUEST"

    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    big_sentence = ''
    for sentence in summarizer(parser.document, number_of_sentences):
        big_sentence += str(sentence)
        big_sentence += ' '
    return jsonify({"summary" : big_sentence})





if __name__ == "__main__":
    serve(app, port=81)