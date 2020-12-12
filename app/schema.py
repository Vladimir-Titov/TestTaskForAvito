from marshmallow import Schema, fields


class QueryString(Schema):
    id = fields.String()
    query = fields.String()
    region = fields.String()
    count_items = fields.Integer()
    time_stamp = fields.DateTime()


class ForStat(Schema):
    id = fields.String(required=True)
    start = fields.DateTime()
    end = fields.DateTime()
