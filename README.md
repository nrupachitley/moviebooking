# Movie Booking App

This python-flask based application uses mysql database to reserve seats for a movie. The application uses MVC design pattern.

Flask-mail is used to send booking confirmation email to the user.

Celery is an asynchronous job queue based on distributed message passing. Celery is used to run asynchronous jobs like:
1. Send reminder email to the user 1 hr before the movie.
2. Send movie feedback email to the user after the movie.
3. Calculate popularity index of movies being screened everyday at midnight based on movie feedback and number of bookings per movie.

Modelled content-based recommendation system to recommend movies to user based pervious movie bookings.
