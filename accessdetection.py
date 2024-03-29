import numpy as np
import cv2, os, datetime, MySQLdb
from PIL import Image

db = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd="root",
                      db="surveillance_db")
cur1 = db.cursor()
cur2 = db.cursor()

# Haar cascade classifier for classifying frontal face
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if face_cascade.empty():
    raise Exception("Can not find your cascade classifier file . Are you sure, the path is correct ?")

# Start train for recognition
# For face recognition we will use the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()

def training():
    def get_images_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        images = []
        labels = []
        for image_path in image_paths:
            # Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')
            # Get the label of the image
            nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
            # Detect the face in the image
            faces = face_cascade.detectMultiScale(image)
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(nbr)
                cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
                cv2.waitKey(50)
        # return the images list and labels list
        return images, labels

    # Path to the Yale Dataset
    path = './training_faces'
    # Call the get_images_and_labels function and get the face images and the
    # corresponding labels
    images, labels = get_images_labels(path)
    cv2.destroyAllWindows()

    # Perform the training
    recognizer.train(images, np.array(labels))

# recognizer


def recognize(filename):
    predict_image_pil = Image.open(filename).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = face_cascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        if conf < 100:
            insert_data = "INSERT INTO access_entries( subject_id, access_time, confidence, origin_x, origin_y, height, width) VALUES (" + str(nbr_predicted) + ",'" + str(datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p")) + "'," + str(conf) + "," + str(x) + "," + str(y) + "," + str(h) + "," + str(w) + ");"
            #print(insert_data)
            cur1.execute(insert_data)
            find_subject ="SELECT subject_name FROM subjects WHERE subject_id = " + str(nbr_predicted) + ";"
            print(find_subject)
            cur2.execute(find_subject)
            cur2.fetchone()
            for (subject_name) in cur2:
                name = subject_name[0]
                print "{} is Correctly Recognized with confidence {} at x={}, y={}, w={}, h={} .".format(name, conf, x, y, w, h)
            #print(cur2)
        else:
            print "{} not identified with confidence  at x={}, y={}, w={}, h={} .".format(nbr_predicted, conf, x, y, w, h)
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main_func():
    camera_feed = cv2.VideoCapture(0)
    training()
    frame_count = 0
    while (camera_feed.isOpened()):
        ret, frame = camera_feed.read()
        frame_count += 1
        if frame_count % 60 == 0 and camera_feed is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            i = 1
            for (x, y, w, h) in faces:
                img = Image.fromarray(frame[y:y + h, x:x + w])
                face_detected = img.convert('L')
                filename = './detected_faces/face_detected' + str(i) + '.png'
                cv2.imwrite(filename, np.array(face_detected))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                recognize(filename)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                i += 1
        cv2.imshow('Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_feed.release()
    cv2.destroyAllWindows()

main_func()