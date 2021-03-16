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
    artist_map = {}
    artist_names = set()

    for artist in artists:
        model = marshal(artist, artist_model)

        if model.get("name") is None:
            model["name"] = "ID"

        artist_name = model.get("name")

        if artist_name not in artist_names:
            search_results = table.search_name(artist_name)

            if len(search_results) == 0:
                api_model.append(model)
            else:
                artist_map[artist_name] = search_results[0].get("id")

            artist_names.add(artist_name)

    database_response = table.upsert(api_model)

    for artist in database_response:
        artist_map[artist.get("name")] = artist.get("id")

    return artist_map


def create_tracks(tracks, artist_map):
    table = TrackTable()

    api_model = []
    track_map = {}
    track_names = set()

    for track in tracks:
        artist_name = track.get("artist").get("name") or "ID"
        artist_id = artist_map.get(artist_name)

        track["artistId"] = artist_id

        remix = track.get("remix")

        if remix is not None:
            remix_artist = remix.get("artist")

            if remix_artist:
                remix_artist_name = remix_artist.get("name") or "ID"
                remix_artist_id = artist_map.get(remix_artist_name)

                track["remix"]["artistId"] = remix_artist_id

        model = marshal(track, track_model)

        if model.get("name") is None:
            model["name"] = "ID"

        track_name = model.get("name")

        if track_name not in track_names:
            search_results = table.search_name(track_name)

            if len(search_results) == 0:
                api_model.append(model)
            else:
                track_map[track_name] = search_results[0].get("id")

            track_names.add(track_name)

    database_response = table.upsert(api_model)

    for track in database_response:
        track_map[track.get("name")] = track.get("id")

    return track_map


def create_tracklists(tracklists, artist_map, track_map):
    table = TracklistTable()

    api_model = []

    for tracklist in tracklists:
        artist_ids = []

        for artist in tracklist.get("artists"):
            artist_name = artist.get("name") or "ID"
            artist_id = artist_map.get(artist_name)

            artist_ids.append(artist_id)

        tracklist["artistIds"] = artist_ids

        for track in tracklist.get("tracks"):
            track_name = track.get("name") or "ID"
            track_id = track_map.get(track_name)

            track["id"] = track_id

        api_model.append(marshal(tracklist, tracklist_model))

    database_response = table.upsert(api_model)

    return database_response
