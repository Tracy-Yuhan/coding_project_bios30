#!/usr/bin/env python
# coding: utf-8

# In[4]:


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

# Fun1
# Encode a text mes into DNA seq using codons of 4 bases
# Input- text mes(str), Output- codons(str)

def fun_1(message):
    encoded_mes = ASCII_to_codons(message)
    if encoded_mes != False:
        encoded_mes = list_to_string(encoded_mes)
        encoded_mes = encoded_mes.upper()
        print(encoded_mes)
        return encoded_mes

# Fun 2
# decode a DNA seq and extract the stored mes

def fun_2(DNA_str):
    codon_lists = string_to_list(DNA_str)
    decoded_mes = codons_to_ASCII(codon_lists)
    decoded_mes = list_to_string(decoded_mes)
    print("The coded message is: "+ decoded_mes)
    return decoded_mes

# Fun 3
# take a str and save the encoded DNA mes str to a text file on disk

def fun_3(encoded_DNA_str):
    f = open('basic_version_encoded.txt','w')
    f.write(encoded_DNA_str)
    f.close()
    print('The encoded DNA is stored in: basic_version_encoded.txt')
    return 'basic_version_encoded.txt'

# Fun 4
# load and decode a text file containing a DNA

def fun_4(filename):
    f = open(filename,'r')
    all_text = f.read()
    print('file has been received')
    return all_text

