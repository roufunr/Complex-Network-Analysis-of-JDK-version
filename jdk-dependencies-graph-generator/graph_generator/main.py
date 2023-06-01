import csv
import os
import re
from config import major_packages, jdk_path, jdk_version
def recurse_create_maps(current_map, key, value):
    if '.' in key:
        current_key = key.split('.')[0]
        deeper_map = current_map.get(current_key)

        if isinstance(deeper_map, dict):
            recurse_create_maps(deeper_map, key[key.index('.') + 1:], value)
        else:
            deeper_map = {}
            current_map[current_key] = deeper_map
            recurse_create_maps(deeper_map, key[key.index('.') + 1:], value)
    else:
        current_map[key] = value
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


nodes = []
flat_path_dict = {}
hierarchical_path_dict = {}

# generate all node and json structure
for pkg in major_packages:
    base_path = jdk_path + pkg
    all_classes_path = [os.path.join(dp, f) for dp, dn, filenames in os.walk(base_path) for f in filenames if
                        os.path.splitext(f)[1] == '.java']
    for cls_path in all_classes_path:
        class_signature = cls_path.replace(jdk_path, "")
        class_signature = class_signature.replace(".java", "")
        class_signature = class_signature.replace("/", ".")
        nodes.append(class_signature)
        flat_path_dict[class_signature] = cls_path
        recurse_create_maps(hierarchical_path_dict, class_signature, class_signature)

# read file and generate dependencies edge
total_nodes = len(nodes)
edges = []
for node_idx in range(total_nodes):
    node_path = flat_path_dict[nodes[node_idx]]
    with open(node_path, 'r') as file:
        for line in file:
            line = line.strip()
            if re.match(r'^import\s.*;$', line):
                line = line.replace("import", "")
                line = line.replace(" ", "")
                line = line.replace(";", "")

                imported_dependency = line
                # containing star *
                if "*" in imported_dependency:
                    before_star = imported_dependency.replace(".*", "")
                    splitted_packages_array = before_star.split(".")
                    executable_str = "hierarchical_path_dict"
                    for key in splitted_packages_array:
                        executable_str += "['" + key + "']"
                    sub_dict = None
                    try:
                        sub_dict = eval(executable_str)
                    except:
                        print(imported_dependency, 'is not present')

                    if sub_dict is not None:
                        if isinstance(sub_dict, dict):
                            flat_sub_dict = flatten_dict(sub_dict)
                            for key in flat_sub_dict:
                                from_idx = node_idx

                                if flat_sub_dict[key] in nodes:
                                    to_idx = nodes.index(flat_sub_dict[key])
                                    edges.append([from_idx, to_idx])
                        else:
                            if sub_dict in nodes:
                                to_idx = nodes.index(sub_dict)
                                edges.append([from_idx, to_idx])
                else:
                    from_idx = node_idx
                    if imported_dependency in nodes:
                        to_idx = nodes.index(imported_dependency)
                        edges.append([from_idx, to_idx])

edges_csv_header = ["from", "to"]
edges_csv_file_name = "../dataset/edges_" + (jdk_version.replace(".", "_")) + ".csv"
with open(edges_csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(edges_csv_header)
    writer.writerows(edges)

classes_csv_header = ["idx", "classname"]
classes_csv_file_name = "../dataset/classes_" + (jdk_version.replace(".", "_")) + ".csv"
with open(classes_csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(classes_csv_header)
    for i in range(len(nodes)):
        writer.writerow([i, nodes[i]])

info_csv_header = ["Total_Nodes", "Total_Edges"]
info_csv_file_name = "../dataset/info_" + (jdk_version.replace(".", "_")) + ".csv"
with open(info_csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(info_csv_header)
    writer.writerow([len(nodes), len(edges)])
