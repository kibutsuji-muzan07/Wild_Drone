import math
import cv2 # Import OpenCV Library
from ultralytics import YOLO
import cv2
import json

def find_zebra():

    model = YOLO('yolov8n.pt')
    model.to('cuda') #uncomment if using CUDA

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
                ]

    #cap = cv2.VideoCapture("rtsp://aaa:aaa@192.168.1.4:8554/streaming/live/1") #uncomment if using CUDA
    cap = cv2.VideoCapture(0) #for video camera testing

    have_found_zebra = False

    while have_found_zebra == False:

        #cap = cv2.VideoCapture("rtsp://aaa:aaa@192.168.1.4:8554/streaming/live/1") #delete if using CUDA
        success, img = cap.read()

        if not success:
            print("failed")
            continue

        results = model(img, stream=True)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:

                confidence = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])

                if confidence > 0.6 and classNames[cls] == "zebra":

                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # confidence
                    confidence = math.ceil((box.conf[0]*100))/100
                    #print("Confidence --->",confidence)

                    # class name
                    cls = int(box.cls[0])
                    #print("Class name -->", classNames[cls])

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, classNames[cls] + " " + str(confidence), org, font, fontScale, color, thickness)

                    info = { 'xres' : img.shape[1], 'yres' : img.shape[0], 'x1' : x1, 'x2' : x2, 'y1' : y1, 'y2' : y2 }

                    with open('my_dict.json', 'w') as f:
                        json.dump(info, f)

                    have_found_zebra = True

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

        #cap.release() #delete if using CUDA

    cap.release()
    cv2.destroyAllWindows()
    return info
    

#find_zebra()
