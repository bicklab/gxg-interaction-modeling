# Variance quantitative trait loci reveal gene-gene interactions which alter blood traits

Github repo for Pershad & Poisner et al, medRxiv, 2024. https://doi.org/10.1101/2024.09.18.24313883.


<!--ts-->
   * [Genome-wide variance QTL scan (Scale test)](#scale)
   * [Gene-specific variance QTL scan (dglm)](#dglm)
   * [Gene-gene interaction testing (gxg)](#gxg)
<!--te-->

## Genome-wide variance QTL scan (Scale test)

Functions in vGWAS_code.ipynb

1. Inverse normal transform traits
2. Calculate residual and square it
3. Run genome wide association study with Regenie v3.3 on both rank-inverse normalized trait (mean) and square of the residual of the rank-inverse-normalized trait (variance). Covariates were age at blood draw, age at blood draw2, sex, genetic ancestry, and the first 5 genotyping principal components.
```
# Ran on the DNANexus UK Biobank Research Analysis Platform - example below.

```
5. Select SNPs with if they had a genome-wide significant association with the variance of a trait ($P < 5x10^{-8}$) without a significant mean effect after multiple-hypothesis correction ($P > 5x10^{-8}$).
6. Run GxG interaction model (Section 3)


## Gene-specific variance QTL scan (dglm)


## Gene-gene interaction testing (gxg)




