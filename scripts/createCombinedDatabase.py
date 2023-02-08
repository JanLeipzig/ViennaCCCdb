#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:09:06 2022

@author: engelhardt

TODO Read in three databases into internal data structure: Liana, cpdb and Mihaela
TODO Combine them to unique entries based on gene-names (primarily)
TODO Print them to a new file

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

liana_data=sys.argv[1]
cpdb_data=sys.argv[2]
mihaela_data=sys.argv[3]
conversion_file=sys.argv[4]

#datafiles
#liana_data="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/liana_0.1.6-database.txt"
#cpdb_data="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/cpdb_lianaformat_v2.txt"
#mihaela_data="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/mihaela_lianaformat_v2.txt"

#conversion_file="/home/engelhardt/bioinf/InterfaceProject/interface_scripts/CCI_database/gene_conversion-AH104864.csv"

#Complete database
all_interactions=[]

#only needed for debugging
all_interactions_liana=[]
all_interactions_cpdb=[]
all_interactions_mihaela=[]

#Read in Liana data
liana_interactions={}

with open(liana_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split(" ")
            L=l[1][1:-1]
            R=l[2][1:-1]
                       
            if("COMPLEX" in L):
                #Ligand is complex
                #DEPR L_compl=1
                L=L[8:]
                L=L.split("_")
                L.sort()
                #L=','.join(L)
            else:
            #Ligand is not complex 
                L=[L]
                
            if("COMPLEX" in R):
                #Receptor is complex
                #DEPR R_compl=1
                R=R[8:]
                R=R.split("_")
                R.sort()
                #R=','.join(R)
            else:
            #Receptor is not complex 
                R=[R]
                  
            all_interactions.append([L,R])
            all_interactions_liana.append([L,R])






#Read in cpdb data
with open(cpdb_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split("\t")
            L=l[0]
            R=l[1]
                       
            if("COMPLEX" in L):
                #Ligand is complex
                #DEPR L_compl=1
                L=L[8:]
                L=L.split("_")
                L.sort()
                #L=','.join(L)
                #print(L)
                
            else:
            #Ligand is not complex 
                L=[L]
                
            if("COMPLEX" in R):
                #Receptor is complex
                #DEPR R_compl=1
                R=R[8:]
                R=R.split("_")
                R.sort()
                #R=','.join(R)
            else:
            #Receptor is not complex
                R=[R]                           
             
            all_interactions_cpdb.append([L,R])

            if(interactionExists(all_interactions, [L,R])==False):
                all_interactions.append([L,R])              

liana_cpdb_number=len(all_interactions)
                
#Read in Mihaela data
with open(mihaela_data) as f:
    for line in f:
        if not ("source_genesymbol" in line):
            line=line.rstrip()
            l=line.split("\t")
            L=l[0]
            R=l[1]
                       
            if("COMPLEX" in L):
                #Ligand is complex
                L=L[8:]
                L=L.split("_")
                L.sort()
                #L=','.join(L)
                
            else:
            #Ligand is not complex 
                L=[L]
                
            if("COMPLEX" in R):
                #Receptor is complex
                #DEPR R_compl=1
                R=R[8:]
                R=R.split("_")
                R.sort()
                #R=','.join(R)
            else:
            #Receptor is not complex 
                R=[R]                           
             
            all_interactions_mihaela.append([L,R])

            if(interactionExists(all_interactions, [L,R])==False):
                all_interactions.append([L,R])

##Some summary statictics and debugging stuff
# print(all_interactions_liana[0])
# print(all_interactions_cpdb[0])
# print(all_interactions_mihaela[0])

# print("Only liana: ",len(all_interactions_liana))
# print("Only cpdb: ",len(all_interactions_cpdb))            
# print("Only mihaela: ",len(all_interactions_mihaela))  
# print("liana+cpdb: ",liana_cpdb_number)  
# print("liana+cpdb+mihaela: ",len(all_interactions))

#print(all_interactions)
# for inter in all_interactions:
#     L=inter[0]
#     R=inter[1]
#     if(len(L)>1 or len(R)>1):
#         print(L,R)
#         sys.exit()
        
# for inter in all_interactions:
#     L=inter[0]
#     R=inter[1]
    
#     if(len(L)==1):
#         print(L[0],end="\t")
#     else:
#         print("COMPLEX:"+"_".join(L),end="\t")
        
#     if(len(R)==1):
#         print(R[0])
#     else:
#         print("COMPLEX:"+"_".join(R))

        

# #TODO: Make real combination with getting rid of duplets
# #combined_uniprot=cpdb_interactions
# #combined_uniprot=liana_interactions


# #Check overlap of cpdb with mihaela
# for m_ligand in mihaela_interactions:
#     if(m_ligand in cpdb_interactions):
#         #print(m_ligand)
#         pass
#         #TODO No overlap so far
#         # cpdb_receptors=cpdb_interactions[cpdb_ligand]
#         # liana_receptors=liana_interactions[cpdb_ligand]
        
#         # #Identical receptors, get rid of cpdb interaction
#         # if(cpdb_receptors == liana_receptors):
#         #      tmp_cpdb_interactions.pop(cpdb_ligand)
#         # else:
            
 
#         #     for c1,cpdb_receptor in enumerate(cpdb_receptors):
            
#         #         #One Receptor list-element is identical to another receptor list-element
#         #         if cpdb_receptor in liana_receptors:
#         #               #If it is the only receptor for this cpdb ligand remove the whole interaction from dict
#         #             if(len(cpdb_receptors)==1):
#         #                 tmp_cpdb_interactions.pop(cpdb_ligand)
#         #             else:
#         #                 #Otherwise remove only the respective receptor
#         #                 tmp_cpdb_interactions[cpdb_ligand]=tmp_cpdb_interactions[cpdb_ligand].remove(cpdb_receptor)
 
# cpdb_interactions_new={**cpdb_interactions,**mihaela_interactions}
# cpdb_interactions=cpdb_interactions_new

# #i=0
# #check if any cpdb interaction is in liana
# tmp_cpdb_interactions=copy.deepcopy(cpdb_interactions)

# for c0,cpdb_ligand in enumerate(cpdb_interactions):
#     if(cpdb_ligand in liana_interactions):
#         cpdb_receptors=cpdb_interactions[cpdb_ligand]
#         liana_receptors=liana_interactions[cpdb_ligand]
        
#         #Identical receptors, get rid of cpdb interaction
#         if(cpdb_receptors == liana_receptors):
#              tmp_cpdb_interactions.pop(cpdb_ligand)
#         else:
            
 
#             for c1,cpdb_receptor in enumerate(cpdb_receptors):
            
#                 #One Receptor list-element is identical to another receptor list-element
#                 if cpdb_receptor in liana_receptors:
#                       #If it is the only receptor for this cpdb ligand remove the whole interaction from dict
#                     if(len(cpdb_receptors)==1):
#                         tmp_cpdb_interactions.pop(cpdb_ligand)
#                     else:
#                         #Otherwise remove only the respective receptor
#                         tmp_cpdb_interactions[cpdb_ligand]=tmp_cpdb_interactions[cpdb_ligand].remove(cpdb_receptor)
                        
#                 else:
                    
#                     #Check if receptor is identical to part of receptor complex
#                     pass
                
#                     #Ignore this part for now
                   
#                     # # print("C1",cpdb_receptor)
                                        
#                     # for l1,liana_receptors1 in enumerate(liana_receptors):
#                     #     # print("L1",liana_receptors1)
                        
#                     #     for c2,cpdb_receptors2 in enumerate(cpdb_receptor):
#                     #         # print("C2",cpdb_receptors2)

#                     #         for l2,liana_receptors2 in enumerate(liana_receptors1):                            
#                     #             # print("L2",liana_receptors2)
#                     #             if(cpdb_receptors2==liana_receptors2):
#                     #                 print("------------")
#                     #                 print("C0",cpdb_ligand,cpdb_receptors,len(cpdb_receptors))
#                     #                 print("L0",cpdb_ligand,liana_receptors,len(liana_receptors))
#                     #                 print("Test",cpdb_receptor)
#                     #                 i+=1



# #TODO: check some cpdb interactions and more complicated stuff
# combined_uniprot={**tmp_cpdb_interactions,**liana_interactions}


##Converte Uniprot IDs to gene names
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

geneName_interactions=[]

for inter in all_interactions:
    L=inter[0]
    R=inter[1]
    
    L_new=[]
    R_new=[]
    convertable=True
    
    if(len(L)==1):
        if(L[0] in uniprot_geneName):
            L_new.append(uniprot_geneName[L[0]])
        else:
            convertable=False
    else:
        for l in L:
            if(l in uniprot_geneName):
                L_new.append(uniprot_geneName[l])
            else:
                convertable=False
    
    if(len(R)==1):
        if(R[0] in uniprot_geneName):
            R_new.append(uniprot_geneName[R[0]])
        else:
            convertable=False
        
    else:
        for r in R:
            if(r in uniprot_geneName):
                R_new.append(uniprot_geneName[r])
            else:
                convertable=False
    
    if(convertable==True):
        geneName_interactions.append([L_new,R_new])
    else:
        #pass
        #We lose 26 interactions with non-convertible uniprot id
        geneName_interactions.append("NA")
    

#print(len(geneName_interactions))
#print(len(all_interactions))
    

#Print the combined database
print("source\ttarget\tsource_genesymbol\ttarget_genesymbol")

for i,inter in enumerate(all_interactions):
    L=inter[0]
    R=inter[1]
    
    if(geneName_interactions[i]!="NA"):
        if(len(L)==1):
            print(L[0],end="\t")
        else:
            print("COMPLEX:"+"_".join(L),end="\t")
            
        if(len(R)==1):
            print(R[0],end="\t")
        else:
            print("COMPLEX:"+"_".join(R),end="\t")
         
        Lg=geneName_interactions[i][0]    
        Rg=geneName_interactions[i][1]
        
        if(len(Lg)==1):
            print(Lg[0],end="\t")
        else:
            print("_".join(Lg),end="\t")
            
        if(len(Rg)==1):
            print(Rg[0],end="\n")
        else:
            print("_".join(Rg),end="\n")



# for ligand in combined_geneName:
#     recs=combined_geneName[ligand]
    
#     #print("--------")
#     #print(ligand,recs)
#     #if(ligand=="NRG2"):
    
    
#     if(',' in ligand):
#         ligand_print="COMPLEX:"+"_".join(ligand.split(','))
        
#         #ligand_print="_".join(ligand.split(','))
#         ligand_print_uniprot="nx"
#     else:
#         ligand_print=ligand     
#         ligand_print_uniprot=geneName_uniprot[ligand]
#         #ligand_print_uniprot="nx"
            
#     r_print_uniprot=""
#     r_tmp=[]
    
#     for r in recs:
#         if(len(r)==1):
#             r_print=r[0]
#             r_print_uniprot=geneName_uniprot[r[0]]
#         else:   
#             r_print="COMPLEX:"+"_".join(r)
#             for u in r:
#                 r_tmp.append(geneName_uniprot[u])
#             r_print_uniprot="COMPLEX:"+"_".join(r_tmp)
        
#         print(ligand_print_uniprot+"\t"+r_print_uniprot+"\t"+ligand_print+"\t"+r_print)
            
        

