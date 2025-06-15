from DBClass import DBconnector
from Analysis_queries import top_artists,top_albums,top_tracks,listening_history

class AnalysisQueries:

    #Analysis queries functions. They simply return the result of the query
    # to be used in the analysis notebook.
    def get_history_in_DB(self):
        return DBconnector.execute_query(listening_history, (self.get_user_info['user_id'],))

    def get_top_artists_in_DB(self):
        return DBconnector.execute_query(top_artists, (self.get_user_info['user_id'],))
    
    def get_top_albums_in_DB(self):
        return DBconnector.execute_query(top_albums, (self.get_user_info['user_id'],))
    
    def get_top_tracks_in_DB(self):
        return DBconnector.execute_query(top_tracks, (self.get_user_info['user_id'],))
    