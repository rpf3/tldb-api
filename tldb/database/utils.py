def get_ids(items):
    """
    Return a set of IDs from a list of database model objects
    """
    ids = {x.get("id") for x in items}

    return ids
