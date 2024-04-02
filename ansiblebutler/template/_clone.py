import json
import sys
import requests
from ._constants import JOB_TEMPLATE_URL, JT_STRIP_KEYS, RELATED_STRIP_KEYS
from ..common.auth import ControllerAuth

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

def clone_survey(src: str, clone_id: int, auth: ControllerAuth, dry_run=False) -> dict:
  survey_spec = get_related(src, auth)
  if not dry_run:
    resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/survey_spec/", headers=auth.default_headers(), json=survey_spec)
    if resp.status_code not in [200,201]:
      print(f"[template] Failed to clone survey spec\n{resp.content}")
      sys.exit(1)
  return survey_spec

def clone_schedules(src: str, clone_id: int, auth: ControllerAuth, dry_run=False) -> list:
  schedules = get_related(src, auth)
  payloads = []
  for schedule in schedules['results']:
    for key in RELATED_STRIP_KEYS:
      schedule.pop(key, None)
    if not dry_run:
      resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/schedules/", headers=auth.default_headers(), json=schedule)
      if resp.status_code not in [200,201]:
        print(f"[template] Failed to clone schedule(s)\n{resp.content}")
        sys.exit(1)
    payloads.append(schedule)
  return payloads

def clone_labels(src: str, clone_id: int, auth: ControllerAuth, dry_run=False) -> list:
  labels = get_related(src, auth)
  payloads = []
  for label in labels['results']:
    for key in RELATED_STRIP_KEYS:
      label.pop(key, None)
    if not dry_run:
      resp = requests.post(f"https://{auth.host}/api/v2/job_templates/{clone_id}/labels/", headers=auth.default_headers(), json=label)
      if resp.status_code not in [200,201,204]:
        print(f"[template] Failed to clone label(s)\n{resp.content}")
        sys.exit(1)
    payloads.append(label)
  return payloads

def clone_template(name: str, tmpl: dict, auth: ControllerAuth, dry_run=False) -> dict:
  for key in JT_STRIP_KEYS:
    tmpl.pop(key, {})
  tmpl['name'] = name
  if not dry_run:
    resp = requests.post(f"https://{auth.host}/{JOB_TEMPLATE_URL}/", headers=auth.default_headers(), verify=auth.verify_ssl, json=tmpl)
    if resp.status_code not in [200,201]:
      print(f"[template] Failed to clone template with id({id})\n{resp.content}")
      sys.exit(1)
    return resp.json()
  return tmpl

def do_clone(args: dict, config: dict, auth: ControllerAuth):
  dry_run = args.get('--dry-run', False)
  report = {}
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
  report['template'] = clone_template(name, src, auth, dry_run=dry_run)
  if not config['skip_labels']:
    report['labels'] = clone_labels(labels, report['template'].get('id', -1), auth, dry_run=dry_run)
  if not dry_run:
    print(f"[template] Successfully cloned template with id({template_id}). View here: https://{auth.host}/#/templates/job_template/{report['template']['id']}/details")
  # Clone related items
  if not config['skip_survey']:
    report['survey'] = clone_survey(survey_spec, report['template'].get('id', -1), auth, dry_run=dry_run)
    if not dry_run and len(report['survey']):
      print(f"[template] Successfully cloned survey. View here: https://{auth.host}/#/templates/job_template/{report['template']['id']}/survey")
  if not config['skip_schedules']:
    report['schedules'] = clone_schedules(schedules, report['template'].get('id', -1), auth, dry_run=dry_run)
    if not dry_run and len(report['schedules']):
      print(f"[template] Successfully cloned schedules. View here: https://{auth.host}/#/templates/job_template/{report['template']['id']}/schedules")
  # Report
  if dry_run:
    print(json.dumps(report, indent=4))