import copy
import json

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


def marshal_track_model(obj):
    result = marshal(obj, track_model)

    del result["id"]

    return result


def get_track_hash(track):
    result = hash(json.dumps(track, sort_keys=True))

    return result


def is_same_track(track1, track2):
    model1 = marshal_track_model(track1)
    model2 = marshal_track_model(track2)

    hash1 = get_track_hash(model1)
    hash2 = get_track_hash(model2)

    result = hash1 == hash2

    return result


def create_track_models(tracks, artist_map):
    models = []

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

        model = marshal_track_model(track)

        models.append(model)

        if remix is not None:
            original = copy.deepcopy(model)
            original["remix"] = None

            models.append(original)

    return models


def create_tracks(tracks, artist_map):
    table = TrackTable()

    track_models = create_track_models(tracks, artist_map)

    api_model = []
    track_map = {}
    track_hashes = set()

    for model in track_models:
        track_name = model.get("name")
        track_hash = get_track_hash(model)

        if track_hash not in track_hashes:
            search_results = table.search_name(track_name)

            if len(search_results) == 0:
                api_model.append(model)
            else:
                match_found = False

                for result in search_results:
                    match_found = is_same_track(model, result)

                    if match_found:
                        track_map[track_hash] = result.get("id")
                        break

                if match_found is False:
                    api_model.append(model)

            track_hashes.add(track_hash)

    database_response = table.upsert(api_model)

    for track in database_response:
        model = marshal_track_model(track)
        track_hash = get_track_hash(model)

        track_map[track_hash] = track.get("id")

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
            model = marshal_track_model(track)
            track_hash = get_track_hash(model)
            track_id = track_map.get(track_hash)

            track["id"] = track_id

        api_model.append(marshal(tracklist, tracklist_model))

    database_response = table.upsert(api_model)

    return database_response
