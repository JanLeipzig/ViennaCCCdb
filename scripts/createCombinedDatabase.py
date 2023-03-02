#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:09:06 2022

@author: engelhardt


Internal data structure
Most importantly gene_name source and gene name target in liana format,e.g.
GeneA GeneB
COMPLEX:GeneC_GeneD GeneF

"""

import sys, warnings
import copy

#Functions

def interactionExists(interactions,new):
    #print(new)
    exists=False     
    for inter in interactions:
        L=inter[0]
        R=inter[1]
        if(L==new[0] and R==new[1]):
            exists=True
    return exists

#print("#version 0.1")


##For debugging in spyder
git_dir="/home/engelhardt/bioinf/InterfaceProject/CCI/ViennaCCCdb/"
liana_data=git_dir+"source_databases/liana-db_0.1.7.txt"
cpdb_data=git_dir+"source_databases/cpdb_lianaformat.txt"
mihaela_data=git_dir+"source_databases/customData_lianaformat.txt"

##Uncomment these for productive work
# liana_data=sys.argv[1]
# cpdb_data=sys.argv[2]
# mihaela_data=sys.argv[3]
# conversion_file=sys.argv[4]

#datafiles

#Complete database
all_interactions=[]

#only needed for debugging
all_interactions_liana=[]
all_interactions_cpdb=[]
all_interactions_mihaela=[]
interactions_db={}

#Read in Liana data
liana_interactions={}

with open(liana_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split(" ")
             
            L=l[3][1:-1] #gene name
            R=l[4][1:-1] #gene name
                       
            if("_" in L): #gene name
                #Ligand is complex
                L=L.split("_")
                L.sort()
            else:
            #Ligand is not complex 
                L=[L]
                
            if("_" in R): #gene name
                #Receptor is complex
                R=R.split("_")
                R.sort()
            else:
            #Receptor is not complex 
                R=[R]
                  
            all_interactions.append([L,R])
            all_interactions_liana.append([L,R])
            
            #Store the source database for each interaction in an additional dictionary
            L_str="_".join(L)
            R_str="_".join(R)
            
            interactions_db[L_str+"-"+R_str]="Liana_v0.1.7"
            
#Read in cpdb data
with open(cpdb_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split("\t")
            L=l[0]
            R=l[1]
                                   
            #if("COMPLEX" in L):
            if("_" in L):
                #Ligand is complex
                #L=L[8:]
                L=L.split("_")
                L.sort()
                
            else:
            #Ligand is not complex 
                L=[L]
                
            #if("COMPLEX" in R):
            if("_" in R):
                #Receptor is complex
                #R=R[8:]
                R=R.split("_")
                R.sort()

            else:
            #Receptor is not complex
                R=[R]                           
             
            all_interactions_cpdb.append([L,R])

            if(interactionExists(all_interactions, [L,R])==False):
                all_interactions.append([L,R]) 
                
            #Access the source database for each interaction
            L_str="_".join(L)
            R_str="_".join(R)
      
            if(L_str+"-"+R_str in interactions_db):
                interactions_db[L_str+"-"+R_str]+="/Cpdb_v4"
            else:
                interactions_db[L_str+"-"+R_str]="Cpdb_v4"

        

liana_cpdb_number=len(all_interactions)
                
#Read in Mihaela data
with open(mihaela_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split("\t")
            L=l[0]
            R=l[1]                        
            
            #if("COMPLEX" in L):
            if("_" in L):
                #Ligand is complex
                #L=L[8:]
                L=L.split("_")
                L.sort()
                
            else:
            #Ligand is not complex 
                L=[L]
                
            #if("COMPLEX" in R):
            if("_" in R):
                #Receptor is complex
                #R=R[8:]
                R=R.split("_")
                R.sort()
            else:
            #Receptor is not complex 
                R=[R]                           
             
            all_interactions_mihaela.append([L,R])

            if(interactionExists(all_interactions, [L,R])==False):
                all_interactions.append([L,R])
                
            #Access the source database for each interaction
            L_str="_".join(L)
            R_str="_".join(R)
      
            if(L_str+"-"+R_str in interactions_db):
                interactions_db[L_str+"-"+R_str]+="/MihaelaXXX"
            else:
                interactions_db[L_str+"-"+R_str]="MihaelaXXX"


##Some summary statictics and debugging stuff
# print(all_interactions_liana[0])
# print(all_interactions_cpdb[0])
# print(all_interactions_mihaela[0])

# print("Only liana: ",len(all_interactions_liana))
# print("Only cpdb: ",len(all_interactions_cpdb))            
# print("Only mihaela: ",len(all_interactions_mihaela))  
# print("liana+cpdb: ",liana_cpdb_number)  
# print("liana+cpdb+mihaela: ",len(all_interactions))



###This was only necessary when we had to convert between gene names and uniprot IDs
###Currently we only take gene names/uniprot IDs which have been present in the source database
##Converte Uniprot IDs to gene names
#Parse conversion file
# uniprot_geneName={}
# uniprot_ENSG={}
# geneName_uniprot={}
# geneName_anyUniprot={}

# with open(conversion_file) as f:
#     for line in f:
#         if not(("GENEID" in line) or ("#" in line) ):           
#             line=line.rstrip()
#             l=line.split("\t")
#             ENSG=l[1]
#             NAME=l[2]
            
#             UNIPROT_tmp=l[4].split(".")
#             UNIPROT_tmp2=UNIPROT_tmp[0].split("-")
#             UNIPROT=UNIPROT_tmp2[0]
            
#             uniprot_geneName[UNIPROT]=NAME
#             uniprot_ENSG[UNIPROT]=ENSG
#             if(UNIPROT!="NA"):
#                 geneName_anyUniprot[NAME]=UNIPROT

# geneName_interactions=[]

# for inter in all_interactions:
#     L=inter[0]
#     R=inter[1]
    
#     L_new=[]
#     R_new=[]
#     convertable=True
    
#     if(len(L)==1):
#         if(L[0] in uniprot_geneName):
#             L_new.append(uniprot_geneName[L[0]])
#         else:
#             convertable=False
#     else:
#         for l in L:
#             if(l in uniprot_geneName):
#                 L_new.append(uniprot_geneName[l])
#             else:
#                 convertable=False
    
#     if(len(R)==1):
#         if(R[0] in uniprot_geneName):
#             R_new.append(uniprot_geneName[R[0]])
#         else:
#             convertable=False
        
#     else:
#         for r in R:
#             if(r in uniprot_geneName):
#                 R_new.append(uniprot_geneName[r])
#             else:
#                 convertable=False
    
#     if(convertable==True):
#         geneName_interactions.append([L_new,R_new])
#     else:
#         #pass
#         #We lose 26 interactions with non-convertible uniprot id
#         geneName_interactions.append("NA")
    

#print(len(geneName_interactions))
#print(len(all_interactions))
    

#Print the combined database
#print("source\ttarget\tsource_genesymbol\ttarget_genesymbol")
print("source_genesymbol\ttarget_genesymbol\tsource_db")

for i,inter in enumerate(all_interactions):
    L=inter[0]
    R=inter[1]
    db="na"
    
    #Access the source database for each interaction
    L_str="_".join(L)
    R_str="_".join(R)
      
    if(L_str+"-"+R_str in interactions_db):
        db=interactions_db[L_str+"-"+R_str]
        
    if(len(L)==1):
        print(L[0],end="\t")
    else:
        print("COMPLEX:"+"_".join(L),end="\t")
        
    if(len(R)==1):
        print(R[0],end="\tna\n")
    else:
        print("COMPLEX:"+"_".join(R),end="\t"+db+"\n")

