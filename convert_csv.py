# Open file for reading
import csv

# classes_file = open('dataset/classes_1_6.csv', 'w', newline='')
# writer = csv.writer(classes_file)
# writer.writerow(['idx', 'classname'])
# with open('dataset/ent.subelj_jdk_jdk.class.name', 'r') as file:
#     # Loop through each line of the file
#     idx = 0
#     for line in file:
#         data = line.replace("\n", "")
#         writer.writerow([idx, data])
#         idx += 1
# classes_file.close()

# edges_file = open('dataset/edges_1_6.csv', 'w', newline='')
# writer = csv.writer(edges_file)
# writer.writerow(['from', 'to'])
# with open('dataset/out.subelj_jdk_jdk', 'r') as file:
#     # Loop through each line of the file
#     idx = 0
#     for line in file:
#         if idx < 2:
#             idx += 1
#             continue
#         else:
#             data = line.replace("\n", "")
#             data = line.split(" ")
#             writer.writerow([int(data[0]) - 1, int(data[1]) - 1])
#             idx += 1
#
# edges_file.close()
