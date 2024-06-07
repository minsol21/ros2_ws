#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import csv
import os
from irobot_create_msgs.msg import IrIntensityVector

class SensorDataCollector(Node):
    def __init__(self):
        super().__init__('sensor_data_collector')
        self.subscription = self.create_subscription(
            IrIntensityVector,
            '/ir_intensity',
            self.listener_callback,
            10)
        self.data = []

    def listener_callback(self, msg):
        # Extract the 'value' from each reading in the readings array
        for reading in msg.readings:
            self.data.append(reading.value)
        self.get_logger().info(f'Received data: {[reading.value for reading in msg.readings]}')

        if len(self.data) >= 500:
            self.save_data()
            rclpy.shutdown()

    def save_data(self):
        home_dir = os.path.expanduser('~')
        data_dir = os.path.join(home_dir, 'ros2_ws', 'plots')
        
        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, 'ir_data.csv')
        
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IR_Intensity"])
            writer.writerows([[value] for value in self.data])
        self.get_logger().info(f"Data saved to {file_path}")

def main(args=None):
    rclpy.init(args=args)
    sensor_data_collector = SensorDataCollector()
    rclpy.spin(sensor_data_collector)
    sensor_data_collector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
