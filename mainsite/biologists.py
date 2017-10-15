#!/usr/bin/env Python
# coding=utf-8



def count_aminoacids(aa):
    freq=[]
    for amino_acid in "ACDEFGHIKLMNPQRSTVWY":
        number = aa.count(amino_acid)
        freq.append(amino_acid+' '+str(number))
    return freq
	
def count_dna(aa):
    freq=[]
    for dna in "ACGT":
        number = aa.count(dna)
        freq.append(dna+' '+str(number))
    return freq
	
def count_rna(aa):
    freq=[]
    for rna in "ACGU":
        number = aa.count(rna)
        freq.append(rna+' '+str(number))
    return freq