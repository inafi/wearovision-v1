from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()


detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "/Users/nafi/Develop/GitHub/GSF/yolo.h5"))
detector.loadModel()
name = "stuff"
choosefile = name + ".jpg"
newfile = "imageai" + ".jpg"
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , choosefile), output_image_path=os.path.join(execution_path , newfile), minimum_percentage_probability=30)

''' custom
custom_objects = detector.CustomObjects(person=True)
detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path , choosefile), output_image_path=os.path.join(execution_path , newfile), minimum_percentage_probability=10)
'''

for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")
