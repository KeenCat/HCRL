from collections import defaultdict, OrderedDict, namedtuple
from itertools import islice
import csv
import sys
import os
import pandas as pd

answer = namedtuple("answer", "malware family classdetection familydetection")

Answer = OrderedDict(defaultdict(lambda: dict))

first_row = True
if __name__ == "__main__":
    answerfile = sys.argv[1]
    submitdir = sys.argv[2]
    result_name = sys.argv[3]

    with open(result_name + ".csv", "w", newline='\n') as resultFile:
        writer = csv.writer(resultFile)
        writer.writerow(['team_index','mal_accuracy', 'family_accuracy', 'total_accuracy'])
        for root, dir, files in os.walk(submitdir):
            if (first_row is True):
                first_row = False
                first_row_name = root
                continue
            dir_name = root[len(first_row_name)+1:]
            for result_index, filename in enumerate(files):

                if (filename[-3:] == "csv"):
                    FamilyCount = 0
                    DiffCount = 0
#                    print(filename)

                    with open(answerfile) as file:
                        reader = csv.reader(file)
                        for idx, row in enumerate(reader):
                            if idx == 0:
                                continue
                            Answer[row[0]] = answer(row[1], row[2], False, False)._asdict()
                            if row[2] != 'na':
                                FamilyCount += 1 

                    dis = 0
                    submitFileName = submitdir +"/" + dir_name + "/" + filename
                    print(filename + " scoring start")
                    
                    #Submit.clear()
                    with open(submitFileName) as file:
                        reader = csv.reader(file)

                        for idx, r in enumerate(reader):
                            if idx == 0:
                                continue
                            try:
                                malware_name = r[0].split('.')[0]
                                if malware_name in Answer.keys():
                                    if Answer[malware_name]['malware'].lower() == r[1].lower():
                                        Answer[malware_name]['classdetection'] = True
                                    if r[2].lower().strip() != 'na':
                                        if Answer[malware_name]['family'].lower() == r[2].lower().strip():
                                            Answer[malware_name]['familydetection'] = True
                                else:
                                    DiffCount += 1


                            except:
                                dis = 1
                                break
                        if DiffCount != 0:
                            print("Different Hash Value " + str(DiffCount))
                        if dis == 1:
                            print('Disqualification (Format Error)')
                            acc = 0
                            facc = 0
                            tacc = 0
                        else:
                            classNegative, classPositive, familyNegative, familyPositive = 0, 0, 0, 0

                            for key, value in Answer.items():
                                # print(key, value['detection'])
                                if (not value['classdetection']):
                                    classNegative += 1
                                else:
                                    classPositive += 1

                                if (not value['familydetection']):
                                    familyNegative += 1
                                else:
                                    familyPositive += 1 
                            Allnum = classNegative + classPositive

                            acc = float(classPositive) / Allnum

                            facc = float(familyPositive) / FamilyCount


                            tacc = acc * 0.6 + facc * 0.4

                        writer.writerow([dir_name, round(acc*100, 3), round(facc*100, 3), round(tacc*100, 3)])

    df = pd.read_csv(result_name + ".csv", encoding='latin1')
    df.columns = ['team_index','mal_accuracy', 'family_accuracy', 'total_accuracy']
    df.to_csv(result_name + ".csv", index=False, encoding='latin1')
