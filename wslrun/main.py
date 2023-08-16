import os
import json
import subprocess
from pprint import pprint
import sys
import getopt
import yaml
from pkg_resources import get_distribution, DistributionNotFound
import argparse

def version_info():
    dist = get_distribution('py-wslrun')
    return f"wslrun {dist.version}"

def image_check(image):
    proc = subprocess.Popen(f"wsl -d {image} --exec uname", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        continue
    image_exit_code = proc.wait()
    return image_exit_code

# def cmd_exit(command, image):
#     cmd_str = f"wsl -d {image} --exec {command}"

#     print(f"wslExec (image: {image}): {command}")
#     proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     while proc.poll() is None:
#         continue
#     command_result = proc.wait()
#     return {'exit_code': command_result}

def execute_wsl_command(command, image):
    process = subprocess.run(['wsl', '-d', image, '--', 'bash', '-c', command], capture_output=True, text=True)
    return process.returncode, process.stdout.strip(), process.stderr.strip()

def execute_steps(steps, image):
    stats = []
    exits = []
    completed = {}
    for k, v in enumerate(steps):
        # command_runner = cmd_exit(v, image)
        step = {}
        step['id'] = k
        print(f'Executing command: {step}')
        returncode, output, errout = execute_wsl_command(v, image)
        step['exit_code'] = returncode
        step['cmd'] = v
        stats.append(step)
        exits.append(returncode)
        if returncode == 0:
            print(f"✔️: {v}\n")
        else:
            print(f"❌: {v}\n")
        print(f'Return code: {returncode}')
        print(f'STDOUT: {output}')
        print(f'STDERR: {errout}')
        print('-' * 30)
    completed['completions'] = f"{exits.count(0)}/{len(exits)}"
    stats.append(completed)
    return stats

def manifest_read(manifest_path):
    try:
        with open(manifest_path, "rt") as manifest_json:
            manifest = yaml.safe_load(manifest_json)
        return manifest
    except OSError as e:
        return e

def define_pipeline(manifest_path):
    manifest = manifest_read(manifest_path)
    if isinstance(manifest, OSError):
        print(manifest)
        exit(2)
    pipeline = []
    for stage in manifest['stages']:
        stage_data = {}
        stage_data['name'] = stage['name']
        image_status = image_check(stage['image'])
        if image_status == 0:
            job = execute_steps(stage['steps'], stage['image'])
            print(f"🔔: {stage['name']} completed.")
            stage_data['stages_run'] = job
        else:
            stage_data['stages_run'] = [{"completions": f"0/0, Image {stage['image']} Unavailable: {image_status}"}]
        pipeline.append(stage_data)
    return pipeline
    
def run_pipeline(pipeline_definition):
    pipeline = define_pipeline(pipeline_definition)
    
    print("Pipeline completed:\n")
    for job in pipeline:
        print(f"🧾 Report: {job['name']}...\n")
        for j in job['stages_run']:
            if 'completions' in j:
                pprint(j)
                print("\n")
    return "Completed."

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pipeline', help="Path to pipeline file (i.e. build.json, build.yaml")
    parser.add_argument('-v', '--version', help="wslrun version", action='store_true')

    args = parser.parse_args()

    if args.pipeline is not None:
        pipeline = args.pipeline
        print(run_pipeline(pipeline))

    if args.version is not None:
        print(version_info())