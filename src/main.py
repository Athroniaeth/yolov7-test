# This is a sample Python script.
import shutil
from random import random, randint

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import glob, os


def video_to_frames():
    # Use a breakpoint in the code line below to debug your script.
    vidcap = cv2.VideoCapture('../data/video-train.mp4')
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    wanted_images = 125
    percentage = wanted_images / length

    if percentage > 1:
        raise Exception("La vidéo ne contient pas assez d'images pour avoir le nombre d'images voulu")

    success, image = vidcap.read()

    count = 2000
    while success:
        # Use a breakpoint in the code line below to debug your script.
        if random() < percentage:
            cv2.imwrite(f"../data/images/frame_{count}.jpg", image)  # save frame as JPEG file
            count += 1
        success, image = vidcap.read()


def delete_not_used_images():
    os.chdir("../data/")
    folder_images = glob.glob("images/*.jpg")
    folder_txt = glob.glob("labels/*.txt")

    name_folder_images = [i.split("\\")[1][:-4:] for i in folder_images]
    name_folder_txt = [i.split("\\")[1][:-4:] for i in folder_txt]
    del folder_txt[0]  # del file "classes"

    count = 2000
    for i in name_folder_images:
        if i not in name_folder_txt:
            if os.path.exists(f"../data/{folder_images[count]}"):
                print(folder_images[count])
                os.remove(f"../data/{folder_images[count]}")
        count += 1
    print(count)

def deplace_data():
    folder_images = glob.glob("../data/images/*.jpg")
    folder_txt = glob.glob("../data/labels/*.txt")

    name_folder_images = [i.split("\\")[1][:-4:] for i in folder_images]
    name_folder_txt = [i.split("\\")[1][:-4:] for i in folder_txt]
    del folder_txt[0]  # del file "classes"
    length = len(name_folder_txt)
    # DELETE ALL FILE IN YOLOV7 TRAIN / VAL FOLDER

    for f in glob.glob('../yolov7/data/train/images/*'): os.remove(f)
    for f in glob.glob('../yolov7/data/train/labels/*'): os.remove(f)
    for f in glob.glob('../yolov7/data/val/images/*'): os.remove(f)
    for f in glob.glob('../yolov7/data/val/labels/*'): os.remove(f)

    # DEPLACE ALL FILE IN PROJECT/DATA ON PROJECT/YOLOV7/DATA
    for i in range(length):
        print(folder_images[i], folder_txt[i])
        # folder_images = "images/frame_xxx.jpg", folder_txt = "labels/frame_xxx.txt"
        os.replace(f"../data/{folder_images[i]}", f"../yolov7/data/train/{folder_images[i]}")
        os.replace(f"../data/{folder_txt[i]}", f"../yolov7/data/train/{folder_txt[i]}")


    # percentage of images/labels for check training precision (other is for training)
    percentage = 5/100
    number = int(percentage * length)
    print(number)

    for i in range(number):
        rand = randint(0, length)
        print(folder_images[rand], folder_txt[rand])
        os.replace(f"../yolov7/data/train/{folder_images[rand]}", f"../yolov7/data/val/{folder_images[rand]}")
        os.replace(f"../yolov7/data/train/{folder_txt[rand]}", f"../yolov7/data/val/{folder_txt[rand]}")
        length -= 1

def complete_image():
    counter = 1
    path = r"../yolov7/data/train/images"
    for counter in range(1,2000):
        if not os.path.isfile(fr"{path}/frame_{counter}.jpg"):
            shutil.copy(fr"{path}/frame_0.jpg", fr"{path}/frame_{counter}.jpg")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    video_to_frames()
    # delete_not_used_images()
    # deplace_data()
    # complete_image()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
