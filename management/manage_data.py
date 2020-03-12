import numpy as np
class data_manage(object):
    def __init__(self):
        pass
    def get_data_from_database(self,data_id):
        #从数据库中取出来数据
        if data_id==8851:
            return self.test()
    def get_new_data(self):
        #新的训练集存到数据库
        pass
    def test(self):
        data = np.random.random((1000, 32)).astype('float32')
        labels = np.random.random((1000, 1)).astype('float32')
        data_info=[{'input_main':{'shape':(32,),'type':data.dtype}},
                   {'output':{'shape':(1,),'type':labels.dtype}}]
        return data,labels,data_info
    def test_mult(self):
        data = [np.random.random((1000,32)).astype('float32'),np.random.random((1000,16)).astype('float32')]
        labels = np.random.random((1000,1)).astype('float32')
        data_info=[
            [{'shape':(32,),'type':data[0].dtype},{'shape':(16,),'type':data[1].dtype}],
            {'shape': (1,), 'type': labels.dtype}
        ]
        return data,labels,data_info