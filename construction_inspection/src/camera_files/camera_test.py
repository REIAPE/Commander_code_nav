

import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 
from ultralytics import YOLO
from nav_msgs.msg import Odometry


from math_code import *
from open_yaml import *
    
class SimpleSub(Node):
    def __init__(self):
        super().__init__('camera_and_pose_sub')
        self.yolo = YOLO('yolov8s.pt')
        topic_name= '/camera/image_raw'

        self.publisher_ = self.create_publisher(Image, topic_name , 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()

        self.subscription = self.create_subscription(Image, topic_name, self.img_callback, 10)
        self.subscription 
        self.br = CvBridge()

        self.odomsubscription = self.create_subscription(Odometry,'odom', self.odom_callback,10 )
        self.odomsubscription  

        self.data_dict = {} #Here we save detected objects. 

        self.cordinate_list = get_cordinate_list()
        #self.location = self.check_aparment()

    def detection_callback(self, frame):
        results = self.yolo.track(frame, stream=True)

        for result in results:
            # get the classes names
            classes_names = result.names
            
            # iterate over each box
            for box in result.boxes:
                # check if confidence is greater than 60 percent
                if box.conf[0] > 0.6:
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
                    self.save_data(class_name)
        return frame

    def odom_callback(self, msg):
        self.pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        )


    def check_aparment(self):

        point = self.pose

        print(point)
        for apartment in self.cordinate_list:
            for rectangle in self.cordinate_list[apartment]:
                if point_inside_rectangle(rectangle,point): self.location = apartment
        
    
    def save_data(self, names):
        #Save object and location to dict. So we can add location data for object.
        
        if self.check_aparment() not in self.data_dict:
            if names not in self.data_dict[self.location]:
                self.data_dict[self.location] = names
        
    def getColours(cls_num):
        base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def timer_callback(self):
        ret, frame = self.cap.read()     
        if ret == True:
            self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
        self.get_logger().info('Publishing video frame')
        self.check_aparment()
        self.get_logger().info(self.location)


    def img_callback(self, data):
        self.get_logger().info('Receiving video frame')
        current_frame = self.br.imgmsg_to_cv2(data)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)

        current_frame = self.detection_callback(current_frame)
        cv2.imshow("camera", current_frame)   
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    simple_sub = SimpleSub()
    SimpleSub.location = "Hallway"
    try:
        rclpy.spin(simple_sub)
    except KeyboardInterrupt:
        pass
    finally:
        # Print the final state of data_dict
        print()
        print(simple_sub.data_dict)
        
        # Clean up resources
        simple_sub.destroy_node()
        
  
if __name__ == '__main__':
  main()
  print("Node shutdown cleanly")