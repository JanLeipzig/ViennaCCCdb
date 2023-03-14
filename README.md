# ViennaCCCdb

Combination of three existing cell-cell communication databases, i.e. Liana Consensus database v0.1.7, CellPhoneDB v4 and a manual selection based on Pavlicev et al. 2017. If an interaction exists in more than one database it is included only once.

## Methods
### Download source data
Extract liana consensus database from https://github.com/saezlab/liana
- Install liana

```
library(liana)
consensus<-select_resource(c('Consensus'))
write.table(consensus, file="liana-db_0.1.12.txt")
```

Download CellPhoneDB v4 from https://github.com/ventolab/CellphoneDB
- Find the database in your home in .cpdb/releases/

Download CellPhoneDB v4.1 from https://github.com/ventolab/cellphonedb-data/releases/tag/v4.1.0

Download additional interactions originally from Pavlicev et
al. (2017) and curated by D. Stadtmauer from
https://gitlab.com/wandplabs/ligrec-enzymes

### Convert to liana format
```
python scripts/convert_cpdb_to_LianaFormat.py source_databases/cpdb_v4.0.0/ > cpdb_lianaformat.txt

python scripts/convert_customData_to_LianaFormat.py source_databases/interaction_input_CellChatDB.csv > customData_lianaformat.txt
```

### Create "raw version" of combined database
This file is the basic input necessary for cell-cell interaction pipelines. Annotation of these interactions is stored in ViennaCCCdb_annotation.csv
```
python scripts/createCombinedDatabase.py source_databases/liana-db_0.1.12.txt source_databases/cpdb_lianaformat.txt source_databases/customData_lianaformat.txt > ViennaCCCdb_raw.csv
```

## Notes
### Manual editions to CellPhoneDB
- for 'CCL3L1' no uniprot id was given, 'P16619' was used manually
- interactions with 'IFNA*' genes are excluded since no uniprot ids were given in 'protein_input.csv', see https://github.com/JanLeipzig/ViennaCCCdb/issues/1
- interactions with 'HLA' genes are excluded since no uniprot ids were given in 'protein_input.csv' possibly due to them beeing manually curated. Manual uniprot ids would have to be consistent with liana consensus
