# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import datetime, MySQLdb
import imutils
import cv2

#mysql connection
db = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd="root",
                      db="surveillance_db")
cur = db.cursor()

room_id = 1

def motion_detect():
    motion_camera_feed = cv2.VideoCapture(0)

    # initialize the first frame in the video stream
    firstFrame = None
    frame_count = 0

    # loop over the frames of the video
    while(motion_camera_feed.isOpened()):
        ret, frame = motion_camera_feed.read()
        frame_count += 1
        text = "Unoccupied"
        if motion_camera_feed is not None and frame_count % 10 ==0:
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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                insert_data = "INSERT INTO motion_entries(room_id,occupied_time) VALUES (" + str(room_id) + ",'" + str(datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p")) + "');"
                #print(insert_data)
                cur.execute(insert_data)

            # draw the text and timestamp on the frame
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # show the frame and record if the user presses a key
            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

    # cleanup the camera and close any open windows
    motion_camera_feed.release()
    cv2.destroyAllWindows()

motion_detect()