import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy

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