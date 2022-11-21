import streamlit as st
import pickle
import pandas as pd

def book_func(): 
    books_dict = pickle.load(open('bookspkl.pkl','rb'))
    books = pd.DataFrame(books_dict)
    return books

def similarity_func(): 
    similarity = pickle.load(open('similaritypkl.pkl','rb'))
    return similarity

books = book_func()
similarity = similarity_func()

st.title('Books Recommender System')

def recommend(book):
    book_index = books[books['title'] == book].index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recommended_books = []
    recommended_book_posters = []
    recommended_book_author = []
    recommended_book_rating = []

    for i in books_list:
             if(type(books.iloc[i[0]].thumbnail) != str):
                continue
             recommended_books.append(books.iloc[i[0]].title)
             recommended_book_posters.append(books.iloc[i[0]].thumbnail)
             recommended_book_author.append(books.iloc[i[0]].authors)
             recommended_book_rating.append(books.iloc[i[0]].average_rating)
    return recommended_books, recommended_book_posters, recommended_book_author, recommended_book_rating


selected_book_name = st.selectbox(
    "Type or select a book from the dropdown",
    books['title'].values
)

if st.button('Show Recommendation'):
    names,posters, authors, ratings = recommend(selected_book_name)

    #display with the columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(names[0])
        st.text("Author: " + str(authors[0]))
        st.text("Rating: " + str(ratings[0]))
        st.image(posters[0])
    with col2:
        st.subheader(names[1])
        st.text("Author: " + str(authors[1]))
        st.text("Rating: " + str(ratings[1]))
        st.image(posters[1])
    with col3:
        st.subheader(names[2])
        st.text("Author: " + str(authors[2]))
        st.text("Rating: " + str(ratings[2]))
        st.image(posters[2])


    col1, col2 = st.columns(2)
    with col1:
        st.subheader(names[3])
        st.text("Author: " + str(authors[3]))
        st.text("Rating: " + str(ratings[3]))
        st.image(posters[3])
    with col2:
        st.subheader(names[4])
        st.text("Author: " + str(authors[4]))
        st.text("Rating: " + str(ratings[4]))
        st.image(posters[4])



