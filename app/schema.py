from marshmallow import Schema, fields


class QueryString(Schema):
    """
    Class for serialization and deserialization request
    found for schema in DB
    """
    id = fields.String()
    query = fields.String()
    region = fields.String()
    count_items = fields.Integer()
    time_stamp = fields.DateTime()
    links = fields.List(cls_or_instance=fields.String)


class ForStat(Schema):
    id = fields.String(required=True)
    start = fields.DateTime()
    end = fields.DateTime()
