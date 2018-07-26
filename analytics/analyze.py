import model.models
from datetime import datetime

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