from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from datetime import datetime

load_dotenv()

class SpotifyAPI:
    
    
    
    def authentication(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-recently-played user-read-private user-read-email"
    ))
        return sp

    
    def get_user_info(self) -> dict:
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
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                os.getenv("user"), os.getenv("password"), os.getenv("host"), 3306, os.getenv("database"))
            )
    
    def execute_query(self,query, params=None) -> None:
        
        if params:
            result = pd.read_sql(query, self.get_connection(), params=params)
        else:
            result = pd.read_sql(query, self.get_connection())
        
        return result
    def insert_data(self, table, data) -> None:
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
            if not self.does_song_exist(d_songs_data['song_id']):
                
                d_songs_df = pd.DataFrame(d_songs_data,index = [0])
                self.insert_data('d_songs', d_songs_df)
        
    def does_artist_exist(self, artist_id: str) -> bool:
        query = "SELECT 1 FROM d_artists WHERE artist_id = %s LIMIT 1"
        result = self.execute_query(query, (artist_id,))
        if result.empty:
            return False
        else:
            return True


    def insert_d_artists(self):
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
               
                if not self.does_artist_exist(d_artists_data['artist_id']):
                    d_artists_df = pd.DataFrame(d_artists_data, index=[0])
                    self.insert_data('d_artists', d_artists_df)
    

    def does_user_exist(self, user_id: str) -> bool:
        query = "SELECT 1 FROM d_user WHERE user_id = %s LIMIT 1"
        result = self.execute_query(query, (user_id,))
        if result.empty:
            return False
        else:
            return True

    
    def insert_d_user(self):
        user_info = self.get_user_info
        user_info_df = pd.DataFrame(user_info, index=[0])
        if not self.does_user_exist(user_info_df['user_id'].iloc[0]):
            self.insert_data('d_user', user_info_df)


    def insert_f_played(self):
        for song in self.get_songs['items']:
            track = song['track']
            dt = datetime.strptime(song['played_at'].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
            date = dt.strftime("%Y-%m-%d %H:%M:%S")
            f_played_data = {
                "song_id": track['id'],
                "song_name": track['name'],
                "artist_id": track['artists'][0]['id'],
                "user_id": self.get_user_info['user_id'],
                "timestamp": date,
                "duration": track['duration_ms']
            }
            f_played_df = pd.DataFrame(f_played_data, index=[0])
            self.insert_data('f_played', f_played_df)


    def insert_records(self):
        self.insert_d_songs()
        self.insert_d_artists()
        self.insert_d_user()
        self.insert_f_played()
        return "Records inserted successfully"
    


