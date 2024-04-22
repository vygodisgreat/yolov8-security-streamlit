import os
import cv2
import streamlit as st
from ultralytics import YOLO
import supervision as sv
import st_pages
# dependencies

model_path = 'yolov8sbest.pt'
# the path of your YOLO model goes here

cams = 0
# the number of cams

# counts the number of cameras connected to the system using some estimate 'n' by trying to open cameras
for i in range(10):
    cam = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cam.isOpened():
        cams += 1
        cam.release()
    else:
        break

root_dir = os.getcwd()
# the root directory for use

# creating captures directory
cap_dir = f"{root_dir}\\CAPTURES"
try:
    os.mkdir(cap_dir)
except:
    pass

# create the image directories corresponding to each camera
for i in range(cams):
    try:
        cam_dir = f"{cap_dir}\\CAMERA{i+1}"
        os.mkdir(cam_dir)
    except:
        pass

# some front end beautification, not much!
st.title("Security Surviellence")
st.subheader("automatically capture real time footage from all connected cameras to the system and monitor them for threats and such.")
st.sidebar.text(f"available cameras in the system: {cams}")

st.sidebar.write("---")
st.sidebar.info("to access the security footage, click on the corresponding icons in the upper part of the sidebar.")
st.sidebar.write("---")

page_list = [st_pages.Page("app.py", "HomePage", "👁️")]
# inital page list for sidebar
pages_from_cams = [st_pages.Page(f"{root_dir}\\pages\\camera{i}.py", f"Camera Feed {i+1}", "📹", in_section=True) for i in range(cams)]
# wot da fuck?? emojis in strings?? man UTF rocks
page_list.extend(pages_from_cams)
# yea extended the page list!

st_pages.show_pages(page_list)
# this should work?

num = 0
for i in range(cams):
    files = os.listdir(f"{cap_dir}\\CAMERA{i+1}")
    num += len(files)
# counts number of images

st.metric(label="captured instances", value=num, delta=num, delta_color='inverse')