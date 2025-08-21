import sevenbridges as sbg
import csv

c = sbg.Config(profile='default')
api = sbg.Api(config=c)

project = 'kfdrc-harmonization/sd-bhjxbdqk-x01-rnaseq-analysis-lt-50m'
tasks = api.tasks.query(project=project, status='COMPLETED').all()
rows = []
for task in tasks:
    task_id = task.id
    task_name = task.name
    outputs = task.outputs
    for key, value in outputs.items():
        files = value if isinstance(value, list) else [value]
        for file in files:
            if hasattr(file, 'id') and hasattr(file, 'name') and hasattr(file, 'size'):
                rows.append([
                    task_id,
                    task_name,
                    file.id,
                    file.name,
                    file.size
                ])
with open('completed_tasks_outputs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['task_id', 'task_name', 'file_id', 'file_name', 'file_size'])
    writer.writerows(rows)