import cv2

pedestrian_cascade = cv2.CascadeClassifier('xml/haarcascade_fullbody.xml')
vehicle_cascade = cv2.CascadeClassifier('xml/cars.xml')

img = cv2.imread('data/0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.2, 3)
vehicles = vehicle_cascade.detectMultiScale(gray, 1.2, 3)

print type(pedestrians)
print len(vehicles)

for (x, y, w, h) in pedestrians:
    img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
for (x, y, w, h) in vehicles:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('test', img)
cv2.imwrite('output/out.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
