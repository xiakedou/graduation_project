import cv2

pedestrian_cascade = cv2.CascadeClassifier('xml/haarcascade_fullbody.xml')
vehicle_cascade = cv2.CascadeClassifier('xml/cars.xml')


def detect_vehicles(frame, scale=1):
    global vehicle_cascade
    height, width = frame.shape[:2]
    size = (int(width * scale), int(height * scale))
    shrink = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(shrink, cv2.COLOR_BGR2GRAY)
    vehicles = vehicle_cascade.detectMultiScale(gray, 1.2, 3)
    return vehicles


def detect_pedestrians(frame, scale=1):
    global pedestrian_cascade
    height, width = frame.shape[:2]
    size = (int(width * scale), int(height * scale))
    shrink = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(shrink, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.2, 3)
    return pedestrians


def analysis(video, interval):
    capture = cv2.VideoCapture('data/'+video)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    writer = cv2.VideoWriter('output/'+video,
                             int(capture.get(cv2.CAP_PROP_FOURCC)),
                             capture.get(cv2.CAP_PROP_FPS),
                             (int(width), int(height)))
    counter = 0
    # detection variable
    pedestrians = []
    vehicles = []
    # tracking variable
    cars = []
    humans = []
    cv2.MultiTracker_create()
    human_scale = 1
    cars_scale = 1

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        if counter == 0:
            pedestrians = detect_pedestrians(frame, human_scale)
            vehicles = detect_vehicles(frame, cars_scale)
        else:
            # TODO tracking
            pass
        # TODO draw rectangle
        writer.write(frame)
        counter = (counter + 1) % interval
        if cv2.waitKey(1) == 27:
            break
    capture.release()



cv2.imshow('test', img)
cv2.imwrite('output/out.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
