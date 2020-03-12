'''
此文件用于将图形化的图类数据结构转换为tensorflow代码
'''

#import tensorflow as tf
from code_transform.config import *
from management.manage_data import data_manage
import json
import tensorflow as tf
import numpy as np
'''
抽象类 负责抽象出一个神经网络框架 
用于后续实例化
'''
class abstract(object):
    def __init__(self,epochs,type_input,type_out,nodes,learning_rate=0.01):
        self.epochs = epochs
        self.type_input = type_input
        self.type_out = type_out
        self.nodes = nodes
        self.learning_rate = learning_rate

'''
用于实例化神经网络的类
'''
class instance(object):
    def __init__(self,abstract,data_info):
        #data_info: [{'input_name':{'shape':input_data.shape,'type':input_data.type}},
        #           {'output_name':{'shape':out_data.shape,'type':out_shape.type}}]
        #input_data.shape 和 out_data.shape 可能都是列表形式
        #因为模型很可能会用多个输入和输出
        self.config = abstract
        self.input=data_info[0]
        self.out=data_info[1]
        self.input_nodes = []
        self.out_nodes = []
        self.other_nodes = []
        self.out_loss = {}
    def read_json(self):
        nodes = json.loads(self.config.nodes)

        for i in nodes:
            if i['type']=='input':
                self.input_nodes.append(i)
            elif i['type']=='out':
                self.out_nodes.append(i)
                self.out_loss['output_{}'.format(i['id'])] = 'mse'
            else:
                self.other_nodes.append(i)
    def neural_net(self):
        self.read_json()
        #保存每个节点输出信息
        out_nodes={}
        #遍历输入节点
        list_input = []
        for i in self.input_nodes:
            input_node = self.input[i['title']]
            temp_input = tf.keras.Input(input_node['shape'],dtype=input_node['type'],name='input_{}'.format(i['id']))
            list_input.append(temp_input)
            out_nodes[i['id']]=temp_input
        #遍历隐层节点
        temp_other_nodes = self.other_nodes
        while len(temp_other_nodes)!=0:
            i=temp_other_nodes[0]
            if i['type']=='hidden':
                #父节点已经被计算过
                if i['parent'][0] in out_nodes.keys():
                    previous_out = out_nodes[i['parent'][0]]
                    out_nodes[i['id']] = tf.keras.layers.Dense(i['units'],
                                                        activation='relu',
                                                    dtype=previous_out[0].dtype)(previous_out)
                    temp_other_nodes.remove(i)
                #若父节点未被计算过
                else:
                    temp_other_nodes.remove(i)
                    temp_other_nodes.append(i)
            #运算节点 比如加法或者乘法或者减法
            else:
                previous_out=[]
                for j in i['parent']:
                    previous_out.append(out_nodes[j])
                out_nodes[i['id']] = tf.keras.layers.concatenate(previous_out)
                temp_other_nodes.remove(i)
        #保存输出节点
        list_output=[]
        for i in self.out_nodes:
            #这里以后修改一下 两个节点的输出同时连一个节点的输入的情况
            #暂时想到的解决办法 新加一个加法节点 type='add'
            #加完之后再连接到下一个节点
            previous_out = out_nodes[i['parent'][0]]
            temp_out =tf.keras.layers.Dense(i['units'],
                                            activation='relu',
                                            dtype=previous_out.dtype,
                                            name='output_{}'.format(i['id']))(previous_out)
            out_nodes[i['id']]=temp_out
            list_output.append(temp_out)
        model = tf.keras.Model(list_input,list_output)
        return model
    def train(self,input_data,labels):
        model = self.neural_net()
        logs_loss = LossHistory()
        model.compile(optimizer='rmsprop',
                      loss=self.out_loss,
                      metrics=['mae'],
                      callbacks=[logs_loss])
        model.fit(input_data,labels,batch_size=200,epochs=self.config.epochs)
'''
callback回调类
用于训练过程中实时获取训练损失函数或者准确率
'''
class LossHistory(tf.keras.callbacks.Callback):
    # 函数开始时创建盛放loss与acc的容器
    def on_train_begin(self, logs={}):
        self.losses = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.val_loss = {'batch': [], 'epoch': []}
        self.val_acc = {'batch': [], 'epoch': []}

    # 按照batch来进行追加数据
    def on_batch_end(self, batch, logs={}):
        # 每一个batch完成后向容器里面追加loss，acc
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        # 每一个epoch完成后向容器里面追加loss，acc
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))


if __name__=='__main__':
    a = abstract(20,1,1,1,0.01)
    data_m = data_manage()
    data,labels,data_info = data_m.test_mult()
    ins = instance(a,data_info)
    ins.train(data,labels)
