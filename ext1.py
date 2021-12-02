#!/usr/bin/env python
# coding: utf-8

# In[1]:


#generate 4bases codons(list)

dna_bases = ['a','t','c','g']
codon_list_4base = []
for base1 in dna_bases:
    for base2 in dna_bases:
        for base3 in dna_bases:
            for base4 in dna_bases:
                codon = base1 + base2 + base3 + base4
                codon_list_4base.append(codon)
                
#generate a list of ACSII
ASCII_list = []
for i in range (0,256):
    ASCII_list.append(chr(i))
    
#generate conversion dict
ASCII_to_codon_dict = dict(zip(codon_list_4base,ASCII_list))
codon_to_ASCII_dict = dict(zip(ASCII_list,codon_list_4base))

#basic convert functions
def ASCII_to_codons(allowable_input):
    output_list = []
    for i in range (len(allowable_input)):
        messages = allowable_input[i]
        if messages in codon_to_ASCII_dict: 
            codons = codon_to_ASCII_dict[messages]
            output_list.append(codons)
        else:
            print('Invalid input')
            return False
    return output_list
    

def codons_to_ASCII(list_of_codons):
    output_list = []
    for codon in list_of_codons:
        if codon in ASCII_to_codon_dict:
            messages = ASCII_to_codon_dict[codon]
            output_list.append(messages)
        else:
            print('Unacceptable values, please check')
            return None
    return output_list

def list_to_string(a_list):
    final_output = ''
    for i in range (len(a_list)):
        final_output = final_output + a_list[i]
        #final_output = final_output.upper()
    return final_output

#turn a string into a list
def string_to_list(a_string):
    a_string = a_string.lower()
    final_output_list = []
    n = 0
    #check length of the str must be a multiple of 4
    if (len(a_string)%4)== 0:
        while n <= (len(a_string)-4):
            a_group = a_string[n:n+4]
            final_output_list.append(a_group)
            n = n+4
    else:
        print('The file is broken')
        return False
    return final_output_list

import random

#generate a random arbitary DNA paragraph
def generate_random_DNA(random_length):
    random_seq = ''
    for i in range(random_length):
        random_seq += random.choice(['A','T','C','G'])
    return random_seq

#insert a seq into a random pos of random seq
def insert_random_seq(inserted_seq_str,length_of_random_DNAlibrary):
    #generate a random DNA seq
    host = generate_random_DNA(length_of_random_DNAlibrary)
    #generate a random pos
    insert_pos = random.randint(0,len(host))
    #insert the target seq into the random pos
    after_insertion = host[:insert_pos] + inserted_seq_str + host[insert_pos:]
    return after_insertion

#add tags(at the begining and the end) of the encoded DNA seq 
def add_tags(DNA_seq_str):
    DNA_seq_str = 'ATCGATCGATCG'+DNA_seq_str +'GCATGCATGCAT'
    return DNA_seq_str
    
#remove tags when decoding
def remove_tags(codon_list):
    del codon_list[:3]
    del codon_list[-3:]
    return codon_list

# find the target seq in a random library
# similar to find_start_codon function

def find_start_tag (import_string):
    pos = 0
    while pos < len(import_string):
        if import_string[pos:pos+12] == 'ATCGATCGATCG':
            return pos
        pos = pos+1
    return False

def find_stop_tag(import_string, pos):
    start_pos = pos
    while start_pos < len(import_string):
        if import_string[start_pos:start_pos+12] == 'GCATGCATGCAT':
            return start_pos
        start_pos = start_pos + 1
    return False

def target_region (import_string):
    start_pos = find_start_tag(import_string)
    if start_pos == False:
        return False
    else:
        stop_pos = find_stop_tag(import_string,start_pos) 
        if stop_pos == False:
            return False
        else:
            region = import_string[(start_pos+12):stop_pos]
            return region       

def ext1_encode(message):
    encoded_mes = ASCII_to_codons(message)
    if encoded_mes != False:
        encoded_mes = list_to_string(encoded_mes)
        encoded_mes = encoded_mes.upper()
        # add tags to the encoded_mes
        encoded_mes = add_tags(encoded_mes)
        after_insert_mes = insert_random_seq(encoded_mes, 500) 
        #the length of the random seq is by default 500
        f = open('ext1_encoded.txt','w')
        f.write(after_insert_mes)
        f.close()
        print('The encoded DNA is stored in: ext1_encoded.txt')
        return 'ext1_encoded.txt'
    
def ext1_decode(filename):
    f = open(filename,'r')
    all_text = f.read()
    #find the target region
    target_mes = target_region(all_text)
    target_mes = string_to_list(target_mes)
    decoded_mes = codons_to_ASCII(target_mes)
    decoded_mes = list_to_string(decoded_mes)
    print("The coded message is: "+ decoded_mes)
    return decoded_mes
    

