#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os

# get the name of the file that we are executing
file_name = os.path.basename(__file__)
# check if the user has provided the correct number of arguments
if len(sys.argv) > 4 or len(sys.argv) < 3:
    print("[INFO] "+file_name+" | Usage: python3 "+file_name+" <bag_name> <topic_name> optional:<topic_type> \nThe file <bag_name> should be placed in the bags folder respectively. \nIt is not necessary to have 'bags/' in the beginning of the <bag_name>.\n <topic_type> is optional and can be found by executing: 'rosbag info <bag_name> -y -k topics'\n <topic_name> has a '/' in the beginning.")
    sys.exit(1)

bag_name = sys.argv[1]
if bag_name.startswith('bags/'):
    bag_name = bag_name.replace('bags/', '')

folder_name = bag_name.split('/')[0] +'/'+bag_name.split('/')[1]

topic_name = sys.argv[2]
topic_name_str = topic_name
if topic_name == 'gt':
    topic_name = '/ground_truth/odom'
elif topic_name == 'orb':
    topic_name = '/orb_slam3/camera_pose'

if len(sys.argv) == 4:
    topic_type = sys.argv[3]
else:
    output = os.popen('rosbag info bags/'+bag_name+' -y -k topics').read()
    # split the output. an entry begins with '-'
    output = output.split('-')
    # remove the first entry because it is empty
    output.pop(0)
    # search for the topic type in the output
    topic_type = ""
    for cell in output:
        # get the word between "topic:" and "\n"
        candiate = cell.split('topic: ')[1].split('\n')[0]
        # compare the candidate with the topic_name
        if candiate == topic_name:
            # print("[INFO] "+file_name+" | found topic name in bag info: " + topic_name)
            # get the word between "type:" and "\n"
            topic_type = cell.split('type: ')[1].split('\n')[0]
            # print("[INFO] "+file_name+" | found topic type: " + topic_type)

    if topic_type == "":
        print("[INFO] "+file_name+" | The topic type could not be resolved from the topic name: " + topic_name + " and the bag: " + bag_name + ".\nPlease provide the topic type as the third argument. f.e. nav_msgs/Odometry")
        sys.exit(1)


# make csv_file the combination of first and second
csv_file = bag_name.split('/')[2].split('.')[0] + '-' + topic_name_str
csv_file = "csv/" + folder_name +'/'+ csv_file + '.csv'

if not os.path.exists("csv/" + folder_name):
    os.makedirs("csv/" + folder_name)
    print("[INFO] "+file_name+" | created folder: " + "csv/" + folder_name)

command = 'rostopic echo -b bags/'+bag_name+' -p '+topic_name+' > '+csv_file
os.system(command)
print("[INFO] "+file_name+" | executing: " + command)

df = pd.read_csv(csv_file)

# define function to replace the following part
if (topic_type == "nav_msgs/Odometry"):
    df = df[df.columns.drop(list(df.filter(regex='twist')))]
    df = df[df.columns.drop(list(df.filter(regex='covariance')))]
    df = df[df.columns.drop(list(df.filter(regex='orientation')))]
    df = df[df.columns.drop(list(df.filter(regex='frame_id')))]
    df.columns = df.columns.str.replace('field.', '')
    df.columns = df.columns.str.replace('pose.', '')
    df.columns = df.columns.str.replace('position.', '')
    df.columns = df.columns.str.replace('%', '')
    df.columns = df.columns.str.replace('header.', '')

elif (topic_type == "geometry_msgs/PoseStamped"):
    # drop the all columns with twist in the name
    df = df[df.columns.drop(list(df.filter(regex='twist')))]
    df = df[df.columns.drop(list(df.filter(regex='covariance')))]
    df = df[df.columns.drop(list(df.filter(regex='orientation')))]
    df = df[df.columns.drop(list(df.filter(regex='frame_id')))]
    # remove the "field." from the column names
    df.columns = df.columns.str.replace('field.', '')
    df.columns = df.columns.str.replace('pose.', '')
    df.columns = df.columns.str.replace('position.', '')
    df.columns = df.columns.str.replace('%', '')
    df.columns = df.columns.str.replace('header.', '')

df.to_csv(csv_file, index=False)
# print("[INFO] "+file_name+" | saved to: " + csv_file)