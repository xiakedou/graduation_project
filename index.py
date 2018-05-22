#!/usr/bin/env python
from importlib import import_module
import os, json
from flask import Flask, render_template, Response, request, jsonify

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

app = Flask(__name__)

@app.route('/')
def index():
    """Start Page"""
    return render_template('start.html')

@app.route('/config')
def config_camera():
    return render_template('config.html')

@app.route('/monitor')
def monitor():
    return render_template('realtime_player.html')

@app.route('/save_polygons', methods=['POST'])
def save_polygons():
    json_data = request.get_json(force=True)
    print json_data
    with open('config/'+json_data['name']+'.json', 'w') as f:
        json.dump(json_data, f, indent=4, separators=(',',':'))
    return jsonify(json_data)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
