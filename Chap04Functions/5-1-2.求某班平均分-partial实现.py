import csv
from easygraphics import dialog as dlg
from functools import partial

class Score:
    def __init__(self,id,name, clazz, math,literacy,english):
        self.id = id
        self.name = name
        self.clazz = clazz
        self.math = math
        self.literacy=literacy
        self.english = english

def read_csv(filename):
    """
    从csv文件中读取学生成绩信息
    :param filename: 文件名
    :return: 学生信息列表
    """
    scores=[]
    with open(filename,mode="r",encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = row[0]
            name = row[1]
            clazz = row[2]
            math = int(row[3])
            literacy = int(row[4])
            english = int(row[5])
            score = Score(id,name,clazz,math,literacy,english)
            scores.append(score)
    return scores

def score_to_total(score):
    return score.math+score.english+score.literacy

def filter_by_class_base(score, clazz):
    return score.clazz == clazz

filename = dlg.get_open_file_name("请选择数据文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)
scores = read_csv(filename)

my_clazz = dlg.get_string("请输入班级名称")
filter_by_class = partial(filter_by_class_base, clazz = my_clazz)
lst1=filter(filter_by_class,scores)
lst2=list(map(score_to_total,lst1))
total = sum(lst2)
count = len(lst2)
average = total / count
print(f"{my_clazz}班{count}名同学三科平均分为{average:.2f}")