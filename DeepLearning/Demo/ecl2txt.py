import os
import random
from openpyxl import load_workbook

# 默认可读写，若有需要可以指定write_only和read_only为True
wb = load_workbook('qanda_01.xlsx')

train_filename = 'train.txt'
test_filename = 'test.txt'
train_test_percent = 0.3

# # 获得所有sheet的名称
# print(wb.get_sheet_names())
# # 根据sheet名字获得sheet
# a_sheet = wb.get_sheet_by_name('T1')
# # 获得sheet名
# print(a_sheet.title)
# # 获得当前正在显示的sheet, 也可以用wb.get_active_sheet()
sheet = wb.active

q_list = []
a_list = []
for cell in sheet['A':'A']:
    q_list.append(cell.value)
for cell in sheet['B':'B']:
    a_list.append(cell.value)


full_len = len(q_list) * len(a_list)

validation = random.sample(range(full_len), int(full_len*train_test_percent))
# print(len(valdation))

# 删除旧的文件
if os.path.exists(train_filename):
    os.remove(train_filename)
if os.path.exists(test_filename):
    os.remove(test_filename)

# 生成新的train和test文件
file_train = open(train_filename, mode='a')
file_test = open(test_filename, mode='a')
print('file save Start!')
for i in range(len(q_list)):
    for j in range(len(a_list)):
        #生成 Q & A 对的lable 标签 正确答案为1 错误匹配为0
        label = 1 if i == j else 0
        qa_content = '{},{},{}\n'.format(q_list[i].replace(
            ',', ' '), a_list[j].replace(',', ' '), label)
        cur_index = (i+1)*(j+1)
        #根据随机产生的测试集数组生成测试文件。其他的为训练文件
        if cur_index in validation:
            file_test.write(qa_content)
        else:
            file_train.write(qa_content)
        #print('{},{},{}'.format(q_list[i], a_list[j], label))

file_train.close()
file_test.close()

#生成完毕
print('file save completed!')
