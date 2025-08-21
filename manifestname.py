import sevenbridges as sbg
import xlsxwriter

c = sbg.Config(profile='default')
api = sbg.Api(config=c)

MANIFEST_PATH = 'manifest_20250731_092827.tsv'
OUTPUT_XLSX = 'file_info.xlsx'

with open(MANIFEST_PATH, 'r') as f:
    ids = [line.strip().split('\t')[0] for line in f if line.strip()]

wb = xlsxwriter.Workbook(OUTPUT_XLSX)
ws = wb.add_worksheet()
headers = [
    'file.name',
    'file.storage.volume',
    "file.storage.volume.service['bucket']",
    'file.storage.volume.storage.location'
]
for col, header in enumerate(headers):
    ws.write(0, col, header)

row = 1
for file_id in ids:
    try:
        file = api.files.get(file_id)
        name = file.name
        src = file.storage.volume
        volume = api.volumes.get(src)
        bucket = volume.service['bucket']
        location = file.storage.location
        ws.write(row, 0, name)
        ws.write(row, 1, src)
        ws.write(row, 2, bucket)
        ws.write(row, 3, location)
    except Exception as e:
        ws.write(row, 0, '')
        ws.write(row, 1, '')
        ws.write(row, 2, '')
        ws.write(row, 3, '')
    row += 1

wb.close()
print(f"Finished writing info for {len(ids)} files to {OUTPUT_XLSX}")
