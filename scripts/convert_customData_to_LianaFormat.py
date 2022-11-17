#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:21:21 2022

@author: engelhardt
"""
import sys

#TODO: If there is more than one possible uniprot id for a gene name than we basically take a random one
#Problem is, how to decide which one is better?

#Location of CCI database in specific .csf format on file system, e.g. '/home/user/interaction_input_CellChatDB.csv'
m_data=sys.argv[1]

#Location of gene name conversion file on file system
conversion_file=sys.argv[2]

#m_data="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/interaction_input_CellChatDB.csv"
#conversion_file="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/gene_conversion-AH104864.csv"

name_to_id={}

with open(conversion_file) as f:
    for line in f:
        if not(("GENEID" in line) or ("#" in line) ):              
            line=line.rstrip()
            l=line.split("\t")
            key=l[0]
            value=l[1]
            name=l[2]
            
    
            if key in name_to_id:
                name_to_id[l[0]].append(value)
            else:
                a=[]
                a.append(value)
                name_to_id[l[0]]=a
                
#Parse conversion file
uniprot_geneName={}
uniprot_ENSG={}
geneName_uniprot={}
geneName_anyUniprot={}

with open(conversion_file) as f:
    for line in f:
        if not(("GENEID" in line) or ("#" in line) ):           
            line=line.rstrip()
            l=line.split("\t")
            ENSG=l[1]
            NAME=l[2]
            
            UNIPROT_tmp=l[4].split(".")
            UNIPROT_tmp2=UNIPROT_tmp[0].split("-")
            UNIPROT=UNIPROT_tmp2[0]
            
            uniprot_geneName[UNIPROT]=NAME
            uniprot_ENSG[UNIPROT]=ENSG
            if(UNIPROT!="NA"):
                geneName_anyUniprot[NAME]=UNIPROT

mihaela_interactions=[]

with open(m_data) as f:
    for line in f:
        if("interaction_name" not in line):
            line=line.rstrip()
            l=line.split(",")
            a=l[0][1:-1].split("_")
            L=a[0]
            R=a[1]
            
            l_len=0
            r_len=0
            
            if(L in geneName_anyUniprot):
                L_uni=geneName_anyUniprot[L]
                
            if(R in geneName_anyUniprot):
                R_uni=geneName_anyUniprot[R]
               
            # if L in name_to_id:
            #     L_ids=name_to_id[L]
            #     l_len=len(L_ids)
            
            # if R in name_to_id:
            #     R_ids=name_to_id[R]
            #     r_len=len(R_ids)
            
            # #print(l_len,r_len,name_to_id["ACER2"])
            
            # if(l_len>0 and r_len>0):
            #     for L in L_ids:
            #         for R in R_ids:
            #             print(L,R)
                        
            mihaela_interactions.append([[L_uni],[R_uni]])
            
            #print(L_uni,R_uni)
#print(len(mihaela_interactions))
for inter in mihaela_interactions:
    L=inter[0]
    R=inter[1]
    
    if(len(L)==1):
        print(L[0],end="\t")
    else:
        print("COMPLEX:"+"_".join(L),end="\t")
        
    if(len(R)==1):
        print(R[0])
    else:
        print("COMPLEX:"+"_".join(R))
             
