#!/usr/bin/env python

import os
import json

info = {'year': 2018, 'version': '1.0'}
categories = [{'id': 1, 'name': 'pedestrian', 'supercategory': 'no'}]

def walk(root_dir):
    lst = []
    for parent, ddirnames, files in os.walk(root_dir):
        for f in files:
            lst.append(f)
    return lst

def construct_image_info(img_id, img_name, json_str):
    img_info = {}
    img_info['id'] = img_id
    img_info['width'] = int(json_str['imgWidth'])
    img_info['height'] = int(json_str['imgHeight'])
    img_info['file_name'] = img_name

    return img_info


def construct_annotations(box_id, image_id, json_str):
    annotations = []
    json_objects = json_str['objects']
    for i in range(len(json_objects)):
        instance = json_objects[i]
        instanceId = int(instance['instanceId'])
        if instanceId != 0:
            annt = {}
            bbox = instance['bbox']
            annt['id'] = box_id
            annt['image_id'] = image_id
            annt['category_id'] = 1
            annt['bbox'] = bbox
            annt['area'] = bbox[2] * bbox[3]
            annt['iscrowd'] = 0
            annotations.append(annt)
            box_id += 1
    return annotations

if __name__ == '__main__':
    annt_root = '/data/peng.wang/data/cityperson/annotations/val' # your own annt root
    img_root = '/data/peng.wang/data/cityperson/images/val' # your own img root
    files = walk(annt_root)

    box_id = 1
    image_id = 1
    success_count = 0
    failed_count = 0
    images_info = []
    annotations_info = []
    num_without_bbox = 0
    for annt in files:
        name, ext = os.path.splitext(annt)
        if ext == '.json':
            city, idx1, idx2, _ = name.split('_')
            image_name = city + '_' + idx1 + '_' + idx2 + '_leftImg8bit.png'
            if os.path.exists(img_root + '/' + city + '/' + image_name):
                success_count += 1
                annt_file = annt_root + '/' + city + '/' + annt
                with open(annt_file, 'r') as fd:
                    json_str = json.load(fd)
                    img_info = construct_image_info(image_id, image_name, json_str)
                    annotations = construct_annotations(box_id, image_id, json_str)
                    images_info.append(img_info)
                    if len(annotations) > 0:
                        annotations_info.extend(annotations)
                        box_id += len(annotations)
                    else:
                        num_without_bbox += 1
                    image_id += 1
            else:
                failed_count += 1
                print('%s is missing' % image_name)
        else:
            failed_count += 1
            print('%s is not a json file' % annt)
    coco_data = {}
    coco_data['info'] = info
    coco_data['images'] = images_info
    coco_data['annotations'] = annotations_info
    coco_data['categories'] = categories

    with open('cityperson_gt_val_coco.json', 'w') as fd:
        json.dump(coco_data, fd)

    print('success_count: ', success_count)
    print('failed_count: ', failed_count)
    print('total box: ', len(annotations_info))
    print('num_without_bbox: ', num_without_bbox)
    print('box_id: ', box_id)
