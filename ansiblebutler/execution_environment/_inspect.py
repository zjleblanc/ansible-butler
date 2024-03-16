import sys
import os
import shutil
import subprocess
import json
import yaml

AUTO='auto'
PODMAN='podman'
DOCKER='docker'
TMP_PYTHON='/tmp/butler-ee-inspect-requirements.txt'
TMP_GALAXY='/tmp/butler-ee-inspect-collections.json'

def _determine_engine(config: str):
  current = config.lower()
  # config specified podman
  if current == PODMAN:
    if shutil.which(PODMAN):
      return current
    print("[ee inspect] podman not found in path")
  # config specified podman
  elif current == DOCKER:
    if shutil.which(DOCKER):
      return current
    print("[ee inspect] docker not found in path")
  # try podman, fallback to docker
  elif current == AUTO:
    if shutil.which(PODMAN):
      return PODMAN
    elif shutil.which(DOCKER):
      return DOCKER
    print("[ee inspect] Neither podman or docker found in path")
  # no container engine present
  sys.exit(1)

def _inspect_python(engine: str, image: str):
  rc = -1
  with open(TMP_PYTHON, "w") as reqs:
    rc = subprocess.call(f"{engine} run --rm -q {image} python3 -m pip freeze", shell=True, stdout=reqs, stderr=reqs)
  with open(TMP_PYTHON, "r") as reqs:
    if rc == 0:
      libs = filter(lambda l: not l.startswith("WARNING"), reqs)
      libs_stripped = map(lambda r: r.rstrip(), libs)
      return list(libs_stripped)
    else:
      raise Exception("failed to determine python libraries")
    
def _inspect_galaxy(engine: str, image: str):
  rc = -1
  with open(TMP_GALAXY, "w") as colls:
    rc = subprocess.call(f"{engine} run --rm {image} ansible-galaxy collection list --format json", shell=True, stdout=colls, stderr=colls)
  with open(TMP_GALAXY, "r") as colls:
    if rc == 0:
      raw = colls.readlines()
      return json.loads(raw[-1])
    else:
      raise Exception("failed to determine python libraries")
    
def _print_report(report: dict, format: str):
  if format.lower() == 'yaml':
    print(yaml.dump(report))
  elif format.lower() == 'json':
    print(json.dumps(report))
  else:
    raise Exception(f"invalid format specified in config: {format}")

def inspect_ee(image: str, config: dict):
  engine = _determine_engine(config.get('engine'))
  report = {}

  failed = False
  try:
    report["python"] = _inspect_python(engine, image)
    report["galaxy"] = _inspect_galaxy(engine, image)
    _print_report(report, config['format'])
  except Exception as ex:
    print(f"[ee inspect] {ex}")
    failed = True
  finally:
    if os.path.exists(TMP_PYTHON):
      os.remove(TMP_PYTHON)
    if os.path.exists(TMP_GALAXY):
      os.remove(TMP_GALAXY)
    if failed:
      sys.exit(1)