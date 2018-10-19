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

def construct_image_info(img_id, img_name, img_shape):
    img_info = {}
    img_info['id'] = img_id
    img_info['width'] = img_shape[0]
    img_info['height'] = img_shape[1]
    img_info['file_name'] = img_name

    return img_info


def construct_annotations(box_id, image_id, boxes_str):
    annotations = []
    boxes = boxes_str.split('-')
    for box in boxes:
        bx = [int(v) for v in box[1:-1].split(',')]
        annt = {}
        bbox = [bx[0], bx[1], bx[2] - bx[0], bx[3] - bx[1]]
        annt['id'] = box_id
        annt['image_id'] = image_id
        annt['category_id'] = 1
        annt['bbox'] = bbox
        annt['iscrowd'] = 0
        annt['area'] = bbox[2] * bbox[3]
        annotations.append(annt)
        box_id += 1
    return annotations

if __name__ == '__main__':
    root_dir = '/Users/wangpeng/Work/rongyi/opensource/data/PennFudanPed' # you shold update this root dir
    annt_dir = root_dir + '/Annotation' # you shold update
    files = walk(annt_dir)

    box_id = 1
    image_id = 1
    success_count = 0
    failed_count = 0
    images_info = []
    annotations_info = []
    for annt in files:
        name, ext = os.path.splitext(annt)
        if ext == '.txt':
            with open(annt_dir + '/' + annt, 'r') as fd:
                lines = fd.readlines()
                img_name = lines[0].strip().split(':')[1]
                img_shape = [int(v) for v in (lines[1].strip().split(':')[1]).split('x')]
                boxes_str = lines[2].strip().split(':')[1]
                if os.path.exists(root_dir + '/' + img_name):
                    success_count += 1
                    img_info = construct_image_info(image_id, img_name, img_shape)
                    annotations = construct_annotations(box_id, image_id, boxes_str)
                    images_info.append(img_info)
                    if len(annotations) > 0:
                        annotations_info.extend(annotations)
                        box_id += len(annotations)
                    image_id += 1
                else:
                    failed_count += 1
                    print('%s is missing' % img_name)
        else:
            failed_count += 1
            print('%s is not a .txt file' % annt)
    coco_data = {}
    coco_data['info'] = info
    coco_data['images'] = images_info
    coco_data['annotations'] = annotations_info
    coco_data['categories'] = categories

    with open('penn_fudan_gt_coco.json', 'w') as fd:
        json.dump(coco_data, fd)

    print('success_count: ', success_count)
    print('failed_count: ', failed_count)
    print('box_id: ', box_id)
