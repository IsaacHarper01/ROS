#!/usr/bin/env python
import rospy
import pyttsx3
from std_msgs.msg import String

class speaker_ros:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices') 
        self.engine.setProperty('voice', voices[2].id)
        self.engine.setProperty('rate', 150)
        self.sub = rospy.Subscriber("/speak", String, self.speakcall)

    def speakcall(self, text):
        self.engine.say(text.data)
        self.engine.runAndWait()
        self.engine.stop()

rospy.init_node("speaker_node")
speaker = speaker_ros()
rospy.spin()