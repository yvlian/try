import os
import zipfile
from bert_serving.client import BertClient
bc = BertClient()
from tool import get_graph_and_nodes_ins_for_apk

def get_data(apk_dir, data_dir,bc):
    apk_classes = os.listdir(apk_dir)  # get all the names of apps
    data_path = data_dir+[x for x in apk_dir.split('/')][-2]
    with open(data_path+'.txt','a') as f:
        for apk_class in apk_classes:
            if os.path.isdir(apk_class):continue
            adj,node_feature = get_graph_and_nodes_ins_for_apk(apk_dir+apk_class,bc)
            a=-1
    return 1

apk_dir = "../apk_data/"  # this is apk files' store path
data_dir = '../data/'

benign_path = apk_dir + 'benign/'
unbenign_path = apk_dir + 'unbenign/'
benign_data,unbenign_path = get_data(benign_path, data_dir,bc), get_data(unbenign_path, data_dir,bc)

#需要开启 bert-serving才能用
# cmd = "bert-serving-start -model_dir E:\projects\wwm_uncased_L-24_H-1024_A-16 -num_worker=4"
# os.system(cmd)

