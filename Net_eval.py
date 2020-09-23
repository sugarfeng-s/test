import torch
import torch.nn.functional as F
from Net_design import Net_design
from utils.dataset import valSampler
from torch.utils.data import DataLoader, random_split
import os
import cv2
import numpy as np
from sklearn.metrics import roc_auc_score,accuracy_score,jaccard_similarity_score
from sklearn import metrics
from dice_loss import Dice_coeff
class Net_eval(object):
    def __init__(self,used_model_list,evaluate_method,weight_name,data_path,save_dir):
        self.evaluate_method = evaluate_method
        self.weight_name = weight_name
        self.data_path = data_path
        self.save_dir = save_dir
        self.used_model_list = used_model_list
    def eval(self):
        device = torch.cuda.current_device()
        model = Net_design(self.used_model_list)
        model.eval()
        model.load_state_dict(torch.load(self.weight_name))
        dataset = valSampler(self.data_path)
        loader = DataLoader(dataset, batch_size=1,
                            shuffle=False, num_workers=2, pin_memory=True)
        for batch in loader:
            imgs = batch['image']
            true_masks = batch['mask']
            imgs = imgs.to(device=device, dtype=torch.float32)
            true_masks = true_masks.to(device = device, dtype = torch.float32)
            with torch.no_grad():
                masks_pred = model(imgs)
                pred = torch.sigmoid(masks_pred)
                pred = (pred > 0.5).float()
                self.calcul_result(pred, true_masks)
                cv2.imwrite(os.path.join(self.save_dir, str(batch) +'.jpg'),pred*255.0)
    def calcul_result(self,pred,true_masks):
        with open(os.path.join(self.save_dir,'pre_log.txt'),'a') as f:
            for method in self.evaluate_method:
                if method=='sensitive':
                    score=metrics.precision_score(pred, true_masks,average='micro')
                    f.write("sensitive is {}" % score)
                if method=='specificity':
                    score =metrics.recall_score(pred, true_masks, average='macro')
                    f.write("specificity {}" % score)
                if method=='accuracy':
                    score =accuracy_score(pred, true_masks)
                    f.write("accuracy {}" % score)
                if method=='AUC':
                    score = roc_auc_score(pred, true_masks)
                    f.write("AUC is {}" % score)
                if method=='Dice':
                    score =Dice_coeff(pred, true_masks)
                    f.write("Dice is {}" % score)
                if method=='Jaccard':
                    score =jaccard_similarity_score(pred, true_masks)
                    f.write("Jaccard is {}" % score)