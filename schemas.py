from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    status_points = fields.Int()


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    status_points = fields.Int()
    category_id = fields.Int()


class HazardSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    severity_level = fields.Int(required=True)
    items = fields.List(fields.Nested('PlainItemSchema'), dump_only=True)


class HazardItemSchema(Schema):
    hazard_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    hazard = fields.Nested(HazardSchema, dump_only=True)
    item = fields.Nested(PlainItemSchema, dump_only=True)


class ItemSchema(PlainItemSchema):
    category_id = fields.Int(required=True, load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    hazards = fields.List(fields.Nested(HazardSchema()), dump_only=True)


class CategorySchema(PlainCategorySchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    category_id = fields.Int(load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(ItemSchema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
