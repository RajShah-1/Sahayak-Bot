/*
Author: eYRC_SB_363
*/

#include <object_recognition/main.hpp>

int main(int argc, char **argv)
{
    // ROS stuffs
    ros::init(argc, argv, "main_node");
    ros::NodeHandle node_handle;
    ros::Rate loop_rate(1);

    // Spin until arm is ready!


    Camera camera(node_handle);

    // Buffer so that we can receive callback messages
    // Ofcourse better ways would be there to do this
    ros::Duration(4).sleep();
    ros::spinOnce();
    camera.preprocess();
    camera.detect();
    

    return 0;
}
