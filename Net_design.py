import torch.nn.functional as F
import torch.nn as nn
from .unet_parts import *
from upmodule import *
import json
class Net_design(nn.Module):
    def __init__(self, used_model_list,bilinear=True):
        super(Net_design, self).__init__()
        self.n_in = 3
        self.n_out = 2
        self.bilinear = bilinear

        self.inc = DoubleConv(self.n_in, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        factor = 2 if bilinear else 1
        self.down4 = Down(512, 1024 // factor)
        self.up1 = Up(1024, 512 // factor, bilinear)
        self.up2 = Up(512, 256 // factor, bilinear)
        self.up3 = Up(256, 128 // factor, bilinear)
        self.up4 = Up(128, 64, bilinear)
        self.outc = OutConv(64, 2)
        self.net_list = [self.inc, self.down1, self.down2, self.down3, self.down4,
         self.up1, self.up2, self.up3, self.up4, self.outc]
        self.used_model_list = used_model_list
        self.new_net_dict = self.build()
    def build(self):
        new_net_dict=[]
        load_f = open(self.used_model_list, 'r', encoding='utf-8')
        papers = []
        for line in load_f.readlines():
            dic = json.loads(line)
            papers.append(dic)
        papers=papers[0]
        for i in range(len(self.net_list)):
            new_net_dict.append(self.net_list[i])
            for paper in papers:
                if str(i) == list(paper.keys())[0]:
                    add_list = paper[str(i)]
                    for module in add_list:
                        if module=='aspp':
                            new_net_dict.append(self.add_aspp())
                        if module=='deep':
                            new_net_dict.append(self.add_deep())
                        if module=='attention':
                            new_net_dict.append(self.add_attention())
                        if module=='dense':
                            new_net_dict.append(self.add_dense())
                        if module=='resblock':
                            new_net_dict.append(self.add_resblock())
        return new_net_dict

    def forward(self,x):
        for module in self.new_net_dict:
            x=module(x)
        return x

    def add_resblock(self):
        add_module = ResBlock(self.n_in, self.n_out)
        return add_module
    def add_aspp(self):
        add_module = ASPP(self.n_in, self.n_out)
        return add_module
    def add_attention(self):
        add_module = SELayer(self.n_in,self.n_out)
        return add_module

