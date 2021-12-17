import argparse
import os
import json
import csv
import sys

csv.field_size_limit(sys.maxsize)
train_file = "train.tsv"
dev_file = "dev.tsv"
test_file = "test.tsv"
task = "MNLI"

confidence_level = "0.05"
folder_name_base = "cartography_confidence_"
highest_level = "0.75"

def processData(data_orig_dir, data_filtered_dir):
    original_ids = []
    original_data = {}
    with open(os.path.join(data_orig_dir, train_file)) as f:
        read_tsv = csv.reader(f, delimiter="\t")
        for row in read_tsv:
            original_ids.append(row[0])
            original_data[row[0]] = row
    
    majority_ids = []


    with open(os.path.join(data_filtered_dir, folder_name_base + str(highest_level),task, train_file)) as f:
        read_tsv = csv.reader(f, delimiter="\t")
        for row in read_tsv:
            majority_ids.append(row[0])
    
    negative_ids = []
    for id in original_data:
        if id not in majority_ids:
            negative_ids.append(id)
    
    positive_ids = []
    with open(os.path.join(data_filtered_dir, folder_name_base + str(confidence_level), task, train_file)) as f:
        read_tsv = csv.reader(f, delimiter="\t")
        for row in read_tsv:
            positive_ids.append(row[0])
    
    print(positive_ids[0:10])
    print("*******")
    print(negative_ids[0:10])
    result_builder = list()
    for ids in [[negative_ids,0], [positive_ids,1]]:
        for id in ids[0]:
            try:
                result_builder.append([id, original_data[id][-4], original_data[id][-3], ids[1]])
            except:
                print("Missed ID: ", id)

    with open(os.path.join(data_filtered_dir, "dataset_using_" + str(confidence_level)) + ".tsv", "wt") as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        for row in result_builder:
            tsv_writer.writerow(row)
    
    print("wrote into the file:")
    print(data_filtered_dir, "dataset_using_" + str(confidence_level) + ".tsv")

if __name__ == "__main__":
    print("Running for the task of ", task)
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_orig_dir",
                      required=True,
                      type=os.path.abspath,
                      help="Directory where the original dataset resides")

    parser.add_argument("--data_filtered_dir",
                      required=True,
                      type=os.path.abspath,
                      help="Directory where the filtered dataset resides")

    args = parser.parse_args()

    processData(args.data_orig_dir, args.data_filtered_dir)