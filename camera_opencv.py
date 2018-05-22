# coding=utf-8
import cv2
from math import sqrt
from base_camera import BaseCamera
from detrac.detect_track import DetectTrack

def too_close(rect1, rect2, min_distance):
    x1 = rect1[0] + rect1[2]/2
    y1 = rect1[1] + rect1[3]/2
    x2 = rect2[0] + rect2[2]/2
    y2 = rect2[1] + rect2[3]/2

    distance = sqrt((x1-x2)**2 + (y1-y2)**2)

    return distance < min_distance


class Camera(BaseCamera):
    video_source = 'data/test1.mp4'
    cars = DetectTrack('xml/cars.xml', 'config/test.json')
    humans = DetectTrack('xml/haarcascade_fullbody.xml', 'config/test.json')

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        count = 0
        counter = 0
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # processs frame
            if count == 0:
                Camera.cars.detect(img)
                Camera.humans.detect(img)
            else:
                Camera.cars.trackers.update(img)
                Camera.humans.trackers.update(img)
            count = (count + 1) % Camera.cars.interval
            counter = (counter + 1) % 50

            if counter == 0:
                for rect in Camera.cars.trackers.getObjects():
                    cv2.rectangle(img,
                                (int(rect[0]), int(rect[1])),
                                (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                                (255, 0, 0),
                                2)
                for rect in Camera.humans.trackers.getObjects():
                    cv2.rectangle(img,
                                (int(rect[0]), int(rect[1])),
                                (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                                (0, 255, 0),
                                2)
            else:
                for car in Camera.cars.trackers.getObjects():
                    for human in Camera.humans.trackers.getObjects():
                        if too_close(car, human, 20):
                            cv2.rectangle(img,
                                (int(car[0]), int(car[1])),
                                (int(car[0] + car[2]), int(car[1] + car[3])),
                                (0, 0, 255),
                                2)
                            cv2.rectangle(img,
                                (int(human[0]), int(human[1])),
                                (int(human[0] + human[2]), int(human[1] + human[3])),
                                (0, 0, 255),
                                2)
                        else:
                            cv2.rectangle(img,
                                (int(car[0]), int(car[1])),
                                (int(car[0] + car[2]), int(car[1] + car[3])),
                                (255, 0, 0),
                                2)
                            cv2.rectangle(img,
                                (int(human[0]), int(human[1])),
                                (int(human[0] + human[2]), int(human[1] + human[3])),
                                (0, 255, 0),
                                2)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
