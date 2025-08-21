import argparse
import sevenbridges as sbg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pjt", required=False, default="neil_c4/test", help="Project ID")
    parser.add_argument("-input_file", required=True, help="Manifest file path")
    args = parser.parse_args()

    c = sbg.Config(profile='default')
    api = sbg.Api(config=c)

    project = args.pjt
    app = 'neil_c4/test/samtools-index-1-20'

    bam_files = []
    with open(args.input_file) as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) < 2 or "id" in fields[0]:
                continue
            bam_files.append(fields[1])

    if len(bam_files) < 2:
        raise ValueError("At least two BAM files are required to create two tasks.")

    file_objects = api.files.query(project=project, names=bam_files)

    for i in range(2): 
        bam_file_name = bam_files[i]
        inputs = {'in_alignments': [file_objects[i]]}
        try:
            task = api.tasks.create(
                name=f'samtools index run {bam_file_name}',
                project=project,
                app=app,
                inputs=inputs,
                run=False
            )
            print(f"Task {i+1} created: {task.id}")
        except Exception as e:
            print(f"I was unable to run task {i+1}: {e}")

if __name__ == "__main__":
    main()
