#!/usr/bin/env python3
import time
from functools import wraps

from marshmallow import Schema, fields
from marshmallow.validate import Range

from flask import Flask, jsonify, request
from leds import StripController

app = Flask(__name__)
strip = StripController()


class StateSchema(Schema):
    hue = fields.Int(validate=Range(min=0, max=360))
    value = fields.Float(validate=Range(min=0, max=1))
    saturation = fields.Float(validate=Range(min=0, max=1))
    status = fields.Bool()


class AnimationParamsSchema(Schema):
    hue = fields.Int(missing=360, validate=Range(min=0, max=360))
    count = fields.Int(missing=1, validate=Range(min=1, max=60))
    duration = fields.Int(missing=1, validate=Range(min=1, max=60))


@app.route("/state", methods=["GET"])
def get_state():
    state = strip.get_state()

    return jsonify(state)


@app.route("/state", methods=["PUT", "POST"])
def update_state():
    payload = request.get_json(force=True)
    state = strip.get_state()

    result = StateSchema().load(payload)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        payload = result.data

    state.update(payload)
    strip.set_state(state)

    return jsonify(state)


# Decorator for wrapping animations, Restores state and sets event_running flag.
def animation(function):
    @wraps(function)
    def decorated_func(*args, **kwargs):
        if strip.event_running:
            return jsonify({"error": "Animation is currently running!"}), 400

        strip.event_running = True

        state = strip.get_state()
        values = function(*args, **kwargs)
        strip.set_state(state)

        strip.event_running = False
        return values

    return decorated_func


# Rainbow animation.
@app.route("/animations/rainbow", methods=["PUT", "POST"])
@animation
def show_rainbow():
    args = request.args

    result = AnimationParamsSchema().load(args)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        duration = result.data["duration"]

    for hue in range(0, 360):
        time.sleep(duration / 360)
        strip.set_color([hue, 1, 1], save_state=False)

    return jsonify({"msg": "Rainbow animation completed!"})


# Blink animation.
@app.route("/animations/blink", methods=["PUT", "POST"])
@animation
def show_blink():
    args = request.args

    result = AnimationParamsSchema().load(args)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        count = result.data["count"]
        hue = result.data["hue"]

    for i in range(count):
        for value in range(10, 0, -1):
            time.sleep(0.01)
            strip.set_color([hue, 1, 1 / value], save_state=False)

        time.sleep(0.3)
        for value in range(1, 10):
            time.sleep(0.01)
            strip.set_color([hue, 1, 1 / value], save_state=False)

        strip.set_color([0, 0, 0], save_state=False)
        time.sleep(0.3)

    return jsonify({"msg": "Blink animation completed!"})


@app.errorhandler(404)
@app.errorhandler(400)
@app.errorhandler(405)
def error_handler(error):
    return jsonify({"error": error.description}), error.code


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
