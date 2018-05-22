#coding=utf-8
"""
    Author: HeKe
    Date:2018/05/07
"""
from cv2 import CascadeClassifier, MultiTracker
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY
from cv2 import TrackerKCF_create
from Polygon import Polygon
from json import load
import logging
import cv2, time


class DetectTrack(object):
    def __init__(self, xml_path, config_path, scale=1.2, interval=25, threshold=0.7):
        """
        Init a DetectTrack instance
        :param xml_path: HAAR xml file to be loaded
        :param config_path: config json file
        :param scale: image shrink rate
        :return: Instance of DetectTrack
        """
        # object classifier
        self.classifier = CascadeClassifier(xml_path)
        # specifying how much the image size is reduced at each image scale
        self.scale = scale
        # trackers for detected objects
        self.trackers = MultiTracker()
        # detection results
        self.objects = []
        # detect every interval frames
        self.interval = interval
        # threshold for judge whether the object and the tracker is the same one
        self.threshold = threshold
        # load config json file
        try:
            f = open(config_path, 'r')
            config_data = load(f)
            self.selector = Polygon(config_data['polygons'])
        except IOError:
            raise Exception('Load config file failed!', config_path) 

    def load_config(self, config_path):
        with open(config_path,'r') as f:
            config_data = load(f)
            self.selector = Polygon(config_data['polygons'])

    def detect(self, frame):
        """
        Detect object from one frame
        :param frame: Image where to find object
        :return: None
        """
        # Step 1: Get detected results, note that old results will be cleared
        gray = cvtColor(frame, COLOR_BGR2GRAY)
        self.objects = self.classifier.detectMultiScale(gray, self.scale, 3, 0, (60, 60))
        # Step 2: Pre-process trackers, remove missed targets
        # TODO: Compare detected results with tracked objects to find missed targets
        del self.trackers
        self.trackers = MultiTracker()
        for obj in self.objects:
            # Add objects into trackers only if it is in the polygon
            if self.selector.isInside(obj[0] + obj[2]/2, obj[1] + obj[3]/2):
                self.trackers.add(newTracker=TrackerKCF_create(),
                                image=frame,
                                boundingBox=(obj[0], obj[1], obj[2], obj[3]))

    def overlap(self, obj, tracker):
        """
        compute join/union
        :param obj:
        :param tracker:
        :return:
        """
        x_max = max(obj[0], tracker[0])
        y_max = max(obj[1], tracker[1])

        x_min = min(obj[0]+obj[2], tracker[0]+obj[2])
        y_min = min(obj[1]+obj[3], tracker[1]+tracker[3])

        if x_min > x_max and y_min > y_max:
            join = (x_min - x_max)*(y_min - y_max)
            union = (obj[1]*obj[3] + tracker[1]*tracker[3] - join)
            return join/union
        else:
            return 0


if __name__ == '__main__':
    a = DetectTrack("../xml/cars.xml", "../config/test.json")
    b = DetectTrack('../xml/haarcascade_fullbody.xml', '../config/test.json')
    logging.basicConfig(filename='log/test.log', level=logging.INFO)
    capture = cv2.VideoCapture('../data/test1.mp4')
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    writer = cv2.VideoWriter("../output/test1.mp4",
                             int(capture.get(cv2.CAP_PROP_FOURCC)),
                             capture.get(cv2.CAP_PROP_FPS),
                             (int(width), int(height)))
    count = 0
    while True:
        ret, img = capture.read()
        if not ret:
            break
        if count % 25 == 0:
            # time to detect
            start = time.time()
            a.detect(img)
            b.detect(img)
            end = time.time()
            logging.info('detect time:%f' % (end-start))
        else:
            # time to track
            start = time.time()
            a.trackers.update(img)
            b.trackers.update(img)
            end = time.time()
            logging.info('update time:%f' % (end-start))
        count = (count + 1) % a.interval
        for rect in a.trackers.getObjects():
            cv2.rectangle(img,
                          (int(rect[0]), int(rect[1])),
                          (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                          (0, 0, 255),
                          2
                          )
        for rect in b.trackers.getObjects():
            cv2.rectangle(img,
                          (int(rect[0]), int(rect[1])),
                          (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                          (255, 0, 0),
                          2
                          )
        # cv2.imshow('test', img)
        writer.write(img)
        if cv2.waitKey(1) == 27:
            break
    capture.release()
    cv2.destroyAllWindows()
