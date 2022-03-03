# pylint: disable=unspecified-encoding
import csv
import re
import os
import time
import subprocess

while True:

    def exec_command():
        encoding = 'utf-8'
        process = subprocess.Popen('sudo virt-top -n 2 --stream', stdout=subprocess.PIPE, shell=True)
        output = process.communicate()[0].decode(encoding)

        return output

    def write_csv(start, end):
        '''
        This function is for writing the values to a csv file
        '''
        with open('out.csv', 'a') as file:
            write = csv.writer(file)
            if os.stat('out.csv').st_size == 0:
                write.writerow(headers)
            for row in lists[start:end]:
                new_list = row[2:5]
                new_list.insert(1, row[-1])
                write.writerow(new_list)

    def add_time_column(indexes):
        '''
        This is a fucntion for adding the time column
        '''
        for enum, value in enumerate(indexes):
            start = value + 2
            time = lists[value][2]
            if enum < len(indexes) - 1:
                end = indexes[(enum + 1) % len(indexes)]
                for item in lists[start:end]:
                    item.insert(2, time)
                write_csv(start, end)
            else:
                for item in lists[value+2:]:
                    item.insert(2, time)
                write_csv(start, -1)

    def cal_index(lists):
        '''
        This is a function for calculating the indexes of lines which contain virt-top
        '''
        word = 'virt-top'
        count = 0
        indexes = []
        for l in lists:
            for item in l:
                if item == word:
                    if count != 0:
                        indexes.append(lists.index(l))
                    count = count + 1
        return indexes

    string = exec_command().split('\n')
    lists = []
    headers = ['Time', 'Domain', 'RDRQ', 'WRRQ']
    for s in string:
        lists.append(list(re.sub(r'\s+', ' ', s).split()))

    index = cal_index(lists)
    add_time_column(index)
