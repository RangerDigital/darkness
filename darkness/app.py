#!/usr/bin/env python3
import time

from marshmallow import Schema, fields
from marshmallow.validate import Range
from flask import Flask, jsonify, request
from leds import StripController

app = Flask(__name__)
strip = StripController()


class StateSchema(Schema):
    hue = fields.Int(validate=Range(
        min=0, max=360))
    saturation = fields.Float(validate=Range(
        min=0, max=1))
    value = fields.Float(validate=Range(
        min=0, max=1))
    status = fields.Bool()


class AnimationParamsSchema(Schema):
    hue = fields.Int(missing=360, validate=Range(
        min=0, max=360))
    duration = fields.Int(missing=1, validate=Range(
        min=1, max=60))
    count = fields.Int(missing=1, validate=Range(
        min=1, max=60))


@app.route("/state", methods=["GET"])
def get_state():
    hue, saturation, value = strip.hsv

    response = {"hue": hue, "saturation": saturation,
                "value": value, "status": strip.status}

    return jsonify(response)


@app.route("/state", methods=["PUT", "POST"])
def update_state():
    payload = request.get_json(force=True)

    # Get current state dictionary. Updates changed values.
    state = {"hue": strip.hsv[0], "saturation": strip.hsv[1],
             "value": strip.hsv[2], "status": strip.status}

    result = StateSchema().load(payload)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        payload = result.data

    state.update(payload)

    # Update strip with new state.
    strip.status = state["status"]
    strip.set_color([state["hue"], state["saturation"], state["value"]])

    return jsonify(state)

# TODO: Refactor all validation and structure for animations!

# Rainbow animation.
@app.route("/animations/rainbow", methods=["PUT", "POST"])
def show_rainbow():
    result = AnimationParamsSchema().load(request.args)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        duration = result.data["duration"]

    if strip.event_running:
        return jsonify({"error": "Another animation is currently running!"}), 400

    strip.event_running = True

    state_hsv = strip.hsv
    state_status = strip.status

    for hue in range(0, 360):
        time.sleep(duration / 360)
        strip.set_color([hue, 1, 1], save_state=False)

    # Restore state before animation.
    strip.status = state_status
    strip.set_color(state_hsv)

    strip.event_running = False

    return jsonify({"msg": "Rainbow animation completed!"})


# Rainbow animation.
@app.route("/animations/blink", methods=["PUT", "POST"])
def show_blink():
    result = AnimationParamsSchema().load(request.args)
    if result.errors:
        return jsonify({"error": result.errors}), 400
    else:
        count = result.data["count"]
        hue = result.data["hue"]

    if strip.event_running:
        return jsonify({"error": "Animation is currently running!"}), 400

    strip.event_running = True

    state_hsv = strip.hsv
    state_status = strip.status

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

    # Restore state before animation.
    strip.status = state_status
    strip.set_color(state_hsv)

    strip.event_running = False

    return jsonify({"msg": "Blink animation completed!"})


# Custom error messages.
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint with that URL doesn't exist!"}), 404

# TODO: Add more info about error.
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "JSON payload is invalid!"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
