import argparse
import logging
import os
import sys

import numpy as np
import torch
import torch.nn as nn
from torch import optim
from torch.utils.tensorboard import SummaryWriter
from utils.dataset import trainSampler
from torch.utils.data import DataLoader, random_split
from Net_design import Net_design
from dice_loss import DiceLoss
class Net_train(object):
    def __init__(self,used_model_list,learning_rate,epoch,opreater,loss_func,batch_size,data_path,save_dir):
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.opreater =opreater
        self.loss_func=loss_func
        self.batch_size = batch_size
        self.data_path = data_path
        self.save_dir = save_dir
        self.used_model_list = used_model_list
    def train(self):
        model = Net_design(self.used_model_list)
        device = torch.cuda.current_device()
        dataset = trainSampler(self.data_path)
        train_loader = DataLoader(dataset, batch_size=self.batch_size,
                                  shuffle=True, num_workers=8, pin_memory=True)
        if self.opreater =='Adam':
            optimizer=optim.Adam(model.parameters(), lr=self.learning_rate)
        elif self.opreater =='SGD':
            optimizer=optim.SGD(model.parameters(), lr=self.learning_rate)
        else:
            optimizer=optim.SGD(model.parameters(), lr=self.learning_rate,momentum=0.9)
        if self.loss_func =='CE':
            criterion = nn.CrossEntropyLoss()
        else:
            criterion = DiceLoss()
        with open(os.path.join(self.save_dir,'train_log.txt'),'a') as f:
            for ep in range(self.epoch):
                model.train()
                epoch_loss = 0.0
                for batch in train_loader:
                    imgs = batch['image']
                    true_masks = batch['mask']
                    imgs = imgs.to(device=device, dtype=torch.float32)
                    true_masks = true_masks.to(device = device, dtype = torch.float32)
                    masks_pred = model(imgs)
                    loss = criterion(masks_pred, true_masks)
                    f.write("epoch is {}:loss is {}" % {(ep+1),loss.item()})
                    logging.info("epoch is {epoch + 1}:loss is {loss.item()}")
                    epoch_loss += loss.item()
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                if ep % 5000 == 0:
                    torch.save(model.state_dict(),
                               self.save_dir + f'CP_epoch{ep + 1}.pth')

