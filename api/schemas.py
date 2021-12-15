from marshmallow import Schema, fields


class MeanSchema(Schema):
    value_type = fields.String(required=True)
    city = fields.String(required=True)


class RecordsSchema(Schema):
    city = fields.String(required=True)
    start_dt = fields.Date('%Y-%m-%d', required=True)
    end_dt = fields.Date('%Y-%m-%d', required=True)


class MovingAverageSchema(Schema):
    city = fields.String(required=True)
    value_type = fields.String(required=True)
    n = fields.Integer(required=True)
