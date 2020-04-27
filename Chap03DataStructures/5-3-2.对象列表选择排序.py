import csv
import easygraphics.dialog as dlg
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: int
    name: str
    score: Decimal

def read_csv(filename):
    """
    从csv文件中读入学生成绩信息
    :param filename: csv文件名
    :return: 学生成绩列表
    """
    scores = []
    with open(filename, mode = "r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = int(row[0])
            name = row[1]
            score = Decimal(row[2])
            s=Score(id,name,score)
            scores.append(s)
    return scores

def select_sort(scores):
    """
    选择排序
    :param scores: 待排序列表
    """
    n = len(scores)
    for i in range(n):
        t = i
        for j in range(i, n):
            if scores[j].score > scores[t].score:
                t = j
        scores[i],scores[t] = scores[t],scores[i]

#5-2-2.成绩.csv
filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)

select_sort(scores)
dlg.show_objects(scores)