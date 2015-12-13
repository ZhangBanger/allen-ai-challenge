"""
  Apply Word2Vec to Wikipedia dataset

  Reference: https://code.google.com/p/word2vec/

    Args (unlabeled):
    input_articles: Path to articles.xml
    output_model: somewhere to save the LSA model
"""

import logging, sys, datetime, multiprocessing

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)

input_articles = sys.argv[1]
output_model = sys.argv[2]
demo_questions = sys.argv[3] # question-words.txt analogy example
output_lines = sys.argv[4]

wiki_corpus = WikiCorpus(input_articles, lemmatize=False)

# Write wiki_lines out for future use
lines_output = open(output_lines, 'w')
for text in wiki_corpus.get_texts():
    lines_output.write(" ".join(text) + "\n")

lines_output.close()

model = Word2Vec(
    sentences=LineSentence(wiki_corpus),
    size=400,
    negative=25,
    window=5,
    min_count=5,
    workers=multiprocessing.cpu_count()
)

# Evaluate using analogy file:
# https://word2vec.googlecode.com/svn/trunk/questions-words.txt
model.accuracy(demo_questions)

model.save("%s/%s.model" % (output_model, timestamp))
