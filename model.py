import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pickle

# Load data
df = pd.read_csv('sample_data/spam.csv', encoding='ISO-8859-1')
le = LabelEncoder()
data = df.to_numpy()

X = data[:, 1]
y = data[:, 0]

# NLP preprocessing
tokenizer = RegexpTokenizer('\w+')
sw = set(stopwords.words('english'))
ps = PorterStemmer()

def getStem(review):
    review = review.lower()
    tokens = tokenizer.tokenize(review)
    removed_stopwords = [w for w in tokens if w not in sw]
    stemmed_words = [ps.stem(token) for token in removed_stopwords]
    clean_review = ' '.join(stemmed_words)
    return clean_review

def getDoc(document):
    d = []
    for doc in document:
        d.append(getStem(doc))
    return d

stemmed_doc = getDoc(X)

# Vectorization
cv = CountVectorizer()
vc = cv.fit_transform(stemmed_doc)

# ✅ Fix: Convert to numpy array, not matrix
X = np.asarray(vc.toarray())

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Train model
from sklearn.naive_bayes import MultinomialNB

modelNB = MultinomialNB()
modelNB.fit(X_train, y_train)
print(modelNB.score(X_test, y_test))

# Preprocess for predictions
def prepare(msgs):
    d = getDoc(msgs)
    return cv.transform(d)

# Save model
pickle.dump(modelNB, open('model.pkl', 'wb'))

# Load model
model = pickle.load(open('model.pkl', 'rb'))


