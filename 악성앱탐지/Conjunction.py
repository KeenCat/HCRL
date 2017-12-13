import sys
from collections import OrderedDict, namedtuple
import csv
score1 = namedtuple("score1", "first_mal_accuracy first_family_accuracy first_total_accuracy")
score2 = namedtuple("score2", "second_mal_accuracy second_family_accuracy second_total_accuracy")
if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    result1 = open(file1).read().splitlines()
    result2 = open(file2).read().splitlines()
    first_f1 = OrderedDict()
    second_f1 = OrderedDict()
    print(file1)
    for line in result1[1:]:
        words = line.split(',')
        first_f1[words[0]] = score1(float(words[1]), float(words[2]), float(words[3]))._asdict()

    for line in result2[1:]:
        words = line.split(',')
        second_f1[words[0]] = score2(float(words[1]), float(words[2]), float(words[3]))._asdict()

    final = open('result_final_andro_all.csv', 'w')
    final.write('team_index,1st_mal_accuracy,1st_family_accuracy,1st_total_accuracy,2nd_mal_accuracy,2nd_family_accuracy,2nd_total_accuracy,total_accuracy\n')
    for team, score in first_f1.items():
        first = first_f1[team]['first_total_accuracy']
        second = second_f1[team]['second_total_accuracy']
        firstmal = first_f1[team]['first_mal_accuracy']
        firstfam = first_f1[team]['first_family_accuracy']
        secondmal = second_f1[team]['second_mal_accuracy']
        secondfam = second_f1[team]['second_family_accuracy']
        final.write(team+','+str(firstmal)+ ',' + str(firstfam)+','+str(first)+','+ str(secondmal)+',' + str(secondfam)+ ','+ str(second)+','+ str((first+second)/2)+'\n')
    final.close()


