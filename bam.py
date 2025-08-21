import sevenbridges as sbg
from sevenbridges.errors import BadRequest

# Load Seven Bridges config from ~/.sevenbridges/credentials
c = sbg.Config(profile='default')
api = sbg.Api(config=c)

PROJECT_NAME = "Neil_c4/test"
APP_NAME = "Neil_c4/test/kfdrc-rnaseq-workflow"

# Get project
project = api.projects.get(PROJECT_NAME)
print(f"Using project: {project.name}")

# Get app
app = api.apps.get(APP_NAME)
print(f"Using app: {app.name}")

# Find BAM file
bam_file = None
for f in api.files.query(project=PROJECT_NAME).all():
    if f.name.endswith(".bam"):
        bam_file = f
        break

if not bam_file:
    raise Exception("No BAM file found in project.")
print(f"Found BAM file: {bam_file.name} (ID: {bam_file.id})")

# Set initial inputs (without output_basename yet)
inputs = {
    "input_alignment_files": [bam_file],
    "is_paired_end": True,
    "sample_name": "BS_J26K22NC"
}

try:
    # Create draft task
    task = api.tasks.create(
        name="Kids First DRC RNAseq Workflow run",
        project=project.id,
        app=app.id,
        inputs=inputs
    )

    # Now set output_basename to task ID and save
    task.inputs['output_basename'] = task.id
    task.save()

    print(f"Draft task created: {task.id}")
    print("Task inputs:")
    for k, v in task.inputs.items():
        print(f"  {k}: {v}")

except BadRequest as e:
    print("BadRequest:", e)
    if hasattr(e, "body"):
        print("Server response:", e.body)
