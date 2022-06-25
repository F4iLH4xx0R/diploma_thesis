from pyDOE2 import *
import pandas as pd
import numpy as np

# perform latin hypercube sampling for input data
# create csv file for creating Mat.k Files for Simulation

# n: integer for number of factors (required)
# samples: integer, number of sample points (default: n)
# output: array n*n dimensions 

number_of_samples = 500
keyword = "MAT_BARLAT_YLD2000_TITLE"
words = ["       k", "e0", "n","  alpha1", "alpha2", "alpha3", "alpha4", "alpha5","alpha6","alpha7","alpha8", "Young"]
minimums = [600, 0.02, 0.05, 0.40, 0.81, 0.80, 0.80, 0.81, 0.55, 0.86, 0.82, 160000] #aus excel und Quelle Mns und Maxs
maximums = [1200, 0.05, 0.3, 1.1, 1.5, 1.27, 1.12, 1.1, 1.1, 1.3, 1.7, 220000]

class data_list_object:
    def __init__(self, keyword, word, min, max):
        self.keyword = keyword
        self.word = word
        self.min = min
        self.max = max
        self.values = []
        self.value_string = ""
        #print(type(self.word))

    def fill_values(self, list_from_sample):
        for entry in list_from_sample:
            value = self.min + (self.max - self.min) * entry
            self.values.append(value)

    def transform_list_to_string(self):
        list_string = "'"
        for value in self.values:
            list_string += str(value) + " "
        list_string = list_string[:-1] + "'"
        self.value_string = list_string
    
def create_csv(keyword, words, minimums, maximums, path, name, number_of_samples):
    if len(words) == len(minimums) == len(maximums):
        data_list = []
        for i in range(len(words)):
            data_list.append(data_list_object(keyword, words[i], minimums[i], maximums[i]))

        sampling_array = lhs(n=len(words), samples=number_of_samples)
        sampling_array = sampling_array.transpose() #damit jede Reihe Werte für eine Variable enthält
        print("TRANSPOSED")
        #print(sampling_array)

        for i in range(len(words)): 
            data_list[i].fill_values(sampling_array[i])
            data_list[i].transform_list_to_string()
         
        # Latin Hypercube Sampling DONE
        print("CREATE DATAFRAME")
        # create dataframe
        dict_list = []
        for class_object in data_list:
            dict_object = {
                "keyword":class_object.keyword,
                "word":str(class_object.word),
                "values":class_object.value_string
            }
            dict_list.append(dict_object)

        df = pd.DataFrame(dict_list)
        df.to_csv(path+ "/" + name + ".csv")
        print("CSV WRITTEN TO: ", path+"/"+name+".csv")

    else:
        print("Words, Minimums and Maximums have different lenghts")

if __name__ == "__main__":

    KEYWORD = "MAT_BARLAT_YLD2000_TITLE"
    WORDS = ["C", "P"]
    mins = [0.95 * 0.9, 40 * 0.9]
    maxs = [4.626 * 1.1, 147394.015 * 1.1]
    path = "D:\\01_Auswertung_Zugversuch\\sims\\new_sims\\cowper_symonds\\hocket-sherby"
    name = "hocket_sherby"
    number_of_samples = 133
    create_csv(KEYWORD, WORDS, mins, maxs, path, name, number_of_samples)

    KEYWORD = "MAT_BARLAT_YLD2000_TITLE"
    WORDS = ["C", "P"]
    mins = [0.95 * 0.9, 40 * 0.9]
    maxs = [4.626 * 1.1, 147394.015 * 1.1]
    path = "D:\\01_Auswertung_Zugversuch\\sims\\new_sims\\cowper_symonds\\swift"
    name = "swift"
    number_of_samples = 133
    create_csv(KEYWORD, WORDS, mins, maxs, path, name, number_of_samples)

    KEYWORD = "MAT_BARLAT_YLD2000_TITLE"
    WORDS = ["C", "P"]
    mins = [0.95 * 0.9, 40 * 0.9]
    maxs = [4.626 * 1.1, 147394.015 * 1.1]
    path = "D:\\01_Auswertung_Zugversuch\\sims\\new_sims\\cowper_symonds\\voce"
    name = "voce"
    number_of_samples = 133
    create_csv(KEYWORD, WORDS, mins, maxs, path, name, number_of_samples)