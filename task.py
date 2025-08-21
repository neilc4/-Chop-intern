import sevenbridges as sbg
import csv

c = sbg.Config(profile='default')
api = sbg.Api(config=c)

project = 'kfdrc-harmonization/sd-bhjxbdqk-x01-rnaseq-analysis-lt-50m'


rows = []
for task in api.tasks.query(project=project, status='COMPLETED').all():
    task_id = task.id
    task_name = task.name
    start_time = task.start_time
    end_time = task.end_time
    cost = getattr(task, 'price', None)


    if start_time and end_time:
        run_time_mins = round((end_time - start_time).total_seconds() / 60)
    else:
        run_time_mins = None

    if cost is not None and hasattr(cost, 'amount'):
        cost_str = f"${cost.amount:.2f}"
    else:
        cost_str = "N/A"

    rows.append([task_id, task_name, run_time_mins, cost_str])

with open('completed_tasks_info.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['task_id', 'task_name', 'total_run_time_minutes', 'task_cost_usd'])
    writer.writerows(rows)

rows = []
tasks = api.tasks.query(project=project, status='COMPLETED').all()
for task in tasks:
    task_id = task.id
    task_name = task.name
    outputs = task.outputs
    for key, value in outputs.items():
        files = value if isinstance(value, list) else [value]
        for file in files:
            if hasattr(file, 'id') and hasattr(file, 'name') and hasattr(file, 'size'):
                rows.append([task_id, task_name, file.id, file.name, file.size])

with open('completed_tasks_outputs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['task_id', 'task_name', 'file_id', 'file_name', 'file_size'])
    writer.writerows(rows)
