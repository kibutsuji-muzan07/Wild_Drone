
# Adapted from : https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv

import cv2
import threading
import time

# bufferless VideoCapture
class BufferLessVideoCapture:
	def __init__(self, IP_RC):
		source = f"rtsp://aaa:aaa@{IP_RC}:8554/streaming/live/1"
		self.cap = cv2.VideoCapture(source)
		self.lock = threading.Lock()
		self.t = threading.Thread(target=self._reader)
		self.t.daemon = True
		self.t.start()

	# grab frames as soon as they are available
	def _reader(self):
		while True:
			with self.lock:
				ret = self.cap.grab()
			if not ret:
				break

	# retrieve latest frame
	def read(self):
		with self.lock:
			_, frame = self.cap.retrieve()
		return frame
