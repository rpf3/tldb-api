from tldb.models import SearchParamsSchema


def parse_search_args(request):
    schema = SearchParamsSchema()

    request_args = {
        "skip": request.args.get("skip"),
        "take": request.args.get("take"),
        "verbose": request.args.get("verbose") == "1",
    }

    search_params = schema.load(request_args)

    return search_params
