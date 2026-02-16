#  Emotion Based Movie Recommendation System

A simple web-based movie recommendation project that suggests movies based on the user’s **current emotion/mood**.  
The project includes a small web app (inside `emotion_movie_app/`) and sample UI screenshots.


##  What this project does

- Takes a user’s **emotion** as input (example: Happy, Sad, Angry, Neutral, etc.)
- Maps that emotion to a curated list / category of movies
- Displays emotion-matched movie recommendations in a clean web UI



## 🛠️ Tech Stack

From the repository language mix, this project uses:

- **Python**
- **HTML**
- **CSS**

## How recommendations work (logic)

- User selects / provides an emotion
- Emotion is mapped to a matching movie category
- App displays a list of recommended movies for that emotion

## Future Improvements

- Add real-time emotion detection from webcam (OpenCV / Deep Learning)
- Use TMDB API to fetch posters, ratings, genres, trailers
- Add user login + watchlist + rating-based personalization
- Improve recommendation quality using collaborative filtering

