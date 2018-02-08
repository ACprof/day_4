'''
Created on 2018 M02 8

@author: Nuno
'''

from urllib.error import HTTPError
import os
import sys

from Bio import Entrez, SeqIO


if __name__ == '__main__':

    # show arguments
    print(sys.argv)

    if (len(sys.argv) != 2):
        print("usage: {} <file id>".format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    # get id from command line
    id_by_arg = sys.argv[1]
    try:
        Entrez.email = "acprof@gmail.com"
        handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
                               id=id_by_arg)
    except HTTPError as e:
        print("Error: {}".format(e.msg))
        sys.exit(1)

    lst_seq_record = SeqIO.read(handle, "gb")
    print("#sequences: {}".format(len(lst_seq_record)))
    with open("{}.gb".format(id_by_arg), "w") as handle_out:
        SeqIO.write(lst_seq_record, handle_out, "gb")

    print("File saved: {}.gb".format(id_by_arg))
