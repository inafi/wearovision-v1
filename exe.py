import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import subprocess
import time
import sys
sys.path.append("/usr/local/lib/python3.7/site-packages")
from gtts import gTTS 
import inflect
import re
import ast
from PIL import Image

#Automatically changes directory in path 
cpath=os.path.abspath(os.path.dirname(__file__) ) # +/gsf
os.chdir(cpath)

#Return array with filtered accuracy
def filter_acc(l, acc):
    indexes = []
    for i in range(0, len(l)):
        if l[i][1] < acc:
            indexes.append(i)
    l = [i for j, i in enumerate(l) if j not in indexes]
    return l

#Pluralizes and return something like this [['books', 7], ['backpack', 1]] 
def get_l(l):
    out = []
    final = []
    p = inflect.engine()
    for i in range(len(l)):
        out.append(l[i][0])
    d = {x:out.count(x) for x in out}
    for x in d:
        if d[x] != 1:
            final.append([(p.plural(x)).replace(":", ""), d[x]])
        else:
            final.append([x.replace(":", ""), d[x]])
    return final

#Get's the average accuracy of all the classifications
def getavg(arg):
    sum = 0
    if len(arg) != 0:
        for i in range(len(arg)):
            sum += arg[i][1]
        return sum/len(arg)
    else:
        return -1

#Runs command and filters through terminal outputs
def run(img_path, acc, yolo):
    outputs = []
    classes = []
    if yolo == 3:
        command = ["./runv3-d detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights " + img_path]
    elif yolo == 9000:
        command = ["./run9000-d detector test cfg/combine9k.data cfg/yolo3-9000.cfg yolo9000.weights " + img_path]
    p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    classes = text.split("\n")
    classes_out = []
    boxes = []
    if classes[0] != "":
        del classes[0], classes[-1]
        count = 0
        for i in range(len(classes)):
            if(count%2 == 0):
                outputs.append([classes[i].split(": ")[0], int(classes[i].split(": ")[1].strip("%"))])
                classes_out.append(classes[i])
            else:
                s2 = classes[i].strip('Bounding Box: ')
                s2 = re.sub('[LTRBeftopighm=,]', '', s2).split(" ")
                boxes.append(s2)
            count = count+1
        save = outputs
        #Average the classes confidence so blank array doesn't get through
        outputs = filter_acc(outputs, acc)
        if outputs == [] and getavg(save) != -1:
            outputs = filter_acc(save, getavg(save))
        final = get_l(outputs)
        return final, classes_out, text.split(" ")[3], save, boxes
    else: 
        return -1, -1, -1

#Sorts through the final outputs of the runs of v3 and 9000 giving the truly final output
#All the inputs are arrays
#Returns array
def sort(v3, v9000, v9000c):
    sorted, d3, d9000 = ({} for i in range(3))
    d3o = 0
    d9000o = 0
    out = []
    for i in range(len(v3)): 
        sorted[v3[i][0]] = v3[i][1]
        d3[v3[i][0]] = v3[i][1]
        d3o += v3[i][1]
    for i in range(len(v9000)): 
        d9000[v9000[i][0]] = v9000[i][1]
        d9000o += v9000[i][1]
    if d9000o > d3o:
        for labels in d9000:
            if labels not in d3:
                sorted[labels] = d9000[labels]
            elif labels in d3 and d3[labels] < d9000[labels]:
                sorted[labels] = d9000[labels]
    else:
        outputs = []
        print(outputs)
        fd = {}
        for i in range(len(v9000c)):
            outputs.append([v9000c[i].split(": ")[0], int(v9000c[i].split(": ")[1].strip("%"))])
        outputs = filter_acc(outputs, 90)
        for i in range(len(outputs)): 
            fd[outputs[i][0]] = outputs[i][1]
        for labels in fd:
            if labels not in d3:
                sorted[labels] = fd[labels]
            elif labels in d3 and d3[labels] < fd[labels]:
                sorted[labels] = fd[labels]
    for i in sorted:
        out.append([sorted[i], i])
    return out

#plt plots figures - 9000 is png and v3 is jpg
def show_img():
    f1 = plt.figure(1)
    path=os.path.join(cpath, "predictions.jpg")
    img=mpimg.imread(path)
    imgplot=plt.imshow(img)
 
    f2 = plt.figure(2)
    path2=os.path.join(cpath, "predictions.png")
    img2=mpimg.imread(path2)
    imgplot=plt.imshow(img2)
    plt.show()

#Runs everything and assume jpg input - jpegs must be in /data
def get_output(img):
    imgl = "data/" + img + ".jpg"
    #Accuracy filters of v3 and 9000
    y3f, y3c, y3t, labs, boxes = run(imgl, 80, 3)
    fil = open("box_dimension.txt", "w")
    fil.write(str(labs)+ "\n")
    fil.write(str(boxes) + "\n")
    y9000f, y9000c, y9000t, labs, boxes = run(imgl, 50, 9000)
    fil.write(str(labs)+ "\n")
    fil.write(str(boxes))
    fil.close()
    if y3f != -1:
        print(y9000t, "\n", y9000c, "\n", y9000f, "\n")
        print(y3t, "\n", y3c, "\n", y3f, "\n")
        s = sort(y3f, y9000f, y9000c)
        print(s)
        audio = ""
        #Convert the array to a string - the commas add a slight pause
        for i in range(len(s)):
            audio += str(s[i][0]) + " " + s[i][1] + ", "
        #show_img()
        language = 'en'
        myobj = gTTS(text=audio, lang=language, slow=False) 
        myobj.save("objects.mp3") 
        os.system("afplay objects.mp3") 
    else:
        print("Unable to Classify")

def get_dist(ob, freedom):
    fil = open("box_dimension.txt", "r")
    inputs = fil.readlines()
    labs = []
    boxes = []
    labs = ast.literal_eval(inputs[0])
    labs.append(ast.literal_eval(inputs[2])[0])
    boxes = ast.literal_eval(inputs[1])
    boxes.append(ast.literal_eval(inputs[3])[0])

    place = -1
    for i in range(len(labs)):
        if(ob == labs[i][0]):
            place = i
            print(place)
    if(place == -1 ):
        return("Object is not there.")

    box = boxes[place]
    for i in range(len(box)):
        box[i] = int(box[i])

    imgl = "predictions.jpg"
    pic = Image.open(imgl)
    width, height = pic.size
    free = width * freedom
    img_center = [width/2, height/2]
    pic_center = [int((box[0]+box[2])/2), int((box[1]+box[3])/2)]
    result = -1
    
    if(
        img_center[0] >= pic_center[0]-free and img_center[0] <= pic_center[0] + free and img_center[1] >= pic_center[0] - free and img_center[1] <= pic_center[1]
    ):
        result = 0
    else:
        result = [pic_center[0]-img_center[0], pic_center[1]-img_center[1]]
    print('')
    return(result)

#Must be jpg 

print(get_dist('motorcyclist', .25))