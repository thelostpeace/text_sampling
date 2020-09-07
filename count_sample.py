#!/usr/bin/env python

samplefile = 'sampling.txt'

sample_dict = dict()
with open(samplefile) as f:
    for line in f:
        segs = line.strip().split('\t')
        if segs[0] not in sample_dict:
            sample_dict[segs[0]] = 0
        sample_dict[segs[0]] += 1

for k in sample_dict:
    print("%s: %s" % (k, sample_dict[k]))
