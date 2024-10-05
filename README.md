# Variance Quantitative Trait Loci Reveal Gene-Gene Interactions Altering Blood Traits

This repository contains the code and analysis scripts for Pershad & Poisner et al, medRxiv, 2024. https://doi.org/10.1101/2024.09.18.24313883

## Table of Contents
1. [Genome-wide Variance QTL Scan (Scale test)](#genome-wide-variance-qtl-scan-scale-test)
2. [Gene-specific Variance QTL Scan (dglm)](#gene-specific-variance-qtl-scan-dglm)
3. [Gene-Gene Interaction Testing (gxg)](#gene-gene-interaction-testing-gxg)
4. [Power Calculations](#power-calculations)

## Genome-wide Variance QTL Scan (Scale test)

Code available in: [vGWAS notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/vGWAS_code.ipynb)

### Workflow:
1. Inverse normal transform traits
2. Calculate residual and square it
3. Run genome-wide association study with Regenie v3.3 on the UK Biobank DNA Nexus Research Analysis Platform
4. Select SNPs with genome-wide significant association with trait variance (P < 5x10^-8) without significant mean effect (P > 5x10^-8)
5. Run GxG interaction model (See Section 3)

Functions in [vGWAS notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/vGWAS_code.ipynb)

### Example Regenie Commands:
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

## Gene-specific Variance QTL Scan (dglm)

Code available in: [dglm notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/dglm_notebook.ipynb)

### Workflow:
1. Extract variants in gene of interest (MAF > 10%) using plink2
2. Run dglm (v1.8.6) in R (v4.4.0) and filter for significant dispersion P values
3. Run GxG interaction model (See Section 3)

### Example plink2 Command:
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

## Gene-Gene Interaction Testing (gxg)

Code available in: [gene-gene-interaction notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/gene-gene-interaction_code.ipynb)

### Workflow:
1. Run genome-wide association study with Regenie v3.3
2. Find significant interactors
3. Extract significant SNPs using plink
4. Create epistasis plots

### Example Commands:
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

## Power Calculations

Code available in: [Epistasis power calculations notebook](https://github.com/bicklab/gxg-interaction-modeling/blob/main/Epistasis%20power%20calculations.ipynb)

## Dependencies
- Regenie v3.3
- plink2
- R v4.4.0
- dglm v1.8.6

## Data
This analysis was performed using the Terra.bio and the UK Biobank data on the [DNA Nexus Research Analysis Platform] (https://ukbiobank.dnanexus.com). Replication analysis was performed in 1) the BioVU app.Terra.bio environment and 2) the [All of Us Research Workbench](https://workbench.researchallofus.org/).

## Citation
If you use this code or find it helpful, please cite:
Pershad & Poisner et al, medRxiv, 2024. https://doi.org/10.1101/2024.09.18.24313883

## License 
This project is licensed under the MIT License:

MIT License

Copyright (c) [2024] [Yash Pershad]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
Yash Pershad, yash.pershad@vanderbilt.edu
