top_tracks = """
SELECT 
	s.song_name musica, 
    s.album_name album,
    s.song_image,
    s.song_url,
    date_format(f.dt_listened,"%%M %%Y") mês, 
    count(*) quantidade,
    round(sum(f.DURATION/60000),2) minutos_estimados
FROM
	f_played f, d_songs s
WHERE
	s.song_id = f.SONG_ID
AND 
	f.user_id = %s
GROUP BY 
	s.song_name, 
    DATE_FORMAT(f.dt_listened,"%%M %%Y"), 
    s.album_name,
	s.song_image,
    s.song_url
ORDER BY COUNT(*) DESC

"""

top_artists = """
SELECT 
	a.artist_name artista, 
    a.artist_image,
    a.artist_url,
    COUNT(*) quantidade,
    ROUND(SUM(duration/60000),2) as minutos_estimados
FROM
	f_played f, d_artists a, d_songs_artists d
WHERE
	a.artist_id = d.artist_id
AND 
	f.song_id = d.song_id
AND 
	f.user_id = %s
GROUP BY 
	a.artist_name,
    DATE_FORMAT(f.dt_listened,"%%M %%Y"),
    a.artist_image,
    a.artist_url
ORDER BY ROUND(SUM(duration/60000),2) desc
"""

top_albums = """
SELECT 
    s.album_name,
    s.song_image album_image,
    s.album_url,
    date_format(f.dt_listened,"%%M %%Y") month, 
    count(*) quantity,
    round(sum(f.DURATION/60000),2) estimated_total_minutes
FROM
	f_played f, d_songs s
WHERE
	s.song_id = f.SONG_ID
AND 
	f.user_id = %s
GROUP BY 
    DATE_FORMAT(f.dt_listened,"%%M %%Y"), 
    s.album_name,
	s.song_image,
    s.album_url
ORDER BY COUNT(*) DESC
"""


listening_history = """
SELECT 
	f.song_name song, a.artist_name artist, s.album_name album, s.song_image, a.artist_image, timestamp
FROM 
	f_played f, d_artists a, d_songs s, d_songs_artists d
WHERE 
	a.artist_id = d.artist_id
AND 
	f.song_id = d.song_id
AND 
	d.song_id = s.song_id
AND
    f.user_id = %s
"""

