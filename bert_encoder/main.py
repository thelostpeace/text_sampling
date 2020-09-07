import sys
from model import BertSentenceEncoder
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import argparse
from torch.utils.data import DataLoader
import time
from tools.data_loader import build_vocab, build_label
from tools.data_loader import load_vocab
from tools.data_loader import TextDataSet
from torch.utils.tensorboard import SummaryWriter
import os, glob, shutil
from pytorch_model_summary import summary
from transformers import BertConfig
from transformers import BertTokenizer
from transformers import get_linear_schedule_with_warmup
from transformers import AdamW

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# set model
bert_config_file = 'bert_config.json'
bert_model_file = 'pytorch_model.bin'
bert_config = BertConfig.from_json_file(bert_config_file)
bert_config.output_hidden_states = False
bert_config.return_dict = True
bert_config.output_attentions = False
#print(bert_config)
model = BertSentenceEncoder.from_pretrained(bert_model_file, config=bert_config)
model.to(device)
# bert tokenizer
vocab_file = 'vocab.txt'
tokenizer = BertTokenizer(vocab_file=vocab_file, do_lower_case=True)

max_length = 32
batch_size = 1024

def generate_batch(batch):
    # TextDataSet yield one line contain label and input
    input_ids, attention_masks = [], []
    for data in batch:
        num_input = []
        sentence = data.split('\t')[1]
        encoded_dict = tokenizer.encode_plus(tokenizer.tokenize(sentence), max_length=max_length, pad_to_max_length=True, return_tensors='pt')
        input_ids.append(encoded_dict["input_ids"])
        attention_masks.append(encoded_dict["attention_mask"])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    return input_ids.to(device), attention_masks.to(device)

def batch_encoding(input_ids, output, encoding):
    output = output.cpu().numpy()
    input_ids = input_ids.cpu().numpy()
    for idx in range(len(output)):
        sent = tokenizer.decode(input_ids[idx]).replace(' ', '').replace('[PAD]', '').replace("[CLS]", '').replace('[SEP]', '')
        encoding[sent] = output[idx]

def sentence_encoding(textfile):
    test_dataset = TextDataSet(textfile)
    data = DataLoader(test_dataset, batch_size=batch_size, collate_fn=generate_batch)
    encoding = dict()
    for i, (input_ids, attention_mask) in enumerate(data):
        with torch.no_grad():
            output = model(input_ids, attention_mask)
            batch_encoding(input_ids, output[1], encoding)

    return encoding

if __name__ == "__main__":
    sentence_file = "new_all.txt"
    encoding = sentence_encoding(sentence_file)

    with open("sentence.encoding", "w+") as f:
        for enc in encoding:
            f.write("%s\t%s\n" % (enc, ' '.join([str(i) for i in encoding[enc]])))
