import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import yaml
from yaml.loader import SafeLoader
from math_code import *
from std_msgs.msg import String

class OdometrySubscriber(Node):
    def __init__(self):
        super().__init__('odometry_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            'odom',  # Replace with your topic name if different
            self.odom_callback,
            10  # QoS profile depth
        )

        self.publisher = self.create_publisher(
            String,
            'drone_location',  # Replace with the name of your output topic
            10  # QoS depth
        )
        self.get_logger().info('StringRelayNode has been started.')
        self.subscription  # prevent unused variable warning
        self.publisher

        with open('/home/ap/commander/construction_inspection/src/yaml_files/apartment_data.yaml', 'r') as f:
            self.yaml_data = list(yaml.load_all(f, Loader=SafeLoader))


    def odom_callback(self, msg):
        self.pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        )
        location = String()
        location.data = self.check_aparment()
        self.publisher.publish(location)
      
    def check_aparment(self):
        point = self.pose
        
        info = f"Location is {self.drone_location},\n"
        for i in self.yaml_data:
            Apartment = i["Apartment"]
            
            rectangle_center = (i["ApartmentSquare"]["rectangle_center"][0],i["ApartmentSquare"]["rectangle_center"][1])
            width = i["ApartmentSquare"]["width"]
            height = i["ApartmentSquare"]["height"]
            angle = i["ApartmentSquare"]["angle"]
            if is_point_inside_rotated_rectangle(point, rectangle_center, width, height, angle):
                house_center = rotate_vector_around_point((rectangle_center[0],rectangle_center[1]+round(height/3,2)),rectangle_center,angle)
                hallway_center = rotate_vector_around_point((rectangle_center[0],rectangle_center[1]-round(height/3,2)),rectangle_center,angle)
                if is_point_inside_rotated_rectangle(point, house_center, width, height/3, angle): self.drone_location = Apartment
                if is_point_inside_rotated_rectangle(point, hallway_center, width, height/3, angle): self.drone_location = "Hallway"

        return info
    
    
    

def main(args=None):
    print("Publishing location as apartments")
    rclpy.init(args=args)
    odometry_subscriber = OdometrySubscriber()
    odometry_subscriber.drone_location = "Hallway"

    try:
        rclpy.spin(odometry_subscriber)
    except KeyboardInterrupt:
        pass

    # Cleanup
    odometry_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


