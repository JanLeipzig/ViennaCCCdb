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
cpdb_gene_input=cpdb_dir+"/data/gene_input.csv"


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

#parses cpdb_v4.0.0/data/gene_input_all.csv to get uniprot to gene_name mapping
cpdb_genenames={}
with open(cpdb_gene_input) as f:
    for line in f:
        if not("gene_name" in line):
            line=line.rstrip()
            l=line.split(",")

            uniprot=l[1]
            gene_name=l[0]
            cpdb_genenames[uniprot]=gene_name


            
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

            #protein A is complex
            if((len(proteinA)!=6) or (proteinA in notUNIPROTS)):
                if proteinA in cpdb_complex_dict:                    
                    A=cpdb_complex_dict[proteinA]
                    A_rec=cpdb_complex_dict_rec[proteinA]                    
                else:
                    warnings.warn("Warning: "+proteinA+" was not found in complexes")

            #protein A is simple
            else:
                A=[proteinA]
                A_rec=cpdb_simple_dict_rec[proteinA]
                

            #protein B is complex                
            if((len(proteinB)!=6) or (proteinB in notUNIPROTS)):
                if proteinB in cpdb_complex_dict:                     
                    B=cpdb_complex_dict[proteinB]                      
                    B_rec=cpdb_complex_dict_rec[proteinB]
                else:
                    warnings.warn("Warning: "+proteinB+"was not found in complexes")

            #protein B is simple
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
    inter_uniprot=""
    inter_genes=""
    
    if(len(L)==1):
        #print(L[0],end="\t")
        inter_uniprot=L[0]+"\t"
        inter_genes=cpdb_genenames[L[0]]+"\t"
    else:
        #print("COMPLEX:"+"_".join(L),end="\t")
        inter_uniprot="COMPLEX:"+"_".join(L)+"\t"

        L_genes=[]
        for l in L:
            L_genes.append(cpdb_genenames[l])        
        inter_genes="COMPLEX:"+"_".join(L_genes)+"\t"
        
    if(len(R)==1):
        #print(R[0])
        inter_uniprot+=R[0]
        inter_genes+=cpdb_genenames[R[0]]
    else:
        #print("COMPLEX:"+"_".join(R))
        inter_uniprot+="COMPLEX:"+"_".join(R)

        R_genes=[]
        for r in R:
            R_genes.append(cpdb_genenames[r])        
        inter_genes+="COMPLEX:"+"_".join(R_genes)

    print(inter_uniprot+"\t"+inter_genes)
