import subprocess
import argparse

parser = argparse.ArgumentParser(description = 'Arguments for generating commands file')

parser.add_argument('--output_folder', '-of', type=str, required=True, help='Path to output folder, must use double quotes')
parser.add_argument('--output_file', '-ofi', type=str, required=True, help='Command File name, must use double quotes')
parser.add_argument('--pheno', '-p', type=str, required=True, help='Phenotype File use id from DNANexus')
parser.add_argument('--covariate', '-c', type=str, required=True, help='Covaraite File use id from DNANexus')
parser.add_argument('--pheno_name', '-pn', type=str, required=True, help='Phenotype Name')
parser.add_argument('--prefix', '-pre', type=str, required=True, help='File Prefix Name')

args = parser.parse_args()

OUTPUT_FOLDER = args.output_folder
output_file = args.output_file

with open("batch_file.txt") as file, open(output_file, "w") as outfile:
    next(file)  # Skip header line
    for line in file:
        fields = line.strip().split('\t')
        chr, igenotype_bgens, igenotype_bgis, igenotype_samples, istep2_extract_txts_raw = fields[:5]
        
        # Remove newline character
        istep2_extract_txts = istep2_extract_txts_raw.replace('\n', '')

        # Construct dx run command
        cmd = f'''dx run app-regenie \
            --priority low \
            --instance-type "mem1_ssd1_v2_x36" \
            --tag="chr{chr}_{args.pheno_name}" \
            -iwgr_genotype_bed="file-GgbZ2j8JK90fK3XY9GjQpJ9J" \
            -iwgr_genotype_bim="file-GgbZ2j8JK90vfYpq1X91jjVg" \
            -iwgr_genotype_fam="file-GgbZ2j8JK90zP4QY0FPvg2z0" \
            -igenotype_bgens="{igenotype_bgens}" \
            -igenotype_bgis="{igenotype_bgis}" \
            -igenotype_samples="{igenotype_samples}" \
            -ipheno_txt="{args.pheno}" \
            -icovar_txt="{args.covariate}" \
            -iquant_traits="true" \
            -ipheno_names="{args.pheno_name}" \
            -icovar_names="baseline_age,age2,PC1,PC2,PC3,PCD4,PC5,PC6,PC7,PC8,PC9,PC10" \
            -istep1_block_size=1000 \
            -istep2_block_size=200 \
            -ioutput_prefix="{args.prefix}" \
            -iprs_mode="false" \
            -ipvalue_threshold=0.05 \
            -iuse_firth_approx="true" \
            -itest_type="additive" \
            -istep1_extract_txts="file-Gj8J14jJ2p5VK7Y9xvxX3XP0" \
            -istep2_extract_txts="{istep2_extract_txts}" \
            -istep1_ref_first="false" \
            -istep2_ref_first="true" \
            -istep1_extra_cmd_line_args="--catCovarList genetic_sex --apply-rint" \
            -istep2_extra_cmd_line_args="--catCovarList genetic_sex --apply-rint" \
            --destination "{OUTPUT_FOLDER}" \
            -y --brief \
            --ignore-reuse\n'''
        
        # Write command to output file
        outfile.write(cmd)

# Execute the commands from the file using subprocess if needed
# subprocess.run(f"bash {output_file}", shell=True)

# Execute outside of this script on the CLI
# sh commands.txt
