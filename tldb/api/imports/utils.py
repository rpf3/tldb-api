import copy

from tldb.database import ArtistTable, TracklistTable, TrackTable


def create_artists(artists):
    table = ArtistTable()

    api_model = []
    artist_map = {}
    artist_names = set()

    for artist in artists:
        if artist.name not in artist_names:
            search_results = table.search_name(artist.name)

            if len(search_results) == 0:
                api_model.append(artist)
            else:
                artist_map[artist.name] = search_results[0].get("id")

            artist_names.add(artist.name)

    database_response = table.upsert(api_model)

    for artist in database_response:
        artist_map[artist.name] = artist.id

    return artist_map


def create_track_model(track, artist_map):
    track_copy = copy.deepcopy(track)

    track_copy.artist.id = artist_map.get(track_copy.artist.name)

    remix = track_copy.remix

    if remix is not None:
        remix.artist.id = artist_map.get(remix.artist.name)

    return track_copy


def create_original_tracks(tracks, artist_map):
    table = TrackTable()

    models = []
    hashes = set()
    track_map = {}

    for track in tracks:
        if track.remix is None:
            model = create_track_model(track, artist_map)
        else:
            track_copy = copy.deepcopy(track)
            track_copy.remix = None

            model = create_track_model(track_copy, artist_map)

        track_hash = model.get_unique_hash()

        if track_hash not in hashes:
            search_result = table.get_exact_match(model.name, model.artist.id)

            if search_result is None:
                models.append(model)
                hashes.add(track_hash)
            else:
                track_map[track_hash] = search_result.get("id")

    database_response = table.upsert(models)

    for track in database_response:
        track_hash = track.get_unique_hash()

        track_map[track_hash] = track.id

    return track_map


def create_remix_tracks(tracks, artist_map, original_track_map):
    table = TrackTable()

    models = []
    hashes = set()
    track_map = {}

    for track in tracks:
        if track.remix is not None:
            model = create_track_model(track, artist_map)
            track_hash = model.get_unique_hash()

            if track_hash not in hashes:
                search_result = table.get_exact_match(
                    model.name,
                    model.artist.id,
                    model.remix.name,
                    model.remix.artist.id,
                )

                if search_result is None:
                    original = copy.deepcopy(track)
                    original.remix = None
                    original_model = create_track_model(original, artist_map)
                    original_hash = original_model.get_unique_hash()

                    model.original_id = original_track_map[original_hash]

                    models.append(model)
                else:
                    track_map[track_hash] = search_result.get("id")

    database_response = table.upsert(models)

    for track in database_response:
        track_hash = track.get_unique_hash()

        track_map[track_hash] = track.id

    return track_map


def create_tracks(tracks, artist_map):
    original_track_map = create_original_tracks(tracks, artist_map)
    remix_track_map = create_remix_tracks(tracks, artist_map, original_track_map)

    track_map = {**original_track_map, **remix_track_map}

    return track_map


def create_tracklists(tracklists, artist_map, track_map):
    table = TracklistTable()

    api_model = []

    for tracklist in tracklists:
        for artist in tracklist.artists:
            artist.id = artist_map.get(artist.name)

        for indexed_track in tracklist.tracks:
            track = indexed_track.track
            track_model = create_track_model(track, artist_map)
            track_hash = track_model.get_unique_hash()

            track.id = track_map.get(track_hash)

        api_model.append(tracklist)

    database_response = table.upsert(api_model)

    return database_response
