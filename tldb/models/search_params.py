from marshmallow import EXCLUDE, fields, post_load

from tldb.models.schema import BaseSchema


class SearchParams:
    def __init__(self, skip=None, take=None, verbose=None, exact=None):
        self.skip = skip or 0
        self.take = take or 10
        self.verbose = verbose or False
        self.exact = exact or False


class SearchParamsSchema(BaseSchema):
    skip = fields.Integer(allow_none=True)
    take = fields.Integer(allow_none=True)
    verbose = fields.Boolean(allow_none=True)
    exact = fields.Boolean(allow_none=True)

    @post_load
    def create_search_params(self, data, **kwargs):
        return SearchParams(**data)

    class Meta:
        unknown = EXCLUDE
