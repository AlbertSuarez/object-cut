import torchvision
import torch
import os
import argparse 
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as T
from PIL import Image
from tqdm import tqdm

model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

#image_tensor = torchvision.transforms.functional.to_tensor(image)

#output = model([image_tensor])
#print(output)

def get_prediction(img_path, threshold):
  img = Image.open(img_path)
  transform = T.Compose([T.ToTensor()])
  img = transform(img)
  pred = model([img])
  pred_score = list(pred[0]['scores'].detach().numpy())
  pred_t = [pred_score.index(x) for x in pred_score if x>threshold][-1]
  masks = (pred[0]['masks']>0.5).squeeze().detach().cpu().numpy()
  pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
  pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
  masks = masks[:pred_t+1]
  pred_boxes = pred_boxes[:pred_t+1]
  pred_class = pred_class[:pred_t+1]
  return masks, pred_boxes, pred_class


def random_colour_masks(image):
  r = np.zeros_like(image).astype(np.uint8)
  g = np.zeros_like(image).astype(np.uint8)
  b = np.zeros_like(image).astype(np.uint8)
  r[image == 0], g[image == 0], b[image == 0] = [255,255,255]
  coloured_mask = np.stack([r, g, b], axis=2)
  return coloured_mask


def instance_segmentation_api(img_path, name, threshold=0.5, rect_th=3, text_size=3, text_th=3):
  masks, boxes, pred_cls = get_prediction(img_path, threshold)
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  label_classes = args.list.split(',')
  for i in range(len(masks)):
    if pred_cls[i] in label_classes:
        rgb_mask = random_colour_masks(masks[i])
        img = cv2.addWeighted(img, 1, rgb_mask, 1, 0)
        #cv2.rectangle(img, boxes[i][0], boxes[i][1],color=(0, 255, 0), thickness=rect_th)
        cv2.putText(img,pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,255,0),thickness=text_th)
  plt.figure(figsize=(20,30))
  plt.imshow(img)
  plt.savefig(os.path.join(args.output, name) + '.png')
  plt.show()

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, default="/home/gauss/Pictures/Wallpapers/wallpaper.jpg")
parser.add_argument('-l', '--list', help='Add a list of desired classes', type=str, default="person,cat")
#parser.add_argument('--image_path', type=str, default="/home/gauss/Pictures/Wallpapers")
parser.add_argument('--output', type=str, default="./output/")
args = parser.parse_args()

if __name__ == '__main__':
    #if args.image_path:
    #    images = [i for i in os.listdir(args.image_path)]
    #    print(images)
    #    for i in images:
    #        instance_segmentation_api(os.path.join(args.image_path,i),"output_masked_"+str(i))
    #else:
    instance_segmentation_api(args.image, "output_masked_")
