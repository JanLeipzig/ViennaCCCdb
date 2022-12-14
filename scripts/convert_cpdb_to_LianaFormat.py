#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:42:21 2022

@author: engelhardt
"""
import sys, warnings

#Location of cellphoneDB database on file system, e.g. '/home/user/cpdb_v4.0.0/'
cpdb_dir=sys.argv[1]

cpdb_inter=cpdb_dir+"/data/interaction_input.csv"
cpdb_complex=cpdb_dir+"/data/complex_input.csv"
cpdb_protein=cpdb_dir+"/data/protein_input.csv"


#Read in cpdb data

notUNIPROTS=['GMCSFR']

cpdb_complex_dict={}
cpdb_complex_dict_rec={}

cpdb_interactions={}
all_interactions=[]

unclearReceptors=0
#parses cpdb_v4.0.0/data/complex_input.csv to get information
#about the complexes stored in cpdb
#cpdb_complex_dict - complex_name : complex_proteinArts
#cpdb_complex_dict_rec - complex_name : Receptor[True/False]

#TODO: Maybe save small molecule ligand name (_by)

with open(cpdb_complex) as f:
    for line in f:
        if not("complex_name" in line):
            line=line.rstrip()
            l=line.split(",")

            proteinArts=[]
            
            for i in range(4):
                comp=l[i+1]
                if(comp!=""):
                    proteinArts.append(comp)
            proteinArts.sort()
            cpdb_complex_dict[l[0]]=proteinArts
            cpdb_complex_dict_rec[l[0]]=l[10]     
                        
#parses cpdb_v4.0.0/data/protein_input.csv to get receptor annotation
#cpdb_protein_dict_rec -protein_id : Receptor[True/False]
cpdb_simple_dict_rec={}
with open(cpdb_protein) as f:
    for line in f:
        line=line.rstrip()
        l=line.split(",")
        
        if not("protein_name" in line):
            cpdb_simple_dict_rec[l[0]]=l[7]
            
#parses cpdb_v4.0.0/data/interaction_input.csv to process the actual interactions
with open(cpdb_inter) as f:
    for line in f:

        #TODO: Maybe handle HLA's, IFNA1 and '_by' things differently
        #HLA removed due to 'weird(?)' manual annotation
        #IFNA1 removed since no uniprot id for it is givein in protein_input.csv
        if not(("partner_a" in line) or ("IFNA1" in line) or ("HLA" in line)):
            line=line.rstrip()
            l=line.split(",")
            
            proteinA=l[0]
            proteinB=l[1]

            #Presumably database error in cpdbv4
            #Gene name is given instead of uniprot-id
            if(proteinA=="CCL3L1"):
                proteinA="P16619"
            if(proteinB=="CCL3L1"):
                proteinB="P16619"
            
            if((len(proteinA)!=6) or (proteinA in notUNIPROTS)):

                if proteinA in cpdb_complex_dict:
                    
                    A=cpdb_complex_dict[proteinA]
                    A_rec=cpdb_complex_dict_rec[proteinA]
                    
                else:
                    warnings.warn("Warning: "+proteinA+" was not found in complexes")
            else:
                A=[proteinA]
                A_rec=cpdb_simple_dict_rec[proteinA]
                
            if((len(proteinB)!=6) or (proteinB in notUNIPROTS)):
                #B_compl=1
                if proteinB in cpdb_complex_dict:
                      
                    B=cpdb_complex_dict[proteinB]                      
                    B_rec=cpdb_complex_dict_rec[proteinB]
                else:
                    warnings.warn("Warning: "+proteinB+"was not found in complexes")
            else:
                B=[proteinB]
                B_rec=cpdb_simple_dict_rec[proteinB]
           
            #print(A,B)
            
            
            #Prints interactions
            #col1,2 - liana format
            #col3,4 - original cpdb format
            #col4 - data source            
            #TODO: Only works if ligand is a single protein
            #R-L
            if(A_rec=="True" and B_rec=="False"):
                pass
                all_interactions.append([B,A])
            elif(B_rec=="True" and A_rec=="False"):
                pass
                all_interactions.append([A,B])
            else:
                pass
                unclearReceptors+=1
 
##Summary statistics                
#Should be 2171 interactions
#858 interactions are not used due to unclear receptor status
#print(len(all_interactions))    
#print(unclearReceptors)
for inter in all_interactions:
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
        

        
###OLD CODE FROM MAIN SCRIPT
# notUNIPROTS=['GMCSFR','HLA']

# cpdb_complex_dict={}
# cpdb_complex_dict_rec={}

# cpdb_interactions={}

# #parses cpdb_v4.0.0/data/complex_input.csv to get information
# #about the complexes stored in cpdb
# #cpdb_complex_dict - complex_name : complex_proteinArts
# #cpdb_complex_dict_rec - complex_name : Receptor[True/False]

# #TODO: Maybe save small molecule ligand name (_by)

# with open(cpdb_complex) as f:
#     for line in f:
#         if not("complex_name" in line):
#             line=line.rstrip()
#             l=line.split(",")

#             proteinArts=[]
            
#             for i in range(4):
#                 comp=l[i+1]
#                 if(comp!=""):
#                     proteinArts.append(comp)
#             proteinArts.sort()
#             cpdb_complex_dict[l[0]]=proteinArts
#             cpdb_complex_dict_rec[l[0]]=l[10]     
                        
# #parses cpdb_v4.0.0/data/protein_input.csv to get receptor annotation
# #cpdb_protein_dict_rec -protein_id : Receptor[True/False]
# cpdb_simple_dict_rec={}
# with open(cpdb_protein) as f:
#     for line in f:
#         if not("protein_name" in line):
#             line=line.rstrip()
#             l=line.split(",")
#             cpdb_simple_dict_rec[l[0]]=l[7]
            
# #parses cpdb_v4.0.0/data/interaction_input.csv to process the actual interactions
# with open(cpdb_inter) as f:
#     for line in f:
#         #A_compl=0
#         #B_compl=0

#         #TODO: Maybe handle HLA's, IFNA1 and '_by' things differently
#         if not(("partner_a" in line) or ("IFNA1" in line) or ("HLA" in line)):
#             line=line.rstrip()
#             l=line.split(",")
            
#             proteinA=l[0]
#             proteinB=l[1]

#             #Presumably database error in cpdbv4
#             #Gene name is given instead of uniprot-id
#             if(proteinA=="CCL3L1"):
#                 proteinA="P16619"
#             if(proteinB=="CCL3L1"):
#                 proteinB="P16619"
            
#             if((len(proteinA)!=6) or (proteinA in notUNIPROTS)):

#                 if proteinA in cpdb_complex_dict:
#                     #Deprecated?
#                     # if(len(cpdb_complex_dict[proteinA])>1):
#                     #     A="COMPLEX:"+'_'.join(cpdb_complex_dict[proteinA])
#                     # else:
#                     #     A=cpdb_complex_dict[proteinA]
                    
#                     A=cpdb_complex_dict[proteinA]
#                     A_rec=cpdb_complex_dict_rec[proteinA][0]
#                 else:
#                     warnings.warn("Warning: "+proteinA+" was not found in complexes")
#             else:
#                 A=[proteinA]
#                 A_rec=cpdb_simple_dict_rec[proteinA]
                
#             if((len(proteinB)!=6) or (proteinB in notUNIPROTS)):
#                 #B_compl=1
#                 if proteinB in cpdb_complex_dict:
#                     #Deprecated?
#                     # if(len(cpdb_complex_dict[proteinB])>1):
#                     #     B="COMPLEX:"+'_'.join(cpdb_complex_dict[proteinB])
#                     # else:
#                     #     B=cpdb_complex_dict[proteinB]
                    
#                     B=cpdb_complex_dict[proteinB]
                        
#                     B_rec=cpdb_complex_dict_rec[proteinB]
#                 else:
#                     warnings.warn("Warning: "+proteinB+"was not found in complexes")
#             else:
#                 B=[proteinB]
#                 B_rec=cpdb_simple_dict_rec[proteinB]
           
         
#             #Prints interactions
#             #col1,2 - liana format
#             #col3,4 - original cpdb format
#             #col4 - data source            
#             #TODO: Only works if ligand is a single protein
#             #R-L
#             if(A_rec=="True" and B_rec=="False"):
#                 cpdb_interactions[B[0]]=[A]
#                 all_interactions_cpdb.append([B,A])
                
#                 if(interactionExists(all_interactions, [[B],[A]])==False):
#                     all_interactions.append([[B],[A]])
                   
#                 else:
#                     pass
#                     #print("1",[[B],[A]])
#             #L-R
#             elif(B_rec=="True" and A_rec=="False"):
#                 cpdb_interactions[A[0]]=[B]
#                 all_interactions_cpdb.append([A,B])
                
#                 if(interactionExists(all_interactions, [[A],[B]])==False):
#                     all_interactions.append([[A],[B]])
                    
#                 else:
#                     pass
#                     #print("2",[[A],[B]])
#                 ###print(A,B,proteinA,proteinB,"CPDBv4")
#             else:
#                 #The not annotated interactions
#                 pass
#                 print(A,B)
#                 #print("#"+A,B,proteinA,proteinB,"CPDBv4",A_rec,B_rec)
#                 #print("#"+B,A,proteinB,proteinA,"CPDBv4",B_rec,A_rec)
        