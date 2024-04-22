import cv2
import os
import datetime
import streamlit as st
import supervision as sv
from ultralytics import YOLO

model_path = "yolov8sbest.pt"
# path of the model
pwd = os.getcwd()

def process(id):
    
    cam = cv2.VideoCapture(id, cv2.CAP_DSHOW)
    # created the camera object
    model = YOLO(model_path)
    # created the yolo model
    
    ctr, rst = 0, False
    # flags for the correct annotated frame display
    # if ct>10 then we display as less chancd of false positives
    # if any frame has no gun with high confidence then we use rst to reset
    an1 = sv.BoundingBoxAnnotator()
    an2 = sv.LabelAnnotator()
    # labelling annotators for labelling of images that run inference
    win = st.image([])
    # window to display the camera footage in the applciation
    images_directory = f"CAPTURES\\CAMERA{id+1}\\"

    warning = st.empty()
    def reset():
        warning.write()
        cam.release()
    st.button("reset alerts", on_click=reset)
    
    st.subheader(f"this is camera {id+1}")

    try:
        while (True):
            # loop goes till user ezits the system?
            
            flag, frame = cam.read()
            if (not flag):
                print(f"CAMERA {id} NOT WORKING!")
                continue
            # try to read camera feed and store frames
            
            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            # detections on the frame to be used!
            
            if not detections.confidence.size:
                win.image(frame)
                continue
                
            rst = False
            
            for val in detections.confidence:
                if (val>0.4):
                    ctr += 1
                    rst = True
                    break
            
            if (not rst):
                ctr = 0
            if (ctr<5):
                win.image(frame)
                continue
            
            alert = True
            
            # labels = [f"{model.model.names[class_id]} {confidence:.2f}" for class_id, confidence in zip(detections.class_id, detections.confidence)]
            
            labels = [f"{model.model.names[class_id]} {confidence:.2f}" for class_id, confidence in zip(detections.class_id, detections.confidence)]
            annotated_image = an1.annotate(scene=frame, detections=detections)
            annotated_image = an2.annotate(scene=annotated_image, detections=detections, labels=labels)
            
            # # Filter detections and labels with confidence > 0.6
            # filtered_detections = [detection for detection in detections if detection.confidence > 0.6]
            # filtered_labels = [f"{model.model.names[detection.class_id]} {detection.confidence:.2f}" for detection in filtered_detections]

            # # Annotate image with filtered labels
            # annotated_image = an1.annotate(scene=frame, detections=detections)
            # annotated_image = an2.annotate(scene=annotated_image, detections=filtered_detections, labels=filtered_labels)

            
            win.image(annotated_image)
            
            # save every 10th correct frame!
            if (ctr%10==0):
                ts = datetime.datetime.now()
                ts = ts.strftime("_%Y-%m-%d_%H-%M-%S")
                filepath = images_directory + ts + ".png"
                # creating the string timestamp for saving images
                cv2.imwrite(filepath, annotated_image)
                
                warning.error("ALERT! SUSPICIOUS ACTIVITY! CHECK LOGS!")  
                
                    
    finally:
        cam.release()