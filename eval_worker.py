from pathlib import Path
import subprocess
import json


submission_folder = Path('./example_submission').resolve()

docker_image = "quay.io/jupyter/scipy-notebook:2026-03-02"


cmd = f"""
docker run --rm --cpus=1 \
   --stop-timeout 1 \
  -v "{submission_folder}:/work" \
  -w /work \
  --user "$(id -u):$(id -g)" \
  --entrypoint bash {docker_image} \
  -c 'TIMEFORMAT="CPU %6U %6S"; {{ time python example_script.py >/dev/null; }} 2>&1 | awk "/^CPU /{{print \\$2+\\$3}}"'
"""

time_limit = 60

try:
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=time_limit,   # wall clock seconds
    )
except subprocess.TimeoutExpired as e:
    # docker run got killed by Python after 60s
    # e.stdout / e.stderr may exist
    timed_out = True
    print("Time out")


print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("return code:", result.returncode)

outputed_file = submission_folder / 'example_output.json'
if outputed_file.exists():
    print("Output generated sucesfully!")
    
    with open(outputed_file) as file:
        sumbission_solution = json.load(file)    
    
    reference_solution_file = submission_folder / 'reference_solution.json'
    with open(reference_solution_file) as file:
        reference_solution = json.load(file)
        
    match_reference = reference_solution['result'] == sumbission_solution['result']    
    
    
else:
    print("No output generated")
    pass # No output provided
    
    
