from numpy import minimum
import prepare_arrays_for_k_files, process_without_gui, upload_files_to_server
import os

path = ""
folder_name = ""
csv_path = path + "/" + folder_name + "/data.csv"
kFile_path = ""
target_path = path + "/" + folder_name
model_path = ""


server = ""
user = ""
password = ""
port = 22

local_path = path
server_path = "" 
command = "sbatch " + server_path  +"/"+folder_name+ "/{}/run_dyna.sh"

number_of_samples = 500

#keyword = "MAT_BARLAT_YLD2000_TITLE"
#words = ["       k", "e0", "n","  alpha1", "alpha2", "alpha3", "alpha4", "alpha5","alpha6","alpha7","alpha8"]
#minimums = [900, 550, 2.8, 0.40, 0.81, 0.80, 0.80, 0.81, 0.55, 0.86, 0.82] #aus excel und Quelle Mns und Maxs
#maximums = [1350, 2500, 4.9, 1.1, 1.5, 1.27, 1.12, 1.1, 1.1, 1.3, 1.7]

# Hocket-Sherby (Investigation ... of dual-phase steel)
keyword = "MAT_BARLAT_YLD2000_TITLE"
words = ["       k", "e0", "n", "p4", "  alpha1", "alpha2", "alpha3", "alpha4", "alpha5","alpha6","alpha7","alpha8"]
minimums = [850, 500, 2.7, 0.27, 0.40, 0.81, 0.80, 0.80, 0.81, 0.55, 0.86, 0.82]
maximums = [1250, 1150, 8.7, 0.65, 6, 1.1, 1.5, 1.27, 1.12, 1.1, 1.1, 1.3, 1.7]

print(path + "/" + folder_name)
print(csv_path, target_path, model_path)
prepare_arrays_for_k_files.create_csv(keyword, words, minimums, maximums, path + "/" + folder_name, number_of_samples)

# PRÜFEN Voce DC04 und DP600 (Selection and identification of elastplastic models for the materials used in the benchmarks)
words = ["       k", "e0", "n","  alpha1", "alpha2", "alpha3", "alpha4", "alpha5","alpha6","alpha7","alpha8"]
minimums = [110, 220, 10, 0.40, 0.81, 0.80, 0.80, 0.81, 0.55, 0.86, 0.82]
maximums = [360, 560, 16.5, 1.1, 1.5, 1.27, 1.12, 1.1, 1.1, 1.3, 1.7]

print(path + "/" + folder_name)
print(csv_path, target_path, model_path)
prepare_arrays_for_k_files.create_csv(keyword, words, minimums, maximums, path + "/" + folder_name, number_of_samples)

# NEU: SWIFT "Study on the influence of work-hardening modeling in springback prediction"
words = ["       k", "e0", "n","  alpha1", "alpha2", "alpha3", "alpha4", "alpha5","alpha6","alpha7","alpha8"]
minimums = [550, 0.0005, 0.145, 0.40, 0.81, 0.80, 0.80, 0.81, 0.55, 0.86, 0.82]
maximums = [1350, 0.01, 0.25, 1.1, 1.5, 1.27, 1.12, 1.1, 1.1, 1.3, 1.7]
prepare_arrays_for_k_files.create_csv(keyword, words, minimums, maximums, path + "/" + folder_name, number_of_samples)


ssh = upload_files_to_server.create_ssh_client(server, port, user, password)    
command = "sbatch run_dyna.sh"  
  
for i in range(9):
    print(command.format(10))
    stdin, stdout, stderr = ssh.exec_command(command.format(i))
    print(stdout.readlines())
ssh.close()



