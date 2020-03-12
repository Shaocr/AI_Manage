from code_transform import network
from management.manage_data import data_manage
class Console(object):
    def __init__(self):
        self.manage_dataset = data_manage()
    #创建抽象ai类
    def create_abstract_class(self,epochs=1,type_input='num',type_out='num',nodes='',learning_rate=0.01):
        self.abstract_class = network.abstract(epochs, type_input, type_out, nodes, learning_rate)
    #开始转换
    def start_code_transform(self):
        neutral = network.instance(self.abstract_class, self.data_info)
        neutral.train(self.data,self.label)
    def get_data_from_dataset(self,data_id):
        self.data,self.label,self.data_info = self.manage_dataset.get_data_from_database(data_id)
        print(self.data,self.label,self.data_info)
    def pass_data_to_dynamic_line(self,data):
        pass
console = Console()