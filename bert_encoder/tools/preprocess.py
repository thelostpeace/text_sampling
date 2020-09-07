from tokenizer import Tokenizer
from tokenizer import LATokenizer
import argparse
import sys

def is_python3():
    if sys.version_info[0] == 3:
        return True
    return False


def is_punctuation(s):
    ascii_punc = "!\"#$%&'()*+,-./:;<=>?`~[]\\^_~{|}"
    # cjk punctuation
    if s in ascii_punc or (s >= u"\u3000" and s <= u"\u303f") or (s >= u"\uff00" and s <= u"\uffef") or (s >= u"\ufe30" and s <= u"\ufe4f"):
        return True
    return False

def remove_punctuation(text):
    res = ""
    if is_python3():
        for ch in text:
            if not is_punctuation(ch):
                res += ch
    else:
        for ch in unicode(text, encoding="utf8"):
            if not is_punctuation(ch):
                res += ch

    return res

def parse_data(data, word_tokenize):
    info = data.split('\t')
    if is_python3():
        text = remove_punctuation(info[1])
    else:
        text = remove_punctuation(info[1]).encode("utf8")
    token = word_tokenize(text)

    return "%s\t%s" % (info[0], ' '.join(token))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tokenize data")
    parser.add_argument('--input', type=str, required=True, help='input file')
    parser.add_argument('--output', type=str, required=True, help='output file')
    parser.add_argument('--use_la', action='store_true')
    args = parser.parse_args()

    with open(args.input) as rf:
        with open(args.output, "w+") as wf:
            if args.use_la:
                tokenizer = LATokenizer().tokenize
            else:
                tokenizer = Tokenizer().tokenize

            for line in rf:
                out = parse_data(line.strip(), tokenizer)
                wf.write("%s\n" % out)
