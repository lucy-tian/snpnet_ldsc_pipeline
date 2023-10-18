#!/bin/bash

# Parent directory where phenotype directories are located
base_directory="${1}/406k_geno_v2_UKB_18PCs/fit_w_val"

# Iterate over directories in the base directory
for directory in "$base_directory"/*; do
    if [ -d "$directory" ]; then
        # Check if snpnet.sscore.zst file exists in the current directory
        file_path="$directory/snpnet.sscore.zst"
        if [ -f "$file_path" ]; then
            echo "Decompressing $file_path..."
            
            # Specify output file name (e.g., snpnet.sscore)
            output_file_name="$directory/snpnet.sscore.txt"
            
            # Decompress the .zst file to the output file
            zstd -d "$file_path" -o "$output_file_name"
            
            echo "Decompressed $file_path to $output_file_name"
        fi
    fi
done
