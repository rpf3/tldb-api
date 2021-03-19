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


def create_track_model(track, artist_map):
    result = marshal_track_model(track)

    artist_name = track.get("artist").get("name")

    result["artistId"] = artist_map.get(artist_name)

    if track.get("remix"):
        remix_artist_name = track.get("remix").get("artist").get("name")

        result["remix"]["artistId"] = artist_map.get(remix_artist_name)

    return result


def create_original_tracks(tracks, artist_map):
    table = TrackTable()

    models = []
    hashes = set()
    track_map = {}

    for track in tracks:
        remix = track.get("remix")

        if remix is None:
            model = create_track_model(track, artist_map)
        else:
            track_copy = copy.deepcopy(track)
            track_copy["remix"] = None

            model = create_track_model(track_copy, artist_map)

        track_hash = get_track_hash(model)

        if track_hash not in hashes:
            search_result = table.get_exact_match(
                track.get("name"), track.get("artistId")
            )

            if search_result is None:
                models.append(model)
                hashes.add(track_hash)
            else:
                track_map[track_hash] = search_result.get("id")

    database_response = table.upsert(models)

    for track in database_response:
        model = marshal_track_model(track)
        track_hash = get_track_hash(model)

        track_map[track_hash] = track.get("id")

    return track_map


def create_remix_tracks(tracks, artist_map, original_track_map):
    table = TrackTable()

    models = []
    hashes = set()
    track_map = {}

    for track in tracks:
        remix = track.get("remix")

        if remix is not None:
            model = create_track_model(track, artist_map)

            track_hash = get_track_hash(model)

            if track_hash not in hashes:
                track_copy = copy.deepcopy(model)
                track_copy["remix"] = None
                track_copy_hash = get_track_hash(track_copy)

                model["originalId"] = original_track_map[track_copy_hash]

                models.append(model)

    database_response = table.upsert(models)

    track_map = {}

    for track in database_response:
        model = marshal_track_model(track)
        track_hash = get_track_hash(model)

        track_map[track_hash] = track.get("id")

    return track_map


def update_original_tracks(original_track_map):
    table = TrackTable()

    track_ids = original_track_map.values()
    search_results = table.get_versions_by_original(track_ids)

    version_map = {}

    for search_result in search_results:
        result_id = search_result.get("id")
        original_id = search_result.get("originalId")

        if original_id in version_map:
            version_map[original_id].append(result_id)
        else:
            version_map[original_id] = [result_id]

    tracks = table.get_all(track_ids)

    for track in tracks:
        track_id = track.get("id")

        if track_id in version_map:
            track["versions"] = version_map[track_id]

    table.update(tracks)


def create_tracks(tracks, artist_map):
    original_track_map = create_original_tracks(tracks, artist_map)
    remix_track_map = create_remix_tracks(tracks, artist_map, original_track_map)

    update_original_tracks(original_track_map)

    track_map = {**original_track_map, **remix_track_map}

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
            model = create_track_model(track, artist_map)
            track_hash = get_track_hash(model)
            track_id = track_map.get(track_hash)

            track["id"] = track_id

        api_model.append(marshal(tracklist, tracklist_model))

    database_response = table.upsert(api_model)

    return database_response
