# -*- coding:utf-8 -*-
import sys
sys.path.append('tools/protocols')
from common.ttypes import *
from protocols.la.ttypes import *
from protocols.la import LAService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import os
pwd = os.getcwd()
os.environ["NLTK_DATA"] = os.path.join(pwd, "contrib/nltk_data")
from nltk.tokenize import word_tokenize

class Tokenizer:
    '''
        对于中文字符，两边加空格，tokenize用nltk的tokenizer
    '''
    def __init__(self):
        '''
            ascii_valid will stay in sequence
            ascii_invalid will be erased and treated as delimeter
            we list all cjk except cjk compatibility and cjk radicals/kangxi radicals
            for chinese tokenization we just use Han and cjk punctuation
        '''
        self.tokenizer = word_tokenize
        self.han_begin = "\u4e00"
        self.han_end = "\u9fff"
        self.cjk_ea_begin = "\u3400"
        self.cjk_ea_end = "\u4dbf"
        self.cjk_eb_begin = "\u0002\u0000"
        self.cjk_eb_end = "\u0002\ua6df"
        self.cjk_ec_begin = "\u0002\ua700"
        self.cjk_ec_end = "\u0002\ub73f"
        self.cjk_ed_begin = "\u0002\ub740"
        self.cjk_ed_end = "\u0002\ub81f"
        self.cjk_ee_begin = "\u0002\ub820"
        self.cjk_ee_end = "\u0002\uceaf"
        self.cjk_ef_begin = "\u0002\uceb0"
        self.cjk_ef_end = "\u0002\uebe0"
        self.cjk_eg_begin = "\u0003\u0000"
        self.cjk_eg_end = "\u0003\u134a"
        self.cjk_punc_begin = "\u3000"
        self.cjk_punc_end = "\u303f"
        self.cjk_punc_comp_begin = "\ufe30"
        self.cjk_punc_comp_end = "\ufe4f"
        self.cjk_punc_half_full_begin = "\uff00"
        self.cjk_punc_half_full_end = "\uffef"
        self.cjk_symbol_begin = "\u3200"
        self.cjk_symbol_end = "\u32ff"
        self.cjk_symbol_comp_begin = "\u3300"
        self.cjk_symbol_comp_end = "\u33ff"

    def tokenize(self, s):
        seq = ""
        for c in s:
            if (c >= self.han_begin and c <= self.han_end) or (c >= self.cjk_punc_begin and c <= self.cjk_punc_end) or (c >= self.cjk_punc_comp_begin and c <= self.cjk_punc_comp_end) or (c >= self.cjk_punc_half_full_begin and c <= self.cjk_punc_half_full_end):
                seq += " " + c + " "
            else:
                seq += c

        return self.tokenizer(seq)

class LATokenizer:
    '''
        LA tokenizer
    '''
    def __init__(self):
        self.server = "not provided"
        self.port = 11111
        transport = TSocket.TSocket(self.server, self.port)
        self.transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = LAService.Client(protocol)

    def tokenize(self, query):
        self.transport.open()
        request = LARequest()
        request.query = query
        request.user_info = UserInfo()
        request.user_info.key = "test_key"
        request.user_info.query_id = "test_queryid"
        request.user_info.device_id = "test_deviceid"
        request.parse_time_switch = 0

        response = self.client.process(request)
        self.transport.close()

        tokens = []
        for token in response.tokens:
            tokens.append(token.term)

        return tokens


'''
if __name__ == '__main__':
    tokenizer = Tokenizer()
    s = "今天A股上升了1.2%。"
    print(tokenizer.tokenize(s))
'''
