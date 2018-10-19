#!/usr/bin/env python
#this copy from https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoEvalDemo.ipynb

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

annType = 'bbox'      #specify type here

#initialize COCO ground truth api
annFile = 'penn_fudan_gt_coco.json'

# initialize COCO detections api
resFile = 'coco_dt_result.json'

cocoGt=COCO(annFile)
cocoDt = cocoGt.loadRes(resFile)

cocoEval = COCOeval(cocoGt, cocoDt, annType)
cocoEval.params.useCats = 0
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()
