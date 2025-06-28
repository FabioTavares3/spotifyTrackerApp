import time
from sqlalchemy import text
from datetime import datetime
from DBClass import DBconnector
from SpotifyClass import SpotifyAPI

class records_inserter:
    API = SpotifyAPI()
    get_songs = API.get_recently_played()
    get_user_info = API.get_user_info()
    authentication = API.authentication()
    connection =  DBconnector().get_connection()

    def insert_d_songs(self):
        sql = """
            INSERT IGNORE INTO d_songs (song_id, song_name, duration, album_name, song_image, song_url, song_uri, album_url, album_id)
            VALUES (:song_id, :song_name, :duration, :album_name, :song_image, :song_url, :song_uri, :album_url, :album_id)"""
        start_time = time.time()
        songs_id = set()
        # For each song in the recently played list, we need to insert the respective records into the d_songs table
        for song in self.get_songs['items']:
            track = song['track']
            songs_id.add(track['id'])
        songs_ids = list(songs_id)

        song_details_list = []
        for i in range(0, len(songs_ids), 50):
            # Fetch song details in batches of 50
            batch = songs_ids[i:i + 50]
            song_details = self.authentication.tracks(batch)['tracks']
            song_details_list.extend(song_details)
        song_data = []
        # Now we have all song details, we can insert them into the d_songs table
        for song_details in song_details_list:
            d_songs_data = {
                "song_id": song_details['id'],
                "song_name": song_details['name'],
                "duration": song_details['duration_ms'],
                "album_name": song_details['album']['name'],
                "song_image": song_details['album']['images'][0]['url'] if song_details['album']['images'] else None,
                "song_url": song_details['external_urls']['spotify'],
                "song_uri": song_details['uri'],
                "album_url": song_details['album']['external_urls']['spotify'],
                "album_id": song_details['album']['id']
            }
            song_data.append(d_songs_data)
                
        with self.connection.begin() as conn:
            conn.execute(text(sql),song_data)
        end_time = time.time()
        print(f"d_songs table updated successfully in {end_time - start_time:.2f} seconds")

    def insert_d_artists(self):
        sql = """
            INSERT IGNORE INTO d_artists (artist_id, artist_name, artist_url, artist_uri, artist_image)
            VALUES (:artist_id, :artist_name, :artist_url, :artist_uri, :artist_image)
            """
        start_time = time.time()
        artists_id = set()
        # For each song in the recently played list, we need to insert the respective records into the d_artists table
        for song in self.get_songs['items']:
            track = song['track']
            for artist in track['artists']:
                artists_id.add(artist['id'])
        artists_ids = list(artists_id)

        artist_details_list = []
        for i in range(0, len(artists_ids), 50):
            # Fetch artist details in batches of 50
            batch = artists_ids[i:i + 50]
            artist_details = self.authentication.artists(batch)['artists']
            artist_details_list.extend(artist_details)
        artist_data = []
        # Now we have all artist details, we can insert them into the d_artists table
        for artist_details in artist_details_list:
            d_artists_data = {
                "artist_id": artist_details['id'],
                "artist_name": artist_details['name'],
                "artist_url": artist_details['external_urls']['spotify'],
                "artist_uri": artist_details['uri'],
                "artist_image": artist_details['images'][0]['url'] if artist_details['images'] else None
            }
            artist_data.append(d_artists_data)
                
        with self.connection.begin() as conn:
            conn.execute(text(sql), artist_data)
        end_time = time.time()
        print(f"d_artists table updated successfully in {end_time - start_time:.2f} seconds")

    def insert_junction_table(self):
        start_time = time.time()
        seen_new_pairs = []

        
        for song_detail in self.get_songs['items']:
            track = song_detail['track']
            for artist in track['artists']:
                pair = {
                    'song_id':track['id'].strip(),
                    'artist_id' :artist['id'].strip()
                    }
                seen_new_pairs.append(pair)
                
            # Insert the new records into the junction table    
        with self.connection.begin() as conn:
            conn.execute(text("""
                INSERT IGNORE INTO d_songs_artists (song_id, artist_id)
                VALUES (:song_id, :artist_id)
            """), seen_new_pairs)
        finish_time = time.time()
        print(f"d_songs_artists junction table updated successfully in {finish_time - start_time:.2f} seconds")
        
                
    
    
    def insert_d_user(self):
        # Insert user information into the d_user table
        d_user_data = {
            "user_id": self.get_user_info['user_id'],
            "user_name": self.get_user_info['user_name'],
            "email": self.get_user_info['email'],
            "country": self.get_user_info['country'],
            "membership": self.get_user_info['membership'],
            "user_image": self.get_user_info['user_image']
        }
        with self.connection.begin() as conn:
            conn.execute(text("""
                INSERT IGNORE INTO d_user (user_id, user_name, email, country, membership, user_image)
                VALUES (:user_id, :user_name, :email, :country, :membership, :user_image)
            """), d_user_data)
        print("d_user table updated successfully")
        



    def insert_f_played(self):
        start_time = time.time()
        new_plays = []
        # For each song in the recently played list, we need to insert the respective records into the f_played table
        for song in self.get_songs['items']:
            track = song['track']
            dt = datetime.strptime(song['played_at'].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
            date = dt.strftime("%Y-%m-%d %H:%M:%S")
            date2 = dt.strftime("%Y-%m-%d")
            f_played_data = {
                "song_id": track['id'],
                "song_name": track['name'],
                "user_id": self.get_user_info['user_id'],
                "timestamp": date,
                "duration": track['duration_ms'],
                "dt_listened": date2
            }
            new_plays.append(f_played_data)
        with self.connection.begin() as conn:
            conn.execute(text("""
                INSERT IGNORE INTO f_played (song_id, song_name, user_id, timestamp, duration, dt_listened)
                VALUES (:song_id, :song_name, :user_id, :timestamp, :duration, :dt_listened)
            """), new_plays)
        end_time = time.time()
        print(f"f_played table updated successfully in {end_time - start_time:.2f} seconds")

    def insert_records(self):
        start_time = time.time()
        self.insert_d_songs()
        self.insert_d_artists()
        self.insert_junction_table()
        self.insert_d_user()
        self.insert_f_played()
        finish_time = time.time()
        print("Records inserted successfully in {:.2f} seconds".format(finish_time - start_time))