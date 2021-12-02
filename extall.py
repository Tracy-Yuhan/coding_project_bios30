#!/usr/bin/env python
# coding: utf-8

# In[40]:


#generate a codon list for hex conversion
dna_bases = ['a','t','c','g']
codon_list_2base = []
for base1 in dna_bases:
    for base2 in dna_bases:
        codon = base1 + base2 
        codon_list_2base.append(codon)
        
#generate a hex list
hex_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

#generate a numerical list
numbers_list = []
for i in range (0,16):
    numbers_list.append(i)
    
import random
import json
#generate random dict
hex_random_list = hex_list.copy()
random.shuffle(hex_random_list)

number_random_list = numbers_list.copy()
random.shuffle(number_random_list)

hex_to_codon_dict = dict(zip(codon_list_2base,hex_random_list))
codon_to_hex_dict = dict(zip(hex_random_list,codon_list_2base))

codon_to_numbers_dict = dict(zip(number_random_list,codon_list_2base))
numbers_to_codon_dict = dict(zip(codon_list_2base,number_random_list))

def codon_to_numbers(list_of_codon):
    output_list = []
    for codon in list_of_codon:
        if codon in numbers_to_codon_dict:
            numbers = numbers_to_codon_dict[codon]
            output_list.append(numbers)
        else:
            return False
    return output_list

def numbers_to_codon(list_of_numbers):
    output_list = []
    for number in list_of_numbers:
        if number in codon_to_numbers_dict:
            number = int(number)
            codon = codon_to_numbers_dict[number]
            output_list.append(codon)
        else:
            return False
    return output_list

def hex_to_codons(allowable_input):
    output_list = []
    for i in range (len(allowable_input)):
        messages = allowable_input[i]
        if messages in codon_to_hex_dict: 
            codons = codon_to_hex_dict[messages]
            output_list.append(codons)
        else:
            print('False')
            return False
    return output_list

def codons_to_hex(allowable_input):
    output_list = []
    for i in range (len(allowable_input)):
        codon = allowable_input[i]
        if codon in hex_to_codon_dict: 
            hex_val = hex_to_codon_dict[codon]
            output_list.append(hex_val)
        else:
            print('Invalid file')
            return False
    return output_list

# turn the list of coded seq into a string
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
    #check length of the str must be a multiple of 2
    if (len(a_string)%2)== 0:
        while n <= (len(a_string)-2):
            a_group = a_string[n:n+2]
            final_output_list.append(a_group)
            n = n+2
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

# Extension 2 checksum
#generate the checksum
def get_checksum(list_codons):
    checksum_val = 0
    for codon in list_codons:
        checksum_val = checksum_val + numbers_to_codon_dict[codon]
    checksum_val = checksum_val%16
    return checksum_val

#turn checksum value to codons
def checksum_to_codons(checksum_val):
    checksum_val = int(checksum_val)
    checksum_append_codon = codon_to_numbers_dict[checksum_val]
    return checksum_append_codon

#add checksum codon to the target seq
def add_checksum_codon(DNA_seq_str, checksum_codon):
    DNA_seq_str = DNA_seq_str + checksum_codon.upper()
    return DNA_seq_str

# receive checksum and compare
def compare_checksum(target_region_output_str):
    target_list = string_to_list(target_region_output_str)
    codon_checksum = target_list[-1]
    checksum0 = numbers_to_codon_dict[codon_checksum]
    checksum1 = get_checksum(target_list[:-1])%16
    if checksum0 == checksum1:
        return True
    else:
        return False

# Extension 3 one-time pad
#taking ref genome and encrypt the target codon list
#ref genome is always longer or equals to the len of message codon list
def encrypt_message(target_codon_list,reference_genome):
    #turn reference genome str into a list correspond to the message codon list
    reference_genome = reference_genome.lower()
    ref_list = []
    i = 1
    while i <= len(target_codon_list):
        bases = reference_genome[:2]
        ref_list.append(bases)
        i = i+1
        reference_genome = reference_genome[2:]
    #assign each value in the target a ref val
    list_message_n = codon_to_numbers(target_codon_list)
    list_pad_n = codon_to_numbers(ref_list)
    #ref genome has to be in lower case
    list_combined =[]
    list_encrypted = []
    for i in range(len(target_codon_list)):
        combine = list_message_n[i] + list_pad_n[i]
        list_combined.append(combine)
    for item in list_combined:
        item = item % 16
        list_encrypted.append(item)
    return list_encrypted
        

#decode the encrypted from a list of codons
def decrypt_message(codon_list, ref_genome):
    ref_genome = ref_genome.lower()
    codon_list_n = codon_to_numbers(codon_list)
    ref_list =[]
    substracted_list = []
    decrypted_n_list =[]
    i = 1
    p = 0
    while i <= len(codon_list_n):
        bases = ref_genome[:2]
        ref_list.append(bases)
        i = i+1
        ref_genome = ref_genome[2:]
    ref_list_n = codon_to_numbers(ref_list)
    
    #with 2 lists, retrieve the original message codon
    while p < len(codon_list_n):
        substracted = codon_list_n[p] -ref_list_n[p]
        substracted_list.append(substracted)
        p = p+1
    for item in substracted_list:
        item = item % 16
        decrypted_n_list.append(item)
    return decrypted_n_list

#store the random dict into json files
filename = 'Ranhex_to_codon_dict.json'         
with open(filename, 'w') as file_object:  
 json.dump(hex_to_codon_dict,file_object) 

filename = 'Rancodon_to_hex_dict.json'         
with open(filename, 'w') as file_object:  
 json.dump(codon_to_hex_dict,file_object) 

filename = 'allRancodon_to_number_dict.json'         
with open(filename, 'w') as file_object:  
 json.dump(codon_to_numbers_dict,file_object)

filename = 'allRannumber_to_codon_dict.json'         
with open(filename, 'w') as file_object:  
 json.dump(numbers_to_codon_dict,file_object)

def extall_encode(message):
    byte_string = message.encode('utf8')
    hex_string=byte_string.hex()
    #covert hex to codons
    encoded_mes = hex_to_codons(hex_string)
    f = open('ref_genome_watermelon_chro1.txt','r')
    reference_genome = f.read()
    reference_genome = reference_genome.replace('\n','')
    if encoded_mes != False:
        encoded_mes = encrypt_message(encoded_mes,reference_genome)
        encoded_mes = numbers_to_codon(encoded_mes)
        #add a checksum val
        #DNA_seq_str = 'Tag'+DNA_seq_str + 'checksum' + 'Tag' 
        checksum_val = get_checksum(encoded_mes)
        checksum_codon = checksum_to_codons(checksum_val)
        encoded_mes = list_to_string(encoded_mes)
        encoded_mes = encoded_mes.upper()
        after_checksum = add_checksum_codon(encoded_mes,checksum_codon)
        # add tags to the encoded_mes
        after_checksum = add_tags(after_checksum)
        final_mes = insert_random_seq(after_checksum, 500) 
        #save DNA str into a text file 
        f = open('extall_encoded.txt','w')
        f.write(final_mes)
        f.close()
        print('The encoded DNA is stored in: extall_encoded.txt')
        return 'extall_encoded.txt'

def extall_decode(filename,reference_genome):
    f = open(filename,'r')
    all_text = f.read()
    target_mes = target_region(all_text)
    #check checksum val
    results = compare_checksum(target_mes)
    print('The result of the checksum test is:',results)
    if results == True:
        target_mes = target_mes[:-2]
        target_mes = string_to_list(target_mes)
        decrypt_mes = decrypt_message(target_mes,reference_genome)
        # number to codons
        decrypt_mes = numbers_to_codon(decrypt_mes)
        decoded_mes = codons_to_hex(decrypt_mes)
        decoded_mes = list_to_string(decoded_mes)
        byte_string = bytes.fromhex(decoded_mes)
        unicode_string = byte_string.decode("utf8")
        print("The coded message is: "+ unicode_string)
        return unicode_string

