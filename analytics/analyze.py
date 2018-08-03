import model.models
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def popularityIndex():
    today_date = datetime.today().strftime('%Y-%m-%d')
    data_booking = model.models.popularity_index_booking(today_date)
    data_rating = model.models.popularity_index_rating()

    d_booking = {}
    for data in data_booking:
        if data[1] not in d_booking:
            d_booking[data[1]] = {}
            d_booking[data[1]][data[2]] = 1
        else:
            if data[2] not in d_booking[data[1]]:
                d_booking[data[1]][data[2]] = 1
            else:
                d_booking[data[1]][data[2]] += 1

    d_rating = {}
    for data in data_rating:
        d_rating[data[1]] = data[2]

    movie_list = d_booking.keys()
    for movie in movie_list:
        theaters = 0
        bookings = 0
        for theater in d_booking[movie].keys():
            theaters += 1
            bookings += d_booking[movie][theater]
            popularity_index = (0.2 * float(d_rating[movie])) + (0.8 * (float(bookings) / theaters))
            model.models.insert_popularity_index(movie, float(popularity_index))


def genre_recommendations(title, titles, indices, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1].all(), reverse=True)
    sim_scores = sim_scores[0:2]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]


def recommendation(today_date, login_id):
    current_movies = model.models.current_movies(today_date)
    person_movies = model.models.person_movies(login_id)

    final_movies = current_movies + person_movies

    df = pd.DataFrame(list(final_movies), columns=['movie_id', 'movie_name', 'genre'])
    df['genre'] = df['genre'].str.split('/')
    df['genre'] = df['genre'].fillna("").astype('str')

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['genre'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    titles = df['movie_name']
    indices = pd.Series(df.index, index=df['movie_name'])

    recommended_movies = []
    for movie in person_movies:
        similar_movies = genre_recommendations(movie[1], titles, indices, cosine_sim).head(2)
        similar_movies_list = similar_movies.tolist()
        for similar_movie in similar_movies_list:
            if similar_movie != movie[1]:
                recommended_movies.append(similar_movie)
                break

    return recommended_movies
