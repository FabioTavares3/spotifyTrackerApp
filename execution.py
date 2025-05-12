from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from datetime import datetime
from Analysis_queries import top_artists,top_albums,top_tracks,listening_history




load_dotenv()

class SpotifyAPI:
    
    
    
    def authentication(self):
        # Authenticate with Spotify API using Spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-recently-played user-read-private user-read-email"
    ))
        return sp

    
    def get_user_info(self) -> dict:
        # Get user information from Spotify API
        authentication = self.authentication()
        user_info = authentication.current_user()
        user_id = user_info['id']
        user_name = user_info['display_name']
        user_email = user_info['email']
        user_country = user_info['country']
        user_product = user_info['product']
        return {
            'user_id': user_id,
            'user_name': user_name,
            'email': user_email,
            'country': user_country,
            'membership': user_product
        }
        

    def get_recently_played(self) -> None:
        authentication = self.authentication()
        recently_played = authentication.current_user_recently_played(limit=50)
        return recently_played
        
     


class DBconnector:
    API = SpotifyAPI()
    get_songs = API.get_recently_played()
    get_user_info = API.get_user_info()
    authentication = API.authentication()
    

    def get_connection(self):
        # Create a connection to the MySQL database using SQLAlchemy
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                os.getenv("user"), os.getenv("password"), os.getenv("host"), 3306, os.getenv("database"))
            )
    
    def execute_query(self,query, params=None) -> None:
        # Execute a query and return the result as a pandas DataFrame
        if params:
            result = pd.read_sql(query, self.get_connection(), params=params)
        else:
            result = pd.read_sql(query, self.get_connection())
        
        return result
    
    def insert_data(self, table, data) -> None:
        # Insert data into the specified table
        try:
            data.to_sql(table, con=self.get_connection(), if_exists='append', index=False)
        except Exception as e:
            print(f"Error inserting data into {table}: {e}")

    def does_song_exist(self, song_id: str) -> bool:
        
        query = "SELECT 1 FROM d_songs WHERE song_id = %s LIMIT 1"
        result = self.execute_query(query, (song_id,))
        if result.empty:
            return False
        else:
            return True
    
    def insert_d_songs(self): 
        # For each song in the recently played list, we need to insert the respective records into the d_songs table
        for song in self.get_songs['items']:
            track= song['track']
            d_songs_data = {
                "song_id": track['id'],
                "song_name": track['name'],
                "duration": track['duration_ms'],
                "album_name": track['album']['name'],
                "song_image": track['album']['images'][0]['url'],
                "song_url": track['external_urls']['spotify'],
                "song_uri": track['uri'],
                "album_url": track['album']['external_urls']['spotify'],
                "album_id": track['album']['id']
    }
            # Check if the song_id already exists in the d_songs table if not, insert them
            if not self.does_song_exist(d_songs_data['song_id']):
                
                d_songs_df = pd.DataFrame(d_songs_data,index = [0])
                self.insert_data('d_songs', d_songs_df)
        
    def does_artist_exist(self, artist_id: str) -> bool:
        # Check if the artist_id already exists in the d_artists table
        query = "SELECT 1 FROM d_artists WHERE artist_id = %s LIMIT 1"
        result = self.execute_query(query, (artist_id,))
        # If the result is empty, it means the artist_id does not exist in the d_artists table
        if result.empty:
            return False
        else:
            return True


    def insert_d_artists(self):
        # For each song in the recently played list, we need to insert the respective records into the d_artists table
        for song in self.get_songs['items']:
            track = song['track']
            for artist in track['artists']:
                artist_details = self.authentication.artist(artist['id'])

                d_artists_data = {
                    "artist_id": artist_details['id'],
                    "artist_name": artist_details['name'],
                    "artist_url": artist_details['external_urls']['spotify'],
                    "artist_uri": artist_details['uri'],
                    "artist_image": artist_details['images'][0]['url'] if artist_details['images'] else None
                }
                # Check if the artist_id already exists in the d_artists table if not, insert them
                if not self.does_artist_exist(d_artists_data['artist_id']):
                    d_artists_df = pd.DataFrame(d_artists_data, index=[0])
                    self.insert_data('d_artists', d_artists_df)
    

    def does_user_exist(self, user_id: str) -> bool:
        # Check if the user_id already exists in the d_user table
        query = "SELECT 1 FROM d_user WHERE user_id = %s LIMIT 1"
        result = self.execute_query(query, (user_id,))
        # If the result is empty, it means the user_id does not exist in the d_user table
        if result.empty:
            return False
        else:
            return True

    
    def insert_d_user(self):
        user_info_df = pd.DataFrame(self.get_user_info, index=[0])
        # Check if the user already exists in the d_user table if not, insert them
        if not self.does_user_exist(user_info_df['user_id'].iloc[0]):
            self.insert_data('d_user', user_info_df)



    def insert_f_played(self):
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
            f_played_df = pd.DataFrame(f_played_data, index=[0])
            self.insert_data('f_played', f_played_df)


    def is_song_stored(self,song_id: str,artist_id: str) -> bool:
        # Check if the song_id and artist_id already exist in the junction table
        query = "SELECT 1 FROM d_songs_artists WHERE song_id = %s AND artist_id = %s LIMIT 1"
        result = self.execute_query(query, (song_id, artist_id))
        # If the result is empty, it means the song_id and artist_id do not exist in the junction table
        if result.empty:
            return False
        else:
            return True

    def insert_junction_table(self):
        # For each song in the recently played list, we need to insert the song_id and artist_id into the junction table
        for song in self.get_songs['items']:
            track = song['track']
            for artist in track['artists']:
                d_songs_data = {
                    "song_id": track['id'],
                    "artist_id": artist['id']
                }
                # Check if the song_id and artist_id already exist in the junction table if not, insert them
                if not self.is_song_stored(d_songs_data['song_id'], d_songs_data['artist_id']):
    
                    d_songs_df = pd.DataFrame(d_songs_data, index=[0])
                    self.insert_data('d_songs_artists', d_songs_df)

    def insert_records(self):
        self.insert_d_songs()
        self.insert_d_artists()
        self.insert_junction_table()
        self.insert_d_user()
        self.insert_f_played()
        print("Records inserted successfully")
    

    #Analysis queries functions. They simply return the result of the query
    # to be used in the analysis notebook.
    def get_history_in_DB(self):
        return self.execute_query(listening_history, (self.get_user_info['user_id'],))

    def get_top_artists_in_DB(self):
        return self.execute_query(top_artists, (self.get_user_info['user_id'],))
    
    def get_top_albums_in_DB(self):
        return self.execute_query(top_albums, (self.get_user_info['user_id'],))
    
    def get_top_tracks_in_DB(self):
        return self.execute_query(top_tracks, (self.get_user_info['user_id'],))


if __name__ == "__main__":
    conn = DBconnector()
    conn.insert_records()