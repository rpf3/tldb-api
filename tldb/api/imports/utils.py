from flask_restx import marshal

from tldb.api.artists.models import artist as artist_model
from tldb.api.tracklists.models import tracklist as tracklist_model
from tldb.api.tracks.models import track as track_model
from tldb.database.artist import Artist as ArtistTable
from tldb.database.track import Track as TrackTable
from tldb.database.tracklist import Tracklist as TracklistTable


def create_artists(artists):
    table = ArtistTable()

    api_model = []

    for artist in artists:
        api_model.append(marshal(artist, artist_model))

    database_response = table.upsert(api_model)

    artist_map = {}

    for artist in database_response:
        artist_map[artist.get("name")] = artist.get("id")

    return artist_map


def create_tracks(tracks, artist_map):
    table = TrackTable()

    api_model = []

    for track in tracks:
        artist_name = track.get("artist").get("name")
        artist_id = artist_map.get(artist_name)

        track["artistId"] = artist_id

        remix = track.get("remix")

        if remix is not None:
            remix_artist = remix.get("artist")

            if remix_artist:
                remix_artist_name = remix_artist.get("name")
                remix_artist_id = artist_map.get(remix_artist_name)

                track["remix"]["artistId"] = remix_artist_id

        api_model.append(marshal(track, track_model))

    database_response = table.upsert(api_model)

    track_map = {}

    for track in database_response:
        track_map[track.get("name")] = track.get("id")

    return track_map


def create_tracklists(tracklists, artist_map, track_map):
    table = TracklistTable()

    api_model = []

    for tracklist in tracklists:
        artist_ids = []

        for artist in tracklist.get("artists"):
            artist_name = artist.get("name")
            artist_id = artist_map.get(artist_name)

            artist_ids.append(artist_id)

        tracklist["artistIds"] = artist_ids

        for track in tracklist.get("tracks"):
            track_name = track.get("name")
            track_id = track_map.get(track_name)

            track["id"] = track_id

        api_model.append(marshal(tracklist, tracklist_model))

    database_response = table.upsert(api_model)

    return database_response
