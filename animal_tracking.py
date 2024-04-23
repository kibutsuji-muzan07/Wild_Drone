import math
import cv2 # Import OpenCV Library
from ultralytics import YOLO
import cv2
import json
import numpy as np

def tone_mapping(frame):
  """
  Performs advanced tone mapping for glare reduction.

  Args:
      frame: The input frame in BGR color space.

  Returns:
      The tone-mapped frame in BGR color space.
  """

  # 1. Convert to HSV color space
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  # 2. Local Contrast Enhancement (Optional)
  # This step can be further optimized using CUDA for faster processing.
  # Here, we'll perform a basic bilateral filtering for illustration.
  value_channel = hsv_frame[:,:,2]  # Extract Value channel
  enhanced_value = cv2.bilateralFilter(value_channel, 9, 75, 75)  # Apply bilateral filtering
  hsv_frame[:,:,2] = enhanced_value  # Replace Value channel

  # 3. Calculate Luminance
  # We'll use a weighted sum of R, G, and B channels for luminance estimation
  luminance = 0.299 * gray_frame[:,:] + 0.587 * gray_frame[:,:] + 0.114 * gray_frame[:,:]

  # 4. Apply Histogram Equalization for global contrast enhancement
  luminance_uint8 = luminance.astype(np.uint8)
  luminance_eq = cv2.equalizeHist(luminance_uint8)

  # 5. Adaptive logarithmic mapping for local detail preservation
  # Here, 'q' is a user-defined parameter controlling the compression strength.
  q = 0.8  # Adjust 'q' between 0 and 1 for desired effect (lower = stronger compression)
  log_map = np.log1p(luminance_eq * 255.0) * q / 255.0

  # 6. Tone mapping using sigmoid function for smooth roll-off in highlights
  # 's' is another user-defined parameter controlling the roll-off steepness.
  s = 0.25  # Adjust 's' between 0 and 1 for desired effect (lower = sharper roll-off)
  sigmoid = 1 / (1 + np.exp(-s * (log_map - 0.5)))

  # 7. Remap luminance using the tone-mapped curve
  mapped_luminance = luminance * sigmoid

  # 8. Merge channels back to BGR color space
  hsv_frame[:,:,2] = mapped_luminance  # Replace Value channel with mapped luminance
  mapped_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)

  return mapped_frame

def is_glare_present(frame):
  """
  Checks for presence of glare in a frame using a simple thresholding approach.

  Args:
    frame: The input frame in BGR color space.

  Returns:
    True if glare is detected, False otherwise.
  """

  # Convert to HSV color space
  hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  # Extract Value channel
  value_channel = hsv_frame[:, :, 2]

  # Calculate average value
  avg_value = np.mean(value_channel)

  # Define glare threshold (adjust based on your video characteristics)
  glare_threshold = 220

  return avg_value > glare_threshold

def find_zebra(url):

    model = YOLO('yolov8n.pt')
    model.to('cuda') #uncomment if using CUDA
    # Check if CUDA (GPU) is available
    use_cuda = cv2.cuda.getCudaEnabledDeviceCount() > 0

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
    #drone_cam_buffer = bufferLessVideoCapture

    cap = cv2.VideoCapture(f"rtsp://aaa:aaa@{url}:8554/streaming/live/1") #uncomment if using CUDA
    #cap = cv2.VideoCapture(0) #for video camera testing
    if use_cuda:
        print("Using GPU for processing")
        cap = cv2.cudacodec.createVideoReader(str(cap))

    have_found_zebra = False

    while have_found_zebra == False:

        success, img = cap.read()

        if not success:
            print("failed")
            continue

        # Check for glare
        if is_glare_present(img):
            processed_frame = tone_mapping(img.copy())  # Apply tone mapping on a copy
        else:
            processed_frame = img

        results = model(processed_frame, stream=True)

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
        # if any(box.cls[0] == "zebra" for box in results.pandas().xyxy[0].to_pandas()):  # Check if any zebra is detected in the frame
        #     have_found_zebra = True

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

        #cap.release() #delete if using CUDA

    cap.release()
    cv2.destroyAllWindows()
    return info

def take_snapshot(url):
    cap1 = cv2.VideoCapture(f"rtsp://aaa:aaa@{url}:8554/streaming/live/1")
    success1,img1=cap1.read()
    if(success1==True):
        cv2.imwrite('zebra_photo_taken.png', img1)
        print("Snap Shotted!!")
        
    else:
        print("Did not latch onto video feed :(")
        
    cap1.release()



#find_zebra("192.168.1.5")
