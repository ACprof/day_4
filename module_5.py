'''
Created on 2018 M02 8

@author: Nuno
'''

import os
import re
import sys

from Bio import SeqIO

import utils


class GetSeq():

    dict = {"N": "[ACTG]", "R": "[AG]", "Y": "[CT]"}

    def __init__(self, pattern_1, pattern_2):
        self.pattern_1 = self.get_expansion_bases(pattern_1)
        self.pattern_2 = self.get_expansion_bases(pattern_2)
        self.re_pattern_1 = re.compile(self.pattern_1)
        self.re_pattern_2 = re.compile(self.pattern_2)
#        self.re_pattern_1_rever_comp = re.compile(self.get_expansion_bases(pattern_1, True))
#        self.re_pattern_2_rever_comp = re.compile(self.get_expansion_bases(pattern_2, True))

    def get_expansion_bases(self, seq, b_reverse_complement=False):
        sz_return = ""
        for base in seq:
            if (base in self.dict):
                if (b_reverse_complement):
                    sz_return += utils.complement(self, dict[base])
                sz_return += self.dict[base]
            else:
                sz_return += base
        return sz_return

    def get_seq_by_fasta(self, sequence):
        """
        get sequence by pattern
        """
        seq_return = self.__get_seq_by_fasta(sequence)  # forward
        if (seq_return == None):  # Reverse
            return self.__get_seq_by_fasta(utils.reverse(utils.complement(sequence)))
        else:
            return seq_return

    def __get_seq_by_fasta(self, sequence):
        start = -1
        for iter in re.finditer(self.re_pattern_1, sequence):
            start = iter.end()
            break

        end = 1
        for iter in re.finditer(self.re_pattern_2, sequence):
            end = iter.start()
            break

        if (start != -1 and end != -1 and start < end):
            return sequence[start: end]

        return None


if __name__ == '__main__':

    print(sys.argv)

    if(len(sys.argv) != 5):
        print("Usage: {} <pattern_1> <pattern_2> <in> <out>".format(
            os.path.basename(sys.argv[0])))
        sys.exit(0)

    pattern_1 = sys.argv[1]
    pattern_2 = sys.argv[2]
    file_in = sys.argv[3]
    file_out = sys.argv[4]

    # test if files exists
    if (not os.path.exists(file_in)):
        print("Error: file does not exists " + file_in)
        sys.exit(1)

    get_seq = GetSeq(pattern_1, pattern_2)
    dict_result = {}
    n_count_seq = 0
    with open(file_in, "r") as handle_in:
        for seq_record in SeqIO.parse(handle_in, "fasta"):
            n_count_seq += 1
            seq = get_seq.get_seq_by_fasta(
                str(seq_record.seq))
            if (seq == None):
                continue
            if (seq in dict_result):
                dict_result[seq] += 1
            else:
                dict_result[seq] = 1

    print("#sequences {}".format(n_count_seq))
    for key in sorted(dict_result.keys()):
        print("Seq: {}  Len: {}  #: {}".format(
            key, len(key), dict_result[key]))
