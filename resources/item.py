import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    # pass by argument first then automatic passing by here item_data alway put in front
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)  # order matter !
    def put(self, item_data, item_id):

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # {"items": list(items.values())} .response with many = true respond with a list , trade off
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):  # pass by argument first then automatic passing by here item_data
        if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
            abort(400, message="Bad request. Ensure 'price' ,'store_id', and 'name' are included in the JSON payload")

        for item in items.values():
            if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
                abort(400, message="item already exists.")

        item_id = uuid.uuid4().hex  # generate random string of letter and number
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item

        return new_item, 201
