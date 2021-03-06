##### README ###### 

## "0_pathway_toolkit.R"
# description: This script contains 2 function useful for pathway 
#   analysis in R. Priciple is categorical terms are used to make 
#   a master list of id-to-category relationships. Then 2nd function
#   uses the mater list (AKA reference set) when performing enrichment
#   analysis usign fisher exact test, outputs the enrichemnt score/pvalue
#   and adjusted p-value for the categorical terms. This code was originally
#   produced for the dental informatics project. 
# issue: #9
# date created: 11/07/2017
# date last modified: 05/30/2020


## "01_KAO_Establishing_connection_to_db_extracting_timeStamp.R"
# description: Establishes DB connection using RSQLite package and 
#     fetches time stamp information for Raw files.
# Relevant Issue(s): 
# date created: 5/12/20
# date last modified: 5/12/20
# input:
#  - Covid-19 Study DB.sqlite
# output:
#  - 

## "X1_KAO_Updating_GC_keep_status_in_db.R"
# description: Sets 1:10 split GC files keep column to 0 (FALSE)
# date created: 5/13/20
# date last modified: 5/13/20
# input: 
# - Covid-19 Study DB.sqlite
# output: 
# - Covid-19 Study DB.sqlite (modified)

## "02_KAO_Runorder_correction_for_GC_metabolomics_data.R"
# description: Performs run order correction of the GC data and explores results.
#   this analysis is exploratory only and does not modify the db.
# date created: 5/13/20
# date last modified: 5/14/20
# input:
# - Covid-19 Study DB.sqlite

## "X2_KAO_GC_metabolomics_runtime_correction.R"
# description: Performs run order correction and modifies db. 
# date created: 5/14/20
# date last modified: 5/15/20
# input:
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite (modified metabolite_measurements table)

## "X3_KAO_Updating_GC_metabolite_tier_in_DB.R"
# description: extracts the mean tier information by molecule. This tier
#   information is useful for filtering out poor quality metabolites and 
#   is added to the sqlite db metadata table
# data created: 5/15/20
# date last modified: 5/15/20
# input:
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite (modified metadata table)

## "03_KAO_Exploring_GC_feature_quality.R"
# description: Explores 4 metrics of GC-metabolomics feature quality -
#   1) duplicate moleucles, 2) mean tier quality, 3) RSDs of QC sampels 
#   within and between batches, 4) dynamic range. 
# date created: 5/16/20
# date last modified: 5/27/20
# input:
# - Covid-19 Study DB.sqlite

## "X4_KAO_updating_biomolecules_keep_column_GC_metabolites.R"
# description: modifies DB to update metabolite keep column to 
#   denote features which should be excluded from downstream analysis.
#   5/27/20 added more filter - tier information. 
# CAUTION: script iterates and caution should be used when executing. 
# date created: 5/18/20
# date last modified: 5/27/20 
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite (biomolecules 'keep' colulmn updated)


## "04_KAO_Exploring_GC_data_after_feature_filtering.R"
# description: looks at GC data by PCA after features have been
# filtered.
# date created: 5/18/2020
# date last modified: 5/19/2020
# input: 
# - Covid-19 Study DB.sqlite

## "05_KAO_Batch_effects_in_lipidomics_data.R"
# description: looks at batch effect of lipidomics data 
#   and in doing so, catches an initial error in the db 
#   entries for lipidomics features due to the way features 
#   were named resulting in duplicate identifiers. I will 
#   work with Dain to update the lipidomics values. 
# date created 5/19/2020
# date last modified: 5/20/2020
# input:
# - Covid-19 Study DB.sqlite
# - Lipidomics/Lipidomics_quant_results/Final_Results.csv


## X5_KAO_creating_new_lipidomics_table_to_match_original.R
# description: In file 05_KAO_Batch_effects_in_lipidomics_data.R,
#   I found that the biomolecule ids did not match up across 
#   the tables in the data frame. This code creates a csv that 
#   looks like the lipidomics_measurements table, but with 
#   updated biomolecule ids (no duplicates) and batch correction
#   to the lipiomics data - run-time correction similar to the
#   GC metabolomics data. Lipid standardized names are also updated
#   in this document. 
# issue: #7
# date created: 5/20/2020
# date last modified: 5/26/2020
# input:
# - Covid-19 Study DB.sqlite
# - Lipidomics/Lipidomics_quant_results/Final_Results.csv
# output:
# -  "../../data/lipidomics_measurements_20200523.csv"
# - above csv file was used to modify db

## "X6_KAO_Creating_pvalues_table.R"
# description: this script contains a function for likelyhood ratio testing between
#   two linear regression models. This script runs this function on all metabolomics,
#   and proteomics measurements. creates a p_value and then a q_value. These data
#   were added to the databse as pvalues table.
# issue: #4
# date created: 5/26/2020
# date last modified: 6/16/2020
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite, added table pvalues 

## "06_KAO_exploring_pvalue_histograms.R
# description: this is an exploratory data analysis of pvalues 
# generated by LR test. This looks at the overall effect 
# of confounders. 
# date created: 5/27/2020
# date last modified: 5/27/2020
# input: 
# - Covid-19 Study DB.sqlite

## "X7_KAO_updating_metadata_biomolecule_id.R"
# description: updates metadata table with non-duplicate biomolecule ids 
#   for lipidomics features. Also see file:  "X5_KAO_creating_new_lipidomics
#   _table_to_match_original.R" 
# date created: 5/30/2020
# date last modified: 5/30/2020
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite, modified metadata biomolecule_id 

## "07_KAO_Exploring_lipidomics_feature_quality.R"
# description: explore aspects of lipidomics feature quality, updates
#   keep column in the biomolecules table. 
# issue: #7 
# date created: 5/30/2020
# date last modified: 6/1/2020
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite, modified biomolecules keep  

## "08_KAO_Crossomes_correlations.R"
# description: Generates a heatmap proteins x metabolites-lipids 
#   correlations > 0.4 or < -0.4 
# issue: #9
# date created: 6/2/2020
# date last modified: 6/11/2020
# input:
# - Covid-19 Study DB.sqlite 
# - 'P:/All_20200428_COVID_plasma_multiomics/Correlation/cor_4omes_kendall.RData'
# output:
# - "heatmap_cross_ome_correlations_kendall_KAO_v2.pdf

## 09_KAO_crossome_correltions_pearson.R
# description: Generates a heatmap proteins x metabolites-lipids with
#   significant pearson correlation coefficient. 
# issue #9
# date created: 6/3/2020
# date last modified: 6/3/2020
# input:
# - Covid-19 Study DB.sqlite 
# - 'P:/All_20200428_COVID_plasma_multiomics/Correlation/cor_4omes_pearson.RData'
# output:
# - "heatmap_cross_ome_correlations_pearson_KAO_v2.pdf

## X8_KAO_transcriptomics_table_upload.R
# desciptiom: appends transcriptomics data to the db. 
# date created: 6/4/2020
# date last modified: 6/5/2020
# input: 
# - Covid-19 Study DB.sqlite
# - 'P:/All_20200428_COVID_plasma_multiomics/Transcriptomics/genes.l2ec.no_hg.norm.tsv'
# - 'P:/All_20200428_COVID_plasma_multiomics/Transcriptomics/genes.ec.no_hg.norm.tsv'
# output: 
# - Covid-19 Study DB.sqlite modified to include transciptomics_runs and transcriptomics_measurements 

## 10_KAO_hospital_free_days_ANOVA_gelsolin.Rmd
# description: For the gelsolin story, wanted to explore the effect of confounders
#  on hostpital free days. 
# date created: 6/5/20
# date last modified: 6/5/20
# input: 
# - Covid-19 Study DB.sqlite

## 11_KAO_Looking_at_effect_of_DM_status.R
# description: This script uses linear regressaion with response factor of hospital 
#  free days at 45 to see if diabetes (DM) status has any effect. There does not apprear
#  to be any significant effect with diabetes.
# date create: 6/5/20
# date last modified: 6/5/20
# input:
# - Covid-19 Study DB.sqlite

## X9_KAO_Adding_Yuchens_pvalues_into_DB.R
# description: Yuchen performed analysis on HFD for each biomolecue. 
# linear regression stats - anova(lm(biomolecule abundance ~ Hopsital_free_days_45))
# These data are found in Rdata files in regression folder and were added to the 
# pvalues table. 
# issue: #4
# date create: 6/8/20
# date last modified: 6/17/20
# input:
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite modified pvalues table. 

## X10_KAO_adding_GO_terms_to_db.R
# description: Anji extracted GO terms based on uniprot ID. this script adds that 
#  data into the db. 
# date created: 6/8/20
# date last modified: 6/8/20
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite modified metadata table. 

## 12_KAO_GO_term_enrichment_for_significant_p_values.R
# description: GO term encrichmetn for significant p_values 
# date created: 6/9/20
# date last modified: 6/9/20
# input: 
# - Covid-19 Study DB.sqlite
# output: 
# - plots/

## 13_KAO_calculating_FC_for_COVID.R
# description: calculates FC for COVID vs. non-COVID in the same 
#   manner as Ian's webtool (also see dash/plots.py)
# date created: 6/25/20
# date last modified: 6/25/20
# input:
# - Covid-19 Study DB.sqlite
# output: 
# - data/COVID_fc_by_biomolecule_ID.csv

## 14_KAO_figure_2_version_1.R
# description: This is a script which is intended to combine different 
#  omes data into one (or multiple) biological stories. Presents high level
#  view of the data and does GO enrichment. 
# date created: 6/24/20
# date last modified: 7/9/20
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - plots/ 

## X11_Adding_GO_terms_for_transcripts_into_db.R
# decription: I used Uniprot to collect GO terms for transcripts. this script adds
#   those GO terms for biological processes into the db. 
# date created: 6/26/20
# date last modified: 6/26/20
# input:
# - "data/uniprot-genelist.tab", generated 2020-06-25 from uniprot webtool
# -  Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite with modified metadata table 

## 15_Volcano_plots_for_Trent_for_Fig3.R 
# description: Trent provided me a list of proteomics features that were important 
# to specific pathways (coagulation, etc), this script plots those features relative 
# the rest of the proteome in a volcano plot for COVID status. 
# date created: 6/27/20
# date last modified: 7/9/20
# input: 
# - "data/Proteins grouped for Fig 3 Volcano Plots.csv"
# - Covid-19 Study DB.sqlite
# - "data/COVID_fc_by_biomolecule_ID.csv"
# output:
# - plots/

## 16_KAO_merging_CD3.1_results_with_Lipidex_output.R 
# description: for supplementary table with unknown matches to CD3.1 searching. 
#   this script connects CD3.1 results by mz and RT to the lipids unknowns table.
# date created: 7/9/20
# date last modified: 7/9/20
# input:
# - "P:/All_20200428_COVID_plasma_multiomics/Lipidomics/CD3_all_discovery_metabolomics_filtered.csv"
# - Covid-19 Study DB.sqlite
# output:
# - "data/Sup_table_2_merge_unknowns.csv"

## 17_KAO_Dynamic_range_for_each_ome.R
# description: Plotting the distributions of each omic data set. 
# date created: 7/19/20
# date last modified: 7/19/20
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - plot 

## 18_KAO_Comparing_WHO_score_to_HFD.R
# description: A reviewer resquested we incorporate WHO ordianl score into the database. 
# This script looks at how the HFD-45 outcome metric compares to the WHO at 28 days. 
# date created: 8/31/20
# date last modified: 8/31/20
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - plot 

## X6_KAO_Creating_pvalues_table_response_to_reviewer.R
# description: A reviewer asked about the validity of linear regression models given
# that outliers can strongly effect the fits of models. This script provides additional 
# pvalue calculation using a robust linear regression and adds to the database
# date created: 8/31/20
# date last _modifed: 8/31/20
# input: 
# - Covid-19 Study DB.sqlite
# output:
# - Covid-19 Study DB.sqlite, modified pvalues table