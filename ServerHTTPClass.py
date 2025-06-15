from DBClass import DBconnector
from flask import Flask, render_template, jsonify


class HTTPServer:

    def bytes_to_str(self,df):
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
        return df
    
    app = Flask(__name__, static_folder='assets', template_folder='.')
    @app.route('/')
    def index(self):
        return render_template('dashboard.html')    
    
    def __init__(self):
        self.app = self.app

    def run(self):
        self.app.run(debug=True, port=8888)

    @app.route('/api/top_artists')
    def top_artists_api(self):
        conn = DBconnector()
        data = conn.get_top_artists_in_DB()
        return jsonify(data.to_dict(orient='records'))

    @app.route('/api/top_albums')
    def top_albums_api(self):
        conn = DBconnector()
        data = conn.get_top_albums_in_DB()
        return jsonify(data.to_dict(orient='records'))

    @app.route('/api/top_tracks')
    def top_tracks_api(self):
        conn = DBconnector()
        data = conn.get_top_tracks_in_DB()
        data = self.bytes_to_str(data)
        return jsonify(data.to_dict(orient='records'))

    @app.route('/api/listening_history')
    def listening_history_api(self):
        conn = DBconnector()
        data = conn.get_history_in_DB()
        return jsonify(data.to_dict(orient='records'))