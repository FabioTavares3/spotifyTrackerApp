# 🎵 spotifyTrackerApp

**spotifyTrackerApp** is a web application to track and visualize your Spotify listening statistics, such as most played tracks, artists, albums, and total listening time.

---

## ✨ Features

- 🎶 View your most played **tracks**, **artists**, and **albums**
- ⏱️ See total listening time and play counts
- 📅 Explore your full listening **history**
- 📊 Clean, responsive, and modern interface
- 🔒 All your data stays private

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/spotifyTrackerApp.git
cd spotifyTrackerApp
```

### 2. Install dependencies

- Python 3.x
- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)
- Flask
- SQLAlchemy
- Pandas
- python-dotenv
- MySQL (or compatible database)

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with your Spotify API credentials and database info:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
user=your_db_user
password=your_db_password
host=localhost
database=your_db_name
```

### 4. Run the application

```bash
python execution.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🖥️ Screenshots

| Dashboard                                  | Tracks                               | Artists                                | Albums                               | History                                |
| ------------------------------------------ | ------------------------------------ | -------------------------------------- | ------------------------------------ | -------------------------------------- |
| ![Dashboard](assets/screens/dashboard.png) | ![Tracks](assets/screens/tracks.png) | ![Artists](assets/screens/artists.png) | ![Albums](assets/screens/albums.png) | ![History](assets/screens/history.png) |

---

## 📂 Project Structure

```
spotifyTrackerApp-1/
│
├── dashboard.html
├── tracks.html
├── artists.html
├── albums.html
├── history.html
│
├── assets/
│   ├── css/
│   │   └── style.css
│   └── script/
│       ├── dataFetcher.js
│       └── index.js
│
├── Analysis_queries.py
├── execution.py
└── README.md
```

---

## 📚 Motivation

Most Spotify stats apps are incomplete, paid, or inconvenient. This project is a free, open-source solution to visualize your full Spotify stats, and was also developed as a university project.

---

## 📝 License

MIT License

---

> Made with ❤️ by Andrel Carvalho and Fabio Tavares
