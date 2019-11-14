import csv
import datetime
import operator
import sys
import statistics

border_crossing_in = sys.argv[1]
report_out = sys.argv[2]
print(border_crossing_in)
print(report_out)

counter = 0
data_acc = {}
with open(border_crossing_in) as file:
    readCSV = csv.reader(file, delimiter=',')
    for row in readCSV:
        if counter != 0:
            if data_acc.get(row[3]) is None:
                data_acc[row[3]] = {}
                data_acc[row[3]][row[5]] = {}
                data_acc[row[3]][row[5]][row[4]] = int(row[6])
            else:
                if data_acc[row[3]].get(row[5]) is None:
                    data_acc[row[3]][row[5]] = {}
                    data_acc[row[3]][row[5]][row[4]] = int(row[6])
                else:
                    if data_acc[row[3]][row[5]].get(row[4]) is None:
                        data_acc[row[3]][row[5]][row[4]] = int(row[6])
                    else:
                        data_acc[row[3]][row[5]][row[4]] += int(row[6])
        counter += 1
output_array = []
# in data_acc - border as dict key and border_value as value
for border, border_value in data_acc.items():
    for measure, measure_value in border_value.items():
        temp = sorted(list(measure_value), key=lambda x: datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S %p"),
                      reverse=True)
        measure_values_sum = sum(measure_value.values())
        month_counter = 1
        for date in temp:
            measure_values_sum -= measure_value[date]
            if len(temp) - month_counter == 0:
                measure_value[date] = [measure_value[date], 0]
            else:
                # python round not work correct for x.5 - will be round to x.0
                if (measure_values_sum / (len(temp) - month_counter) + 0.5) - (
                        measure_values_sum / (len(temp) - month_counter) + 0.5) == 0:
                    average = int(round(measure_values_sum / (len(temp) - month_counter) + 0.5, 1))
                else:
                    average = int(round(measure_values_sum / (len(temp) - month_counter)))
                measure_value[date] = [measure_value[date], average]
            month_counter += 1
        for date, date_value in measure_value.items():
            output_array.append([border, date, measure, str(date_value[0]), str(date_value[1])])
output_array.sort(key=operator.itemgetter(1, 4, 2, 1), reverse=True)

with open(report_out, mode='w') as report_file:
    report_writer = csv.writer(report_file, delimiter=',')
    report_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])
    for out_row in output_array:
        report_writer.writerow(out_row)
