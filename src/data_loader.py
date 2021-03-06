# data loader related functions.
import os
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm


def load_pairs(file_name):
    f = open(file_name, "r")
    body = f.read()
    body = body.split("\n")

    wid_pairs = []
    for i in range(len(body)):
        try:
            a, b, c = body[i].split(" ")
            wid_pairs.append([int(a), int(b), int(c)])
        except:
            pass
    f.close()

    return wid_pairs

def load_emb_matrix(npydir):
    return np.load(npydir)

def load_dictionary(pklfile):
    f = open(pklfile, "rb")
    dict_load = pickle.load(f)

    return dict_load

def generate_pairs(directory, batch_size):
    '''
    Generate pair of concept for batch trainining
    -- directory: directory contain 
    -- batch size: number of pairs in each batch
    -- concept_dictionary: conceptid to emb id mapping
    -- return : a batch of traininig samples
    '''

    i = 0
    file_list = os.listdir(directory)
    pairs = load_pairs(file_list[i])
    c = 0

    while (True):

        X_batch = [[], []]
        Y_batch = []
        if (i == len(file_list)):
            i = 0

        if ((len(pairs) - c) < batch_size):
            rest_num = len(pairs) - c
            for j in range(rest_num):
                sample = pairs[c+j]
                pair_content1 = sample[0]
                pair_content2 = sample[1]
                label = sample[2]

                X_batch[0].append(pair_content1)
                X_batch[1].append(pair_content2)
                Y_batch.append(label)

            i += 1
            c = 0
            if (i != len(file_list)):
                pairs = load_pairs(file_list[i])

                for t in range(batch_size - rest_num):
                    sample = pairs[c]
                    c += 1

                    pair_content1 = sample[0]
                    pair_content2 = sample[1]
                    label = sample[2]

                    X_batch[0].append(pair_content1)
                    X_batch[1].append(pair_content2)
                    Y_batch.append(label)
            else:
                pass

            X_batch[0] = np.array(X_batch[0])
            X_batch[1] = np.array(X_batch[1])
            Y_batch = np.array(Y_batch)

            yield [X_batch[0], X_batch[0], X_batch[1], X_batch[1]], Y_batch

        else:
            for k in range(batch_size):
                sample = pairs[c]
                c += 1
                pair_content1 = sample[0]
                pair_content2 = sample[1]
                label = sample[2]

                X_batch[0].append(pair_content1)
                X_batch[1].append(pair_content2)
                Y_batch.append(label)

            X_batch[0] = np.array(X_batch[0])
            X_batch[1] = np.array(X_batch[1])
            Y_batch = np.array(Y_batch)

            yield [X_batch[0], X_batch[0], X_batch[1], X_batch[1]], Y_batch


def build_weight_matrix(npy):
    '''
    build weight matrix for training from npy
    -- npy: a npy file contain weight matrix
    -- return: list of wieghted matrix
    '''

    weight_matrix = np.load(npy)
    weight_matrix_expand = np.zeros((weight_matrix.shape[0]+1, 128))
    for i in range(weight_matrix.shape[0]):
        weight_matrix_expand[i+1] = weight_matrix[i]

    return weight_matrix_expand

def load_train_data(data_dir):
    with open(data_dir, "r") as f:
        body = f.read()
    body = body.split("\n")
    
    mylist = []
    for i in tqdm(range(len(body))):
        str_list = body[i].split(",")
        int_list = [int(c) for c in str_list]
        mylist.append(int_list)
    
    return mylist