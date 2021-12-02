#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import random
class Encrypt:
    def __init__(self, input_mes, one_time_pad):
        self.input_mes = input_mes
        self.ref_genome = one_time_pad
        
        
        # use the random dict generated before
        with open('Ranhex_to_codon_dict.json','r') as file_object:  
            self.hex_to_codon_dict = json.load(file_object) 

        with open('Rancodon_to_hex_dict.json','r') as file_object:  
            self.codon_to_hex_dict = json.load(file_object) 

        with open('allRancodon_to_number_dict.json','r') as file_object:  
            self.codon_to_numbers_dict = json.load(file_object) 
            
        with open('allRannumber_to_codon_dict.json','r') as file_object:  
            self.numbers_to_codon_dict = json.load(file_object) 
    
    # take unicode str and convert it to hex str       
    def unicode_to_hex(self):
        self.byte_string = self.input_mes.encode('utf8')
        self.hex_string = self.byte_string.hex()
        return self.hex_string
    
    #take hex str and convert it to a list of codons       
    def hex_to_codons(self):
        self.hex_to_codons_output_list = []
        for i in range (len(self.hex_string)):
            messages = self.hex_string[i]
            if messages in self.codon_to_hex_dict: 
                codons = self.codon_to_hex_dict[messages]
                self.hex_to_codons_output_list.append(codons)
            else:
                print('False')
                return False
        return self.hex_to_codons_output_list
    
    # convert list of codons to list of numbers
    def codon_to_numbers(self,list_of_codon):
        self.codon_to_numbers_output_list = []
        for codon in list_of_codon:
            if codon in self.numbers_to_codon_dict:
                numbers = self.numbers_to_codon_dict[codon]
                self.codon_to_numbers_output_list.append(numbers)
            else:
                return False
        return self.codon_to_numbers_output_list
    
    # convert list of numbers to list of codons
    def numbers_to_codon(self,list_of_numbers):
        self.numbers_to_codon_output_list = []
        for number in list_of_numbers:
            number = str(number)
            if number in self.codon_to_numbers_dict:
                codon = self.codon_to_numbers_dict[number]
                self.numbers_to_codon_output_list.append(codon)
            else:
                print('Incorrect conversion of numbers and codon')
                return False
        return self.numbers_to_codon_output_list
    
    # turn the list of coded seq into a string
    def list_to_string(self,a_list):
        self.list_to_string_output = ''
        for i in range (len(a_list)):
            self.list_to_string_output =  self.list_to_string_output + a_list[i]
        return self.list_to_string_output

    #turn a string into a list
    def string_to_list(self,a_string):
        a_string = a_string.lower()
        self.string_to_list_output_list = []
        n = 0
        #check length of the str must be a multiple of 2
        if (len(a_string)%2)== 0:
            while n <= (len(a_string)-2):
                a_group = a_string[n:n+2]
                self.string_to_list_output_list.append(a_group)
                n = n+2
        else:
            print('The file is broken')
            return False
        return self.string_to_list_output_list
    
    # take one_time_pad and encrypt the input_mes, return a list of numbers
    def encrypt_message(self):
        #turn ref genome str into a list correspond to the message codon list
        self.ref_genome = self.ref_genome.lower()
        self.ref_list = []
        i = 1
        while i <= len(self.hex_to_codons_output_list):
            bases = self.ref_genome[:2]
            self.ref_list.append(bases)
            i = i+1
            self.ref_genome = self.ref_genome[2:]
        #assign each value in the target a ref val
        list_message_n = self.codon_to_numbers(self.hex_to_codons_output_list)
        list_pad_n = self.codon_to_numbers(self.ref_list)
        #ref genome has to be in lower case
        list_combined =[]
        self.list_encrypted = []
        for i in range(len(self.hex_to_codons_output_list)):
            combine = list_message_n[i] + list_pad_n[i]
            list_combined.append(combine)
        for item in list_combined:
            item = item % 16
            self.list_encrypted.append(item)
        return self.list_encrypted
    
    # Checksum val (encode part)
    #generate the checksum
    def get_checksum(self,list_codons):
        self.checksum_val = 0
        for codon in list_codons:
            self.checksum_val = self.checksum_val + self.numbers_to_codon_dict[codon]
        self.checksum_val = self.checksum_val%16
        return self.checksum_val

    #turn checksum value to codons
    def checksum_to_codons(self):
        self.checksum_val = str(self.checksum_val)
        self.checksum_append_codon = self.codon_to_numbers_dict[self.checksum_val]
        return self.checksum_append_codon

    #add checksum codon to the target seq
    def add_checksum_codon(self,DNA_seq_str):
        self.DNA_seq_str = DNA_seq_str + self.checksum_append_codon.upper()
        return self.DNA_seq_str
    
    # Extension1
    # add tags, insert into random DNA library

    #generate a random arbitary DNA paragraph
    def generate_random_DNA(self,random_length = 500):
        self.random_seq = ''
        for i in range(random_length):
            self.random_seq += random.choice(['A','T','C','G'])
        return self.random_seq

    #insert a seq into a random pos of random seq
    def insert_random_seq(self,inserted_seq_str):
        #generate a random DNA seq
        host = self.generate_random_DNA()
        #generate a random pos
        insert_pos = random.randint(0,len(host))
        #insert the target seq into the random pos
        self.after_insertion = host[:insert_pos] + inserted_seq_str + host[insert_pos:]
        return self.after_insertion

    #add tags(at the begining and the end) of the encoded DNA seq 
    def add_tags(self):
        self.DNA_seq_str = 'ATCGATCGATCG'+self.DNA_seq_str +'GCATGCATGCAT'
        return self.DNA_seq_str
    
    # The final encode function that takes input_mes, ref_genome, and generates the file.
    def encode(self):
        encoded_mes = self.unicode_to_hex()
        encoded_mes = self.hex_to_codons()
        if encoded_mes != False:
            encoded_mes = self.encrypt_message()
            encoded_mes = self.numbers_to_codon(encoded_mes)
            #add a checksum val
            #DNA_seq_str = 'Tag'+DNA_seq_str + 'checksum' + 'Tag' 
            checksum_val = self.get_checksum(encoded_mes)
            checksum_codon = self.checksum_to_codons()
            encoded_mes = self.list_to_string(encoded_mes)
            encoded_mes = encoded_mes.upper()
            after_checksum = self.add_checksum_codon(encoded_mes)
            # add tags to the encoded_mes
            after_checksum = self.add_tags()
            final_mes = self.insert_random_seq(after_checksum) 
            #save DNA str into a text file 
            f = open('class_encoded.txt','w')
            f.write(final_mes)
            f.close()
            print('The encoded DNA is stored in: class_encoded.txt')
            return 'class_encoded.txt'


# In[ ]:


import json
import random
class Decrypt:
    def __init__(self, filename, one_time_pad):
        self.filename = filename
        self.ref_genome = one_time_pad
        
        
        # use the random dict generated before
        with open('Ranhex_to_codon_dict.json','r') as file_object:  
            self.hex_to_codon_dict = json.load(file_object) 

        with open('Rancodon_to_hex_dict.json','r') as file_object:  
            self.codon_to_hex_dict = json.load(file_object) 

        with open('allRancodon_to_number_dict.json','r') as file_object:  
            self.codon_to_numbers_dict = json.load(file_object) 
            
        with open('allRannumber_to_codon_dict.json','r') as file_object:  
            self.numbers_to_codon_dict = json.load(file_object) 
            
    def extract_file(self):
        f = open(self.filename,'r')
        self.import_string = f.read()
        return self.import_string
    
    def find_start_tag(self):
        self.pos = 0
        while self.pos < len(self.import_string):
            if self.import_string[self.pos:self.pos+12] == 'ATCGATCGATCG':
                return self.pos
            self.pos = self.pos+1
        return False

    def find_stop_tag(self):
        self.start_pos = self.pos
        while self.start_pos < len(self.import_string):
            if self.import_string[self.start_pos:self.start_pos+12] == 'GCATGCATGCAT':
                return self.start_pos
            self.start_pos = self.start_pos + 1
        return False

    def target_region(self):
        start_pos = self.find_start_tag()
        if start_pos == False:
            return False
        else:
            stop_pos = self.find_stop_tag()
            if stop_pos == False:
                return False
            else:
                self.region = self.import_string[(start_pos+12):stop_pos]
                return self.region         
            
    # convert list of codons to list of numbers
    def codon_to_numbers(self,list_of_codon):
        self.codon_to_numbers_output_list = []
        for codon in list_of_codon:
            if codon in self.numbers_to_codon_dict:
                numbers = self.numbers_to_codon_dict[codon]
                self.codon_to_numbers_output_list.append(numbers)
            else:
                return False
        return self.codon_to_numbers_output_list
    
    # convert list of numbers to list of codons
    def numbers_to_codon(self,list_of_numbers):
        self.numbers_to_codon_output_list = []
        for number in list_of_numbers:
            number = str(number)
            if number in self.codon_to_numbers_dict:
                codon = self.codon_to_numbers_dict[number]
                self.numbers_to_codon_output_list.append(codon)
            else:
                print('Incorrect conversion of numbers and codon')
                return False
        return self.numbers_to_codon_output_list
    
    # turn the list of coded seq into a string
    def list_to_string(self,a_list):
        self.list_to_string_output = ''
        for i in range (len(a_list)):
            self.list_to_string_output =  self.list_to_string_output + a_list[i]
        return self.list_to_string_output

    #turn a string into a list
    def string_to_list(self,a_string):
        a_string = a_string.lower()
        self.string_to_list_output_list = []
        n = 0
        #check length of the str must be a multiple of 2
        if (len(a_string)%2)== 0:
            while n <= (len(a_string)-2):
                a_group = a_string[n:n+2]
                self.string_to_list_output_list.append(a_group)
                n = n+2
        else:
            print('The file is broken')
            return False
        return self.string_to_list_output_list
    
    def get_checksum(self,list_codons):
        self.checksum_val = 0
        for codon in list_codons:
            self.checksum_val = self.checksum_val + self.numbers_to_codon_dict[codon]
        self.checksum_val = self.checksum_val%16
        return self.checksum_val
    
    # receive checksum and compare
    def compare_checksum(self):
        target_list = self.string_to_list(self.region)
        codon_checksum = target_list[-1]
        checksum0 = self.numbers_to_codon_dict[codon_checksum]
        checksum1 = self.get_checksum(target_list[:-1])%16
        if checksum0 == checksum1:
            return True
        else:
            return False
        
    #decode the encrypted from a list of codons
    def decrypt_message(self,codon_list):
        self.ref_genome = self.ref_genome.lower()
        codon_list_n = self.codon_to_numbers(codon_list)
        ref_list =[]
        substracted_list = []
        self.decrypted_n_list =[]
        i = 1
        p = 0
        while i <= len(codon_list_n):
            bases = self.ref_genome[:2]
            ref_list.append(bases)
            i = i+1
            self.ref_genome = self.ref_genome[2:]
        ref_list_n = self.codon_to_numbers(ref_list)
        #with 2 lists, retrieve the original message codon
        while p < len(codon_list_n):
            substracted = codon_list_n[p] -ref_list_n[p]
            substracted_list.append(substracted)
            p = p+1
        for item in substracted_list:
            item = item % 16
            self.decrypted_n_list.append(item)
        return self.decrypted_n_list
    
    def codons_to_hex(self,list_of_codons):
        self.codons_to_hex_output_list = []
        for i in range (len(list_of_codons)):
            codon = list_of_codons[i]
            if codon in self.hex_to_codon_dict: 
                hex_val = self.hex_to_codon_dict[codon]
                self.codons_to_hex_output_list.append(hex_val)
            else:
                print('Invalid file')
                return False
        return self.codons_to_hex_output_list
    
    def hex_to_unicode(self,decoded_mes):
        # decoded_mes has to be str
        byte_string = bytes.fromhex(decoded_mes)
        self.unicode_string = byte_string.decode("utf8")
        return self.unicode_string
    
    def decode(self):
        decoded_mes = self.extract_file()
        decoded_mes = self.target_region()
        # check checksum val
        results = self.compare_checksum()
        print('The result of the checksum test is:',results)
        if results == True:
            decoded_mes = decoded_mes[:-2]
            decoded_mes = self.string_to_list(decoded_mes)
            decrypt_mes = self.decrypt_message(decoded_mes)
            decrypt_mes = self.numbers_to_codon(decrypt_mes)
            decrypt_mes = self.codons_to_hex(decrypt_mes)
            decrypt_mes = self.list_to_string(decrypt_mes)
            decrypt_mes = self.hex_to_unicode(decrypt_mes)
            print("The coded message is: "+ decrypt_mes)
            self.unicode_string = decrypt_mes
        return self.unicode_string

