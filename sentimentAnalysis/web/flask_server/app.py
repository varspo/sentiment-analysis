import re
from flask import Flask, request
from flask_cors import CORS
import pickle
import pandas as pd
import nltk
stopWords = set(nltk.corpus.stopwords.words('english'))

bow_vectorizer =  pickle.load(open("bow_vectorizer", 'rb'))
clf_bow_knn =  pickle.load(open("clf_bow_knn", 'rb'))

app = Flask(__name__)
CORS(app)

def remove_pattern(text, pattern):
    """
    Docstring: 
    
    remove any pattern from the input text.
    
    Parameters
    ----------
    text: string input, the text to clean.
    pattern : string input, the pattern to remove from the text input.
    
    Returns
    -------
    a cleaned string.
    
    """
    
    # find all the pattern in the input text and return a list of postion indeces 
    r = re.findall(pattern, text)
    
    # replace the pattern with an empty space
    for i in r: text = re.sub(pattern, '', text)
    
    return text

def test(sentence):
    sentence = pd.DataFrame(sentence.split())
    sentence = sentence.apply(lambda x : [word for word in x if not word in stopWords])

    # print(sentence.head())
    # create a word net lemma
    lemma = nltk.stem.WordNetLemmatizer()
    pos = nltk.corpus.wordnet.VERB
    sentence = sentence.apply(lambda x : [lemma.lemmatize(word, pos) for word in x])

    # remove any punctuation
    sentence = sentence.apply(lambda x : [ remove_pattern(word,'\.') for word in x])

    # rejoin the text again to get a cleaned text
    sent = sentence.apply(lambda x : ' '.join(x))
    sent=bow_vectorizer.transform(sent)
    predi = clf_bow_knn.predict(sent)
    return predi

@app.route("/", methods=["GET"])
def home():
    return "<h1>GROUP-14 Sentimental Analysis</h1>&nbsp;<h4>Post on <a href='/api'>/api</a></h4>"

@app.route("/api", methods=["POST"])
def api():
    sentence = request.json['sentence']
    return str(test(request.json['sentence'])[0])

if __name__ == "__main__":
    app.run()