from torch.utils import data

def build_vocab(vocab_file, label_save, vocab_save):
    label2id = dict()
    id2label = dict()
    word2id = dict()
    id2word = dict()
    label_idx = 0
    word_idx = 0
    with open(vocab_file) as f:
        for line in f:
            info = line.strip().split('\t')
            label = info[0]
            words = info[1].split()
            if label not in label2id:
                label2id[label] = label_idx
                id2label[label_idx] = label
                label_idx += 1
            for w in words:
                if w not in word2id:
                    word2id[w] = word_idx
                    id2word[word_idx] = w
                    word_idx += 1
    #print("lable size: %d" % len(label2id))
    #print("vocab size: %d" % len(word2id))

    # add special word
    word2id['<BOS>'] = word_idx
    id2word[word_idx] = '<BOS>'
    word2id['<EOS>'] = word_idx + 1
    id2word[word_idx + 1] = '<EOS>'
    word2id['<PAD>'] = word_idx + 2
    id2word[word_idx + 2] = '<PAD>'
    word2id['<UNK>'] = word_idx + 3
    id2word[word_idx + 3] = '<UNK>'

    with open(label_save, "w+") as f:
        for k in sorted(id2label.keys()):
            f.write("%s\n" % id2label[k])

    with open(vocab_save, "w+") as f:
        for k in sorted(id2word.keys()):
            f.write("%s\n" % id2word[k])

def build_vocab_with_morpheme(vocab_file, label_save, vocab_save):
    label2id = dict()
    id2label = dict()
    word2id = dict()
    id2word = dict()
    label_idx = 0
    word_idx = 0
    with open(vocab_file) as f:
        for line in f:
            info = line.strip().split('\t')
            label = info[0]
            words = info[1].split()
            if label not in label2id:
                label2id[label] = label_idx
                id2label[label_idx] = label
                label_idx += 1
            for w in words:
                if w not in word2id:
                    word2id[w] = word_idx
                    id2word[word_idx] = w
                    word_idx += 1
                for morpheme in w:
                    if morpheme not in word2id:
                        word2id[morpheme] = word_idx
                        id2word[word_idx] = morpheme
                        word_idx += 1
    #print("lable size: %d" % len(label2id))
    #print("vocab size: %d" % len(word2id))

    # add special word
    word2id['<BOS>'] = word_idx
    id2word[word_idx] = '<BOS>'
    word2id['<EOS>'] = word_idx + 1
    id2word[word_idx + 1] = '<EOS>'
    word2id['<PAD>'] = word_idx + 2
    id2word[word_idx + 2] = '<PAD>'
    word2id['<UNK>'] = word_idx + 3
    id2word[word_idx + 3] = '<UNK>'
    word2id['<MORPHEME>'] = word_idx + 4
    id2word[word_idx + 4] = '<MORPHEME>'

    with open(label_save, "w+") as f:
        for k in sorted(id2label.keys()):
            f.write("%s\n" % id2label[k])

    with open(vocab_save, "w+") as f:
        for k in sorted(id2word.keys()):
            f.write("%s\n" % id2word[k])

def build_label(vocab_file, label_save):
    label2id = dict()
    id2label = dict()
    label_idx = 0
    with open(vocab_file) as f:
        for line in f:
            info = line.strip().split('\t')
            label = info[0]
            if label not in label2id:
                label2id[label] = label_idx
                id2label[label_idx] = label
                label_idx += 1

    with open(label_save, "w+") as f:
        for k in sorted(id2label.keys()):
            f.write("%s\n" % id2label[k])

def load_vocab(vocab_file):
    idx = 0
    vocab2id = dict()
    id2vocab = dict()
    with open(vocab_file) as f:
        for line in f:
            w = line.strip()
            vocab2id[w] = idx
            id2vocab[idx] = w
            idx += 1

    return vocab2id, id2vocab

def save_vocab(vocab, save_file):
    with open(save_file, 'w+') as f:
        for v in vocab:
            f.write("%s\n" % v)


class TextDataSet(data.Dataset):
    def __init__(self, filename):
        self.data = []
        with open(filename) as f:
            for line in f:
                self.data.append(line.strip())

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)



