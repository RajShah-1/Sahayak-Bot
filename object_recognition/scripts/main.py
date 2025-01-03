#! /usr/bin/env python
import rospy
from manipulator import Manipulator
from pose_settings import PoseSettings
from object_recognition.msg import ObjectPose
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped


object_centroids = {}


def detection_info_callback(data):
    object_centroids[data.name] = data.pose


def main():

    # Initialise node
    node_name = 'sara'  # Super Automatic Robot Arm
    rospy.init_node(node_name, anonymous=True)
    detect_pub = rospy.Publisher('detect', Bool, queue_size=10)
    sara = Manipulator()
    # print("\n\n\n")
    # print(sara.scene.get_known_object_names())
    # print("\n\n\n")    
    capture_pose = [0.12965710797413593, -0.2558361846975669, -
                    0.4842167126928663, -1.525936090630152, 5.7309490891563115, 1.807201005762695]
    sara.set_joint_angles(capture_pose)

    # Signal object_recognition node to start the work
    detect_pub.publish(True)
    
    # Wait for the object_detection node to publish the data
    rospy.Subscriber('detection_info', ObjectPose, detection_info_callback)
    while len(object_centroids.keys()) < 3:
        rospy.sleep(0.5)

    print(object_centroids)
    add_objects(sara.scene)
    settings = PoseSettings(object_centroids)

    # print("\n\n\n")
    # print(sara.scene.get_known_object_names())
    # print("\n\n\n") 

    sara.pick(settings.coke)
    rospy.sleep(1.0)
    sara.place(settings.coke)
    rospy.sleep(1.0)


def add_objects(scene):
    """
    Add objects to the scene
    """
    pose = PoseStamped()

    pose.pose = object_centroids["Coke Can"].pose
    pose.pose.position.z = 0.279
    pose.pose.orientation.w = 0
    pose.header.frame_id = "base_link"
    scene.add_box(
        name="Coke Can",
        pose=pose,
        size=(0.01, 0.01, 0.05)
    )

    pose.pose = object_centroids["Battery"].pose
    pose.pose.position.z = 0.269
    pose.pose.orientation.w = 0
    pose.header.frame_id = "base_link"
    scene.add_box(
        name="Battery",
        pose=pose,
        size=(0.01, 0.01, 0.05)
    )

    pose.pose = object_centroids["Glue"].pose
    pose.pose.position.z = 0.279
    pose.pose.orientation.w = 0
    pose.header.frame_id = "base_link"
    scene.add_box(
        name="Glue",
        pose=pose,
        size=(0.01, 0.01, 0.05)
    )


if __name__ == '__main__':
    main()
