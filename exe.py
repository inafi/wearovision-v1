import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import subprocess
import inflect

#Automatically changes directory in path 
cpath=os.path.abspath(os.path.dirname(__file__)) 
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
        command = ["./runv3 detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights " + img_path]
    elif yolo == 9000:
        command = ["./run9000 detector test cfg/combine9k.data cfg/yolo3-9000.cfg yolo9000.weights " + img_path]
    p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    classes = text.split("\n")
    if classes[0] != "":
        del classes[0], classes[-1]
        for i in range(len(classes)):
            outputs.append([classes[i].split(": ")[0], int(classes[i].split(": ")[1].strip("%"))])
        save = outputs
        #Average the classes confidence so blank array doesn't get through
        outputs = filter_acc(outputs, acc)
        if outputs == [] and getavg(save) != -1:
            outputs = filter_acc(save, getavg(save))
        final = get_l(outputs)
        return final, classes, text.split(" ")[3]
    else: 
        return -1, -1, -1

#Sorts through the final outputs of the runs of v3 and 9000 giving the truly final output
#All the inputs are arrays
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
    y3f, y3c, y3t = run(imgl, 80, 3)
    y9000f, y9000c, y9000t = run(imgl, 50, 9000)
    if y3f != -1:
        print(y9000t, "\n", y9000c, "\n", y9000f, "\n")
        print(y3t, "\n", y3c, "\n", y3f, "\n")
        s = sort(y3f, y9000f, y9000c)
        print(s)
        show_img()
    else:
        print("Unable to Classify")

#Must be jpg 
get_output("stuff2")
