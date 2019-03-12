from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 180
camera.resolution = (1920, 1080)
camera.framerate = 30
camera.start_preview()
sleep(30)
#camera.capture('snap.jpg')
print("Captured")
camera.stop_preview()
