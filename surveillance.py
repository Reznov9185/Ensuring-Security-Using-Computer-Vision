import numpy as np
import cv2, os, imutils, datetime, MySQLdb
from PIL import Image
from multiprocessing import Pool

#mysql connection


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="surveillance_db")
cur = db.cursor()

room_id = 1
global alarm
alarm = 0

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


def recognize(filename):
    predict_image_pil = Image.open(filename)
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = face_cascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        if conf < 100:
            insert_data = "INSERT INTO access_entries( subject_id, access_time, confidence, origin_x, origin_y, height, width) VALUES (" + str(nbr_predicted) + ",'" + str(datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p")) + "'," + str(conf) + "," + str(x) + "," + str(y) + "," + str(h) + "," + str(w) + ");"
            #print(insert_data)
            cur.execute(insert_data)
            find_subject = "SELECT subject_name FROM subjects WHERE subject_id = " + str(nbr_predicted) + ";"
            print(find_subject)
            cur.execute(find_subject)
            cur.fetchone()
            for (subject_name) in cur:
                name = subject_name[0]
                print "{} is Correctly Recognized with confidence {} at x={}, y={}, w={}, h={} .".format(name, conf, x, y, w, h)
            #print(cur2)
            find_authentication = "SELECT subject_id FROM authentication_table WHERE room_id = " + str(room_id) + ";"
            print(find_authentication)
            cur.execute(find_authentication)
            cur.fetchall()
            global alarm
            for valid_subject in cur:
                if str(valid_subject[0]) == str(nbr_predicted):
                    alarm = 0
                    break
        else:
            alarm = 1
            print "{} not identified with confidence {} at x={}, y={}, w={}, h={} .".format(nbr_predicted, conf, x, y, w, h)
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the loop
        if key == ord("q"):
            break


def motion_detect(camera_id):
    motion_camera_feed = cv2.VideoCapture(camera_id)

    # initialize the first frame in the video stream
    firstFrame = None
    frame_count = 0

    global alarm
    alarm = 0

    # loop over the frames of the video
    while(motion_camera_feed.isOpened()):
        ret, frame = motion_camera_feed.read()
        frame_count += 1
        text = "Unoccupied"
        #cv2.imshow("Camera Feed", frame)
        if motion_camera_feed is not None and frame_count %10  ==0:

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)


            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 500:
                    continue

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                insert_data = "INSERT INTO motion_entries(room_id,occupied_time) VALUES (" + str(room_id) + ",'" + str(datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p")) + "');"
                #print(insert_data)
                cur.execute(insert_data)

            # draw the text and timestamp on the frame
            if text == "Unoccupied":
                b, g, r = 0, 255, 0
            else:
                b, g, r = 0, 0, 255
                if alarm == 1:
                    cv2.putText(frame, "Unauthorized Access (ALARM) ".format(text), (10, frame.shape[0] - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                else:
                    cv2.putText(frame, "Authorized Access".format(text), (10, frame.shape[0] - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (b, g, r), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

            cv2.imshow("Security Feed: "+str(camera_id), frame)
            #cv2.imshow("Thresh", thresh)
            #cv2.imshow("Frame Delta", frameDelta)

            #face detection
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            i = 1
            for (x, y, w, h) in faces:
                img = Image.fromarray(frame[y:y + h, x:x + w])
                face_detected = img.convert('L')
                filename = './detected_faces/face_detected' + str(i) + '.png'
                cv2.imwrite(filename, np.array(face_detected))
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                recognize(filename)
                # roi_gray = gray[y:y+h, x:x+w]
                # roi_color = frame[y:y+h, x:x+w]
                i += 1

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

    # cleanup the camera and close any open windows
    motion_camera_feed.release()
    cv2.destroyAllWindows()


def main_func():
    camera1 = 0
    camera2 = 1
    training()


    motion_detect(camera1)
    #motion_detect(camera2)
    # thread.allocate(motion_detect(camera1))
    # thread.allocate(motion_detect(camera2))
    # cam_queue = multiprocessing.Queue()
    # t1 = threading.Thread(target=motion_detect, args=[camera1])
    # t2 = threading.Thread(target=motion_detect, args=[camera2])

    # pool = Pool(processes=2)
    # results = [pool.apply_async(motion_detect, args=(cam,)) for cam in (0, 1)]
    # for r in results:
    #     r.get()

    db.close()

main_func()