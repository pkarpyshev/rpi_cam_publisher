#!/usr/bin/env python

import sys
sys.path.append('/usr/lib/python2.7/dist-packages')

import rospy
import argparse

from cv_bridge import CvBridge

from time import time
from picamerathread import PiVideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray

from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from sensor_msgs.msg import Image

import os


class DatasetCollector:
    def __init__(self):
        self.rpi_num = os.environ['PI_NUMBER']
        self.framerate = int(os.environ['PI_CAM_FRAMERATE'])
        self.resolution = [int(i) for i in os.environ['PI_CAM_RESOLUTION'].split(',')]

        self.node = rospy.init_node('camera_{}'.format(self.rpi_num), anonymous=True)
        self.start_status = True
        self.timer = None

        self.bridge = CvBridge()
        self.time_publisher = rospy.Publisher('/cameras/time_{}'.format(self.rpi_num), Float32, queue_size=10)
        self.image_publisher = rospy.Publisher('/cameras/images_{}'.format(self.rpi_num), Image, queue_size=10)

        # rospy.Subscriber('/cameras/start_status', Bool, self.start_status_callback, queue_size=1)
        # rospy.Subscriber('/cameras/args', String, self.args_callback, queue_size=1)

        self.camera = PiCamera()
        self.camera.framerate = self.framerate
        self.camera.resolution =self.resolution
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.timer_status = False
        self.current_time = None
        self.run()

    # def start_status_callback(self, data):
    #     self.start_status = data.data

    # def args_callback(self, data):
    #     self.resolution = data.data

    def run(self):
        # self.start_status = True

        while not rospy.is_shutdown():
            for image in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                frame = image.array
                if self.start_status:

                    # if not self.timer_status:
                    #     self.start_timer()

                    self.image_publisher.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))
                    self.time_publisher.publish(time())

                self.rawCapture.truncate(0)

    # def start_timer(self):
    #     self.current_time = time()
    #     self.timer_status = True


if __name__ == '__main__':
    try:
        DatasetCollector(1)
    except rospy.ROSInterruptException:
        pass

    rospy.spin()
