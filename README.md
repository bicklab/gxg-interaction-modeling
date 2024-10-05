# Variance quantitative trait loci reveal gene-gene interactions which alter blood traits

Github repo for Pershad & Poisner et al, medRxiv, 2024. https://doi.org/10.1101/2024.09.18.24313883.


<!--ts-->
   * [Genome-wide variance QTL scan (Scale test)](#scale)
   * [Gene-specific variance QTL scan (dglm)](#dglm)
   * [Gene-gene interaction testing (gxg)](#gxg)
<!--te-->

## Genome-wide variance QTL scan (Scale test)

Functions in [vGWAS notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/vGWAS_code.ipynb)

1. Inverse normal transform traits
2. Calculate residual and square it
3. Run genome wide association study with Regenie v3.3 on the UK Biobank DNA Nexus Research Analysis Platform on both rank-inverse normalized trait (mean) and square of the residual of the rank-inverse-normalized trait (variance). Covariates were age at blood draw, age at blood draw2, sex, genetic ancestry, and the first 5 genotyping principal components.
```
# Example Regenie Step 1 for Lymphocyte Count (Mean) for chr5 
regenie \
--step 1 \
--bed ukb_imp_step1 \
--phenoFile Users_Yash_Pershad_lymph_vgwas_pheno_cov_v2.tsv \
--bsize 1000 \
--use-relative-path \
--extract /home/dnanexus/PACER_UKB_GWAS_step1QC_plink_mac5000_thinned.snplist \
--covarFile jak2_plt_interaction_data_yp07152024.tsv \
--phenoColList lymph_rint \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10 \
--catCovarList genetic_sex \
--out lymph_gwas

# Example Regenie Step 2 for Lymphocyte Count (Mean) for chr5
regenie \
--step 2 \
--bgen ukb22828_c12_b0_v3.bgen \
--phenoFile Users_Yash_Pershad_lymph_vgwas_pheno_cov_v2.tsv \
--bsize 200 \
--pThresh 0.05 \
--test additive \
--pred lymph_gwas_pred.list \
--gz \
--sample ukb22828_c12_b0_v3.sample \
--extract /home/dnanexus/imputed_UKB_GWAS_step2QC_plink_maf0.001_geno0.1_chr12.snplist \
--covarFile jak2_plt_interaction_data_yp07152024.tsv \
--firth \
--approx \
--firth-se \
--phenoColList lymph_rint \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10 \
--catCovarList genetic_sex \
--ref-first --htp ukb22828_c12_b0_v3 \
--out lymph_gwas_ukb22828_c12_b0_v3

# Example Regenie Step 1 for Lymphocyte Count (Variance) for chr5 
regenie \
--step 1 \
--bed ukb_imp_step1 \
--phenoFile Users_Yash_Pershad_lymph_vgwas_pheno_cov_v2.tsv \
--bsize 1000 \
--use-relative-path \
--extract /home/dnanexus/PACER_UKB_GWAS_step1QC_plink_mac5000_thinned.snplist \
--covarFile jak2_plt_interaction_data_yp07152024.tsv \
--phenoColList lymph_rint_resid_sq \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10 \
--catCovarList genetic_sex \
--out lymph_resid_gwas

# Example Regenie Step 2 for Lymphocyte Count (Variance) for chr5
regenie \
--step 2 \
--bgen ukb22828_c5_b0_v3.bgen \
--phenoFile Users_Yash_Pershad_lymph_vgwas_pheno_cov_v2.tsv \
--bsize 200 \
--pThresh 0.05 \
--test additive \
--pred lymph_resid_gwas_pred.list \
--gz --sample ukb22828_c5_b0_v3.sample \
--extract /home/dnanexus/imputed_UKB_GWAS_step2QC_plink_maf0.001_geno0.1_chr5.snplist \
--covarFile jak2_plt_interaction_data_yp07152024.tsv \
--firth \
--approx \
--firth-se \
--phenoColList lymph_rint_resid_sq \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10 \
--catCovarList genetic_sex \
--ref-first --htp ukb22828_c5_b0_v3 \
--out lymph_resid_gwas_ukb22828_c5_b0_v3

```
5. Select SNPs with if they had a genome-wide significant association with the variance of a trait ($P < 5x10^{-8}$) without a significant mean effect after multiple-hypothesis correction ($P > 5x10^{-8}$).
6. Run GxG interaction model (Section 3)


## Gene-specific variance QTL scan (dglm)
1. Extract variants in gene of interest with minor allele frequency > 10% using plink2 on the UK Biobank DNA Nexus Research Analysis Platform.
```
# Example for variants in HFE
plink2 \
--bgen ukb22828_c6_b0_v3.bgen ref-first \
--sample ukb22828_c6_b0_v3.sample \
--chr 6 \
--from-bp 26087657 \
--to-bp 26098571 \
--maf 0.1 \
--export vcf \
--out hfe_snps
```

2.

## Gene-gene interaction testing (gxg)
Functions in [gene-gene-interaction notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/gene-gene-interaction_code.ipynb).

1. Run genome wide association study with Regenie v3.3 on the UK Biobank DNA Nexus Research Analysis Platform.
```
# Example Regenie interaction step 1 for lymphocyte count and variance quantitative trait loci rs3819720 for chr5
regenie \
--step 1 \
--bed ukb_imp_step1 \
--phenoFile rs3819720_lymph_interaction_phenocov.tsv \
--bsize 1000 \
--use-relative-path \
--extract /home/dnanexus/PACER_UKB_GWAS_step1QC_plink_mac5000_thinned.snplist \
--covarFile rs3819720_lymph_interaction_phenocov.tsv \
--phenoColList lymph \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10,rs3819720 \
--catCovarList genetic_sex \
--apply-rint \
--out lymph_rs3819720

# Example Regenie interaction step 2 for lymphocyte count and variance quantitative trait loci rs3819720 for chr5
regenie \
--step 2 \
--bgen ukb22828_c5_b0_v3.bgen \
--phenoFile rs3819720_lymph_interaction_phenocov.tsv \
--bsize 200 \
--pThresh 0.05 \
--test additive \
--pred lymph_rs3819720_pred.list \
--gz \
--sample ukb22828_c5_b0_v3.sample \
--extract /home/dnanexus/imputed_UKB_GWAS_step2QC_plink_maf0.001_geno0.1_chr5.snplist \
--covarFile rs3819720_lymph_interaction_phenocov.tsv \
--firth \
--approx \
--firth-se \
--phenoColList lymph \
--covarColList baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10,rs3819720 \
--catCovarList genetic_sex \
--apply-rint \
--interaction rs3819720 \
--ref-first \
--htp ukb22828_c5_b0_v3 \
--out lymph_rs3819720_ukb22828_c5_b0_v3
```
2. Find significant interactors (Model = "ADD-WGR-LR-INT_SNPx[SNP])
3. Extract SNPs which are significant using plink.
```
# Example for HFE variant
plink2 \
--bgen ukb22828_c6_b0_v3.bgen ref-first \
--sample ukb22828_c6_b0_v3.sample \
--chr 6 \
--from-bp 26091178 \
--to-bp 26091180 \
--export vcf \
--out hfe_pathogenic_rs1799945_snp
```
5. Make epistasis plots.

## Power calculations
Code in [this notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/Epistasis%20power%20calculations.ipynb)
