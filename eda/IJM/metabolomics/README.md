# Notebooks and EDA for metabolomics datasets

### 1.0_metabolomics_qc.ipynb

**description**:   
    1. Load data from SQLlite data base  
    2. Join metabolomics measurements and clinical metadata tables  
    3. Run PCA  
    4. Generate plot scores plot and color by ICU status  
**Relevant Issue(s)**: NA  
**date created**: 5/12/20  
**date last modified**: 5/19/20  
**input**:  
  - sqlite_db: data/SQLite Database/Covid-19 Study DB.sqlite  
**output**:  
  - NA  

### 1.1_metabolomics_qc.ipynb 

description: Same as 1.0_metabolomics_qc.ipynb but joins are pandas-centric and rawfiles 'keep' column filtered.
Relevant Issue(s): NA
date created: 5/19/20
date last modified: 5/19/20
input:
  - sqlite_db: data/SQLite Database/Covid-19 Study DB.sqlite
output:
  - NA
