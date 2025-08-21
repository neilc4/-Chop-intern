import sys
import os
import csv
import xlsxwriter

def main(manifest_file):
    bam_count = 0
    fqgz_count = 0
    bam_size = 0
    fqgz_size = 0
    total_files = 0


    with open(manifest_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')  
        for row in reader:
            filename = row.get('name') or row.get('Filename') or ''
            size_str = row.get('size') or row.get('Size') or '0'
            try:
                size = int(size_str)
            except ValueError:
                size = 0

            total_files += 1

            if filename.endswith('.bam'):
                bam_count += 1
                bam_size += size
            elif filename.endswith('.fq.gz') or filename.endswith('.fastq.gz'):
                fqgz_count += 1
                fqgz_size += size

  
    workbook = xlsxwriter.Workbook('file_summary.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'File Type')
    worksheet.write('B1', 'Count')
    worksheet.write('C1', 'Total Size (GB)')

    worksheet.write('A2', 'BAM')
    worksheet.write('B2', bam_count)
    worksheet.write('C2', round(bam_size / (1024**3), 2))

    worksheet.write('A3', 'FQ.GZ')
    worksheet.write('B3', fqgz_count)
    worksheet.write('C3', round(fqgz_size / (1024**3), 2))

    worksheet.write('A4', 'TOTAL FILES')
    worksheet.write('B4', total_files)

    workbook.close()

    print("Excel file 'file_summary.xlsx' has been created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <manifest_file>")
        sys.exit(1)
    main(sys.argv[1])
