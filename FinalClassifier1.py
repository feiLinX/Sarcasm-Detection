
import torch
import numpy as np
import LoadData1
import AttributeFeature
import ImageFeature
import FuseAllFeature1

#%%

class ClassificationLayer(torch.nn.Module):
    def __init__(self,dropout_rate=0):
        super(ClassificationLayer, self).__init__()
        self.Linear_1=torch.nn.Linear(512,256)
        self.Linear_2=torch.nn.Linear(256,2)
        self.dropout=torch.nn.Dropout(dropout_rate)
        
    def forward(self,input):
        hidden=self.Linear_1(input)
        hidden=self.dropout(hidden)
        
        output=torch.sigmoid(self.Linear_2(hidden))
        return output
if __name__ == "__main__":
    image=ImageFeature.ExtractImageFeature()
    attribute=AttributeFeature.ExtractAttributeFeature()
    fuse=FuseAllFeature1.ModalityFusion()
    final_classifier=ClassificationLayer()
    for image_feature,attribute_index,group,id in LoadData1.train_loader:
        image_result,image_seq=image(image_feature)
        attribute_result,attribute_seq=attribute(attribute_index)

        output=fuse(image_result,image_seq,attribute_result,attribute_seq.permute(1,0,2))
        result=final_classifier(output)
        predict=torch.round(result)



        print(result)
        break
