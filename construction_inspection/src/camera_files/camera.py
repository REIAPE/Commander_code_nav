
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import cv2
from roboflow import Roboflow

from open_yaml import *
from math_code import *
from data_handeler import *

class RoboflowROS2Detector(Node):
    def __init__(self):
        super().__init__('roboflow_ros2_detector')

        self.odomsubscription = self.create_subscription(Odometry,'odom', self.odom_callback,10 )
        self.odomsubscription
        self.pose = None
        self.location = None

        self.subscription = self.create_subscription(Image,'/camera/image_raw', self.image_callback, qos_profile=rclpy.qos.QoSPresetProfiles.SYSTEM_DEFAULT.value)

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.bridge = CvBridge()

        
        # Initialize Roboflow
        rf = Roboflow(api_key="j1NYSJsR06G2mkXfcsKL")
        project = rf.workspace().project("specific-gazebo-models")
        self.model = project.version("3").model
        
        self.cordinate_list = get_cordinate_list()
        self.data_dict = {}

        self.get_logger().info("Roboflow ROS2 Detector Node has been started.")

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # Preprocess image if necessary (e.g., resizing)
        #resized_image = cv2.resize(cv_image, (416, 416))  # Adjust size as needed
        
        # Inference using Roboflow
        response = self.model.predict(cv_image, confidence=40, overlap=30).json()
        detections = response['predictions']
        
        # Scale factor if resizing was performed
        height_ratio = cv_image.shape[0] / cv_image.shape[0]
        width_ratio = cv_image.shape[1] / cv_image.shape[1]
        
        # Draw bounding boxes on the image
        name_list = {}
        for detection in detections:

            confidence = detection['confidence']
            if confidence > 0.5:
                # Scale predictions back to original image dimensions
                center_x = detection['x'] * width_ratio
                center_y = detection['y'] * height_ratio
                width = detection['width'] * width_ratio
                height = detection['height'] * height_ratio
                
                # Calculate top-left and bottom-right corners
                x1 = int(center_x - width / 2)
                y1 = int(center_y - height / 2)
                x2 = int(center_x + width / 2)
                y2 = int(center_y + height / 2)
                
                label = detection['class']
                rectangle = (x1,y1,x2,y2)
                
                # Draw rectangle and label
                cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(cv_image, f"{label}: {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                name_list[label] = rectangle

        #Saves object information if location is known.  
        if self.location !=None:
            self.save_data(name_list)

        cv2.imshow("Detection", cv_image)
        cv2.waitKey(1)
    
    def save_data(self, objects):
        
        
        self.data_dict = update_dictionary(objects=objects, location=self.location, data_dict=self.data_dict)
        print("dict tulostus")
        print(self.data_dict)

    def odom_callback(self, msg):
        self.pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        )

    def check_aparment(self):

        point = self.pose
        if point != None:
            for apartment in self.cordinate_list:
                for rectangle in self.cordinate_list[apartment]:
                    if point_inside_rectangle(rectangle,point): self.location = apartment
    
    def timer_callback(self):
        self.get_logger().info('Publishing video frame')
        self.check_aparment()
        self.get_logger().info(self.location)

def main(args=None):
    rclpy.init(args=args)
    node = RoboflowROS2Detector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("___Shutting down Roboflow ROS2 Detector Node.___")
    finally:
        print_data(node.data_dict)
        
        node.destroy_node()

if __name__ == '__main__':
    main()
    print("___Node shutdown cleanly___")
