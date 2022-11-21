import numpy as np
import pandas as pd
import pickle

#read csv file
books = pd.read_csv("./datasets/books.csv")
# print(books.head(10))

# print(books.shape)

#cleaning data
books.drop_duplicates()
books.dropna(axis='columns')

books.dropna()

books = books[[
  'title', 'authors', 'categories', 'thumbnail', 'description',
  'average_rating'
]]
# print(books.head())

#creating book tags
books['identify'] = books['categories'] + " " + books['description']

new_books = books[[
  'title', 'authors', 'average_rating', 'thumbnail', 'identify'
]]
print(new_books.head())
# print(new_books['identify'][0])

new_books['identify'] = new_books['identify'].apply(lambda x: str(x))
# print(new_books['identify'][0])

new_books['identify'] = new_books['identify'].apply(lambda x: x.lower())
# print(new_books['identify'][0])

# building a model
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_books['identify']).toarray()
# print(vectors)

# print(cv.get_feature_names_out())

#find similar words to recommend to users

import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


#remmove unnecesary endings from words
def rem_comm(message):
  phrase = []
  for item in message.split():
    phrase.append(ps.stem(item))
  return " ".join(phrase)


new_books['identify'] = new_books['identify'].apply(rem_comm)
# print(new_books['identify'])


pickle.dump(new_books.to_dict(),open('books.pkl','wb'))

#calculate distance between each movie to identify the level of similarity
from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(vectors)

similarity = cosine_similarity(vectors)

pickle.dump(similarity,open('similarity.pkl','wb'))

# print(len(similarity))

# print(similarity[0])


#sorting according to similarity scores and recommending books
def recommend(book):

  #find the index of the books
  book_index = new_books[new_books['title'] == book].index[0]
  distances = similarity[book_index]
  books_list = sorted(list(enumerate(distances)),
                      reverse=True,
                      key=lambda x: x[1])[1:7]

  #to fetch books from indeces
  for i in books_list:
    print(new_books.iloc[i[0]].title)


print(recommend('Gilead'))
