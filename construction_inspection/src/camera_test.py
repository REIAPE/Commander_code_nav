#! /usr/bin/env python3

import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 

from ultralytics import YOLO
    
class SimplePubSub(Node):
    def __init__(self):
        super().__init__('simple_pub_sub')
        self.yolo = YOLO('yolov8s.pt')
        topic_name= '/camera/image_raw'

        self.publisher_ = self.create_publisher(Image, topic_name , 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()

        self.subscription = self.create_subscription(Image, topic_name, self.img_callback, 10)
        self.subscription 
        self.br = CvBridge()

    def detection_callback(self, frame):
        results = self.yolo.track(frame, stream=True)

        for result in results:
            # get the classes names
            classes_names = result.names

            # iterate over each box
            for box in result.boxes:
                # check if confidence is greater than 40 percent
                if box.conf[0] > 0.4:
                    # get coordinates
                    [x1, y1, x2, y2] = box.xyxy[0]
                    # convert to int
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # get the class
                    cls = int(box.cls[0])

                    # get the class name
                    class_name = classes_names[cls]

                    # get the respective colour
                    colour = (255, 0, 0)

                    # draw the rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                    # put the class name and confidence on the image
                    cv2.putText(frame, f'{class_name} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
        return frame

    def getColours(cls_num):
        base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def timer_callback(self):
        ret, frame = self.cap.read()     
        if ret == True:
            self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
        self.get_logger().info('Publishing video frame')


    def img_callback(self, data):
        self.get_logger().info('Receiving video frame')
        current_frame = self.br.imgmsg_to_cv2(data)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)

        current_frame = self.detection_callback(current_frame)
        cv2.imshow("camera", current_frame)   
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    simple_pub_sub = SimplePubSub()
    rclpy.spin(simple_pub_sub)
    simple_pub_sub.destroy_node()
    rclpy.shutdown()

  
if __name__ == '__main__':
  main()