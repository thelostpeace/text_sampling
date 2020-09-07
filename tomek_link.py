#!/usr/bin/env python
from imblearn.under_sampling import TomekLinks
import numpy as np

encoding_file = "bert_encoder/sentence.encoding"

data = dict()
with open(encoding_file) as f:
    for line in f:
        segs = line.strip().split('\t')
        data[segs[0]] = np.array([float(d) for d in segs[1].split()])

datafile = "bert_encoder/new_all.txt"
label2id = {"sys_yes":0, "sys_no":1, "chitchat":2}
labels = dict()
text2label = dict()
with open(datafile) as f:
    for line in f:
        segs = line.strip().split('\t')
        labels[segs[1]] = label2id[segs[0]]
        text2label[segs[1]] = segs[0]

x = np.empty(shape=(768,))
y = np.array([])

text = []
with open(encoding_file) as f:
    for line in f:
        segs = line.strip().split('\t')
        x = np.vstack((x, np.array([float(d) for d in segs[1].split()])))
        y = np.concatenate((y, [labels[segs[0]]]))
        text.append(segs[0])

tl = TomekLinks(n_jobs=24, sampling_strategy='not minority')
x_res, y_res = tl.fit_resample(x[1:], y)

new_text = [text[i] for i in tl.sample_indices_]

with open("sampling.txt", "w+") as f:
    for q in new_text:
        f.write("%s\t%s\n" % (text2label[q], q))
