import io
import time

import picamera
import requests
import RPi.GPIO as GPIO

GPIO_TRIGGER = 18
GPIO_ECHO = 24
GREEN_LED_PIN = 17
RED_LED_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)


def measure_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


def capture_image():
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        camera.capture(stream, format='jpeg')
    stream.seek(0)
    return stream


def send_attendance_request(stream):
    response = requests.post(
        'http://10.0.52.207:5000/attendance', files={'file': stream})
    return response
