import cv2

def get_faces(orig_image):
    image = orig_image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier('mask_detection/haarcascade.xml')
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    #print("[INFO] Found {0} Faces!".format(len(faces)))

    status = False
    boxes = []
    for (x, y, w, h) in faces:
        boxes.append([x,y,w,h])
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return boxes