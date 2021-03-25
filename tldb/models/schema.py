from marshmallow import Schema, post_dump


class BaseSchema(Schema):
    @post_dump
    def remove_empty_values(self, data, **kwargs):
        result = {key: value for key, value in data.items() if value is not None}

        return result
