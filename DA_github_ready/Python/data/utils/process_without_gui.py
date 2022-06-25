import errno

import pandas as pd
import itertools
import os, shutil
from kparser.models import KFile # utils outside of the machine learning scope of this project
import random
import paramiko
print("Start")



def create_data_object_from_csv(path):
    keyword_list = []
    word_list = []
    value_lists = []
    df = pd.read_csv(path)

    for index, row in df.iterrows():
        keyword_list.append(row["keyword"])
        word_list.append(row["word"])
        values = row["values"].split(" ")
        value_list = []
        for value in values:
            value_list.append(float(value.replace("'", "")))
        value_lists.append(value_list)

    data = {
        "Keyword": keyword_list,
        "Word":word_list,
        "Values":value_lists
    }
    return data


def convert_data():
    if len(all_entries) > 0:
        if len(sorted_kw_w_lists) == 0:
            sorted_kw_w_lists.append([all_entries[0]])
        else:
            keyword = sorted_kw_w_lists[-1][0]["Keyword"] 
            word = sorted_kw_w_lists[-1][0]["Word"] 
            if all_entries[0]["Keyword"] == keyword and all_entries[0]["Word"] == word:
                sorted_kw_w_lists[-1].append(all_entries[0])
            else:
                sorted_kw_w_lists.append([all_entries[0]])
        all_entries.pop(0)
        convert_data()


def create_changed_k_file(unmodified_k_file, task_list, path):
    modified_k_file = unmodified_k_file

    for i in range(len(task_list)):
        task_keyword = task_list[i]["Keyword"]
        task_word = task_list[i]["Word"]
        task_value = task_list[i]["Value"]

        for keyword in modified_k_file.keywords:
            if keyword.name == task_keyword:
                print("Keyword found")
                for word in keyword.words:
                    if word.name == task_word:
                        word.value = task_value
                    else:
                        continue                       
    modified_k_file.write_file(path)


def create_sim_folders(csv_path, kFile_path, target_path, model_path):
    data = create_data_object_from_csv(csv_path)
    k_file = KFile(kFile_path)
    df = pd.DataFrame(data=data)
    global all_entries
    all_entries = [] 
    global sorted_kw_w_lists
    sorted_kw_w_lists = []

    for index, row in df.iterrows():
        for entry in row["Values"]:
            entry_object = {}
            entry_object["Keyword"] = row["Keyword"]
            entry_object["Word"] = row["Word"]
            entry_object["Value"] = entry
            all_entries.append(entry_object)

    convert_data()
    sorted_kw_w_lists = list(itertools.product(*sorted_kw_w_lists))

    for entry in sorted_kw_w_lists:
        print("ENTRY")
        print(entry, type(entry))
        create_changed_k_file(k_file, entry, target_path +"/"+ str(sorted_kw_w_lists.index(entry))+".k")

    for root, dirs, files in os.walk(target_path):
        for f in files:
            if f.endswith(".k"):
                file_path = root + "/" + f
                new_model_path = file_path[:-2]
                os.mkdir(new_model_path)
                shutil.move(file_path, new_model_path + "/Mat_test.k")
                for entry in os.listdir(model_path):
                    if entry != "Mat_test.k":
                        shutil.copy(model_path + "/" + entry, new_model_path + "/" + entry)

    print(target_path + "/models_info.txt")
    print("WRITING INFO FILE")
    with open(target_path + "/models_info.txt", "w") as f:
        for entry in sorted_kw_w_lists:
            f.write("%s\n" % str(entry))
    print("DONE")


def create_sim_folders_2(csv_path, kFile_path, target_path, model_path):
    df = pd.read_csv(csv_path)
    csv_data = []
    k_file = KFile(kFile_path)

    df_2 = pd.DataFrame()
    for index, row in df.iterrows():
        keyword = row["keyword"]
        word = row["word"]
        values = row["values"]

        values = values.replace("'", "")
        values = values.split(" ")
        values = [float(i) for i in values]

        data_object = {
                        "keyword":keyword,
                        "word": word,
                        "values":values
                    }
        csv_data.append(data_object)
        df_2[word] = data_object["values"]
        
    for i in range(1, len(csv_data)):
        if len(csv_data[i-1]) != len(csv_data[i]):
            print("DATA FORMAT FAILURE")

    list_of_list_of_data_objects = []
    for e in csv_data:
        list_of_data_objects = []
        for i in range(len(e["values"])):
            keyword = e["keyword"]
            word = e["word"]
            value = e["values"][i]

            data = {}
            data["Keyword"] = keyword
            data["Word"] = word
            data["Value"] = value
            list_of_data_objects.append(data)
        list_of_list_of_data_objects.append(list_of_data_objects)
        
    task_list = []
    for i in range(len(list_of_list_of_data_objects[0])):
        entry = []
        for j in range(len(list_of_list_of_data_objects)):        
            entry.append(list_of_list_of_data_objects[j][i])
        entry = tuple(entry)
        task_list.append(entry)

    for entry in task_list:
        create_changed_k_file(k_file, entry, target_path +"/"+ str(task_list.index(entry))+".k")

    for root, dirs, files in os.walk(target_path):
        for f in files:
            if f.endswith(".k"):
                file_path = root + "/" + f
                new_model_path = file_path[:-2]
                os.mkdir(new_model_path)
                shutil.move(file_path, new_model_path + "/Mat_test.k")
                for entry in os.listdir(model_path):
                    if entry != "Mat_test.k":
                        shutil.copy(model_path + "/" + entry, new_model_path + "/" + entry)

    with open(target_path + "/models_info.txt", "w") as f:
        for entry in task_list:
            f.write("%s\n" % str(entry))
    print("DONE")


def create_sim_folders_3(csv_path, kfile_path, target_path, model_path):#, kFile_path, target_path):
    df = pd.read_csv(csv_path)

    unmodified_kfile = KFile(kfile_path)
    for i in range(len(df.index)):
        value_string = df["values"].iloc[i]
        value_string.replace("'", "")
        values = value_string.split(" ")
        values[0] = values[0].replace("'", "")
        values[-1] = values[-1].replace("'", "")
        df["values"].iloc[i] = values

    # select right words and values and change k file accordingly than write copy to different path
    for j in range(len(df["values"][0])):
        for i in range(len(df["word"])):
            keyword = df["keyword"][i]
            word = df["word"][i]
            value = df["values"][i][j]
            print(keyword, word, value)

            for kw in unmodified_kfile.keywords:
                if kw.name == keyword:
                    print("Keyword found.")
                    for w in kw.words:
                        if w.name == word:
                            print("Word found.")
                            print("Before: ", w.value)
                            w.value = value
                            print("After: ", w.value)

        shutil.copytree(model_path, target_path.format(j))
        unmodified_kfile.write_file(target_path.format(str(j)+"\Mat_test.k"))


def create_sim_folder_with_random_model(model_path, target_path, obj, index):

    def change_kfile(kfile_path, obj):
        kfile = KFile(kfile_path)
        for keyword in kfile.keywords:
            if keyword.name == obj["Keyword"]:
                for word in keyword.words:
                    if word.name == obj["Word"][0]:
                        word.value = obj["Values"][0]
                    elif word.name == obj["Word"][1]:
                        word.value = obj["Values"][1]

        kfile.write_file(kfile_path)

    def copy_folder(model_path, target_path):
        actual_target_path = target_path + "\\" + "New_" + str(index) + "old_" + model_path.split("\\")[-1]
        try:
            shutil.copytree(model_path, actual_target_path)
        except OSError as exc:
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(model_path, actual_target_path)
            else:
                raise
        return actual_target_path

    new_target_path = copy_folder(model_path, target_path)
    kfile_path = new_target_path + "\\Mat_test.k"
    change_kfile(kfile_path, obj)


def choose_random_model(model_root_path):
    path_list = [x[0] for x in os.walk(model_root_path) if x[0] != model_root_path]
    return random.choice(path_list)


def cowper_symonds_samples(csv_path, model_root_path, target_path):
    # main function for cowper-symonds
    data = create_data_object_from_csv(csv_path)
    info_list = []
    for key, value in data.items(): print(key, value)
    for i in range(len(data["Values"][0])):
        obj = {
            "Keyword" : data["Keyword"][0], #check
            "Word" : ["c", "p"], #data["Word"], #check
            "Values" : [data["Values"][0][i], data["Values"][1][i]] #check
        }
        model_path = choose_random_model(model_root_path)
        create_sim_folder_with_random_model(model_path, target_path, obj, i)
        obj["path"] = model_path
        info_list.append(obj)

    with open(target_path + "\\info.txt", "w") as f:
       for obj in info_list:
           f.write("%s\n" % obj)


def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def start_run(server, port, user, password, commands):
    print("START PROCESS...")
    ssh = create_ssh_client(server, port, user, password)
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print("EXECUTING")
        lines = stdout.readlines()
        print(lines)
        ssh.close


if __name__ == "__main__":

    server=""
    port=""
    user=""
    password=""

    root_path = ""
    laws = ["swift", "voce", "hocket-sherby"]
    local_root_path = r""

    command_list = []
    for law in laws:
        local_formated_path = local_root_path.format(law=law)
        dir_list = [x[0].replace(local_formated_path, "")[1:] for x in os.walk(local_formated_path)][1:]
        for dir in dir_list:
            formated_dir_path = root_path.format(law=law, dir=dir) + "/run_dyna.sh"
            command_list.append("sbatch " + formated_dir_path)

    