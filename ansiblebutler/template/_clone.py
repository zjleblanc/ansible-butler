import os
import json
import sys
import requests
from ._constants import JOB_TEMPLATE_URL, JT_STRIP_KEYS, RELATED_STRIP_KEYS
from ..common.auth import ControllerAuth, get_controller_auth

def get_template_definition(id: str, auth: ControllerAuth) -> dict:
  resp = requests.get(f"https://{auth.host}/{JOB_TEMPLATE_URL}/{id}", headers=auth.default_headers(), verify=auth.verify_ssl)
  if resp.status_code == 404:
    print(f"[template] Job template not found with id({id}) - support for workflow job templates coming soon")
    sys.exit(1)
  if resp.status_code not in [200,201]:
    print(f"[template] Failed to get template with id({id})\n{resp.content}")
    sys.exit(1)
  return resp.json()

def get_related(url: str, auth: ControllerAuth) -> dict:
  resp = requests.get(f"https://{auth.host}{url}", headers=auth.default_headers())
  if resp.status_code not in [200,201]:
    print(f"[template] Failed to get related resource\n{resp.content}")
    sys.exit(1)
  return resp.json()

def clone_survey(src: str, clone_id: int, auth: ControllerAuth) -> bool:
  survey_spec = get_related(src, auth)
  if len(survey_spec) == 0:
    return False
  resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/survey_spec/", headers=auth.default_headers(), json=survey_spec)
  if resp.status_code not in [200,201]:
    print(f"[template] Failed to clone survey spec\n{resp.content}")
    sys.exit(1)
  return True

def clone_schedules(src: str, clone_id: int, auth: ControllerAuth) -> bool:
  schedules = get_related(src, auth)
  if not schedules['count'] > 0:
    return False
  for schedule in schedules['results']:
    for key in RELATED_STRIP_KEYS:
      schedule.pop(key, None)
    resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/schedules/", headers=auth.default_headers(), json=schedule)
    if resp.status_code not in [200,201]:
      print(f"[template] Failed to clone schedule(s)\n{resp.content}")
      sys.exit(1)
  return True

def clone_labels(src: str, clone_id: int, auth: ControllerAuth) -> None:
  labels = get_related(src, auth)
  if not labels['count'] > 0:
    return
  for label in labels['results']:
    for key in RELATED_STRIP_KEYS:
      label.pop(key, None)
    resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/labels/", headers=auth.default_headers(), json=label)
    if resp.status_code not in [200,201,204]:
      print(f"[template] Failed to clone label(s)\n{resp.content}")
      sys.exit(1)

def clone_template(name: str, tmpl: dict, auth: ControllerAuth) -> dict:
  stripped = {}
  for key in JT_STRIP_KEYS:
    stripped[key] = tmpl.pop(key, {})
  tmpl['name'] = name
  resp = requests.post(f"https://{auth.host}/{JOB_TEMPLATE_URL}/", headers=auth.default_headers(), verify=auth.verify_ssl, json=tmpl)
  if resp.status_code not in [200,201]:
    print(f"[template] Failed to clone template with id({id})\n{resp.content}")
    sys.exit(1)
  return resp.json()

def do_clone(args: dict, config: dict, auth: ControllerAuth):
  # Get source
  template_id = args['<id>']
  src = get_template_definition(template_id, auth)
  survey_spec = src['related']['survey_spec']
  schedules = src['related']['schedules']
  labels = src['related']['labels']
  # Clone template
  name = args.get('<name>')
  if not name:
    name = src["name"] + " [CLONE]"
  clone = clone_template(name, src)
  if not config['skip_labels']:
    clone_labels(labels, clone['id'], auth)
  print(f"[template] Successfully cloned template with id({template_id}). View here: https://{auth.host}/#/templates/job_template/{clone['id']}/details")
  # Clone related items
  if not config['skip_survey']:
    if clone_survey(survey_spec, clone['id'], auth):
      print(f"[template] Successfully cloned survey. View here: https://{auth.host}/#/templates/job_template/{clone['id']}/survey")
  if not config['skip_schedules']:
    if clone_schedules(schedules, clone['id'], auth):
      print(f"[template] Successfully cloned schedules. View here: https://{auth.host}/#/templates/job_template/{clone['id']}/schedules")