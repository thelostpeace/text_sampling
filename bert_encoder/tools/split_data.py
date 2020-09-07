import argparse
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tokenize data")
    parser.add_argument('--input', type=str, required=True, help='input file')
    parser.add_argument('--output', type=str, required=True, help='output dir')
    parser.add_argument('--split_ratio', type=list, help='split_ratio', default=[0.8, 0.1, 0.1])
    args = parser.parse_args()

    domain_sample = dict()
    with open(args.input) as rf:
        for line in rf:
            line = line.strip()
            info = line.split('\t')
            if info[0] not in domain_sample:
                domain_sample[info[0]] = []
            domain_sample[info[0]].append(line)

    train, dev, test = [], [], []
    for _, sample in domain_sample.items():
        random.shuffle(sample)
        idx1 = int(len(sample) * args.split_ratio[0])
        idx2 = int(len(sample) * (args.split_ratio[0] + args.split_ratio[1]))
        train.extend(sample[:idx1])
        dev.extend(sample[idx1:idx2])
        test.extend(sample[idx2:])

    random.shuffle(train)
    random.shuffle(dev)
    random.shuffle(test)

    output_name = ['train', 'dev', 'test']
    output_data = [train, dev, test]
    for name, data in zip(output_name, output_data):
        with open("%s/%s.txt" % (args.output, name), "w+") as f:
            f.write("\n".join(data))
