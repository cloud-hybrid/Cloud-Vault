#!/usr/bin/env python3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

DOCUMENTATION = """
Module: 
Author: Jacob B. Sanders (@cloud-hybrid)
Summary:
Documentation: https://vaultcipher.com/

@Development
- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration

"""

import os
import sys
import time
import json
import shlex
import tempfile
import subprocess

from Vault.Tools.Progress import Progress
from Vault.Tools.HyperThread import HyperThread
from Vault.Tools.Environment import Environment

try:
  import awscli
except:
  install_check = input("PIP dependency {awscli} is not installed. Correct? (Y/N): ")
  if install_check.upper() == "Y":
    command = "pip3 install awscli"
    stream = subprocess.run(command, shell = True)
    time.sleep(5)
    try:
      import awscli
    except:
      sys.exit("Unable to import awscli. Aborting")

class AWSBaseObject(object):
  @property
  def status(self):
    status = False
    return status

  def __init__(self):
    Progress.run("Performing AWS Configuration Checks")
    self.validateConfiguration()

  def validateConfiguration(self):
    if os.path.isfile(f"/Users/{Environment().USERNAME}/.aws/config") == False:
      configure_setup = input("AWS is not configured. Execute setup? (Y/N): ")
      if configure_setup.upper() == "Y":
        time.sleep(0.25)
        print("  ↳ Vault requires {Default Output Format[None]} to be set to {json} ")
        time.sleep(0.25)
        print()
        command = "aws configure"
        subprocess.run(shlex.split(command))
      elif configure_setup.upper() == "N":
        sys.exit("  ↳ AWS Error: awscli is not configured.")
      else:
        sys.exit("  ↳ Input Error: Unknown Input.")
    else:
      print("Validating Configuration File: ")
      Progress.run("Loading")
      with open(f"/Users/{Environment().USERNAME}/.aws/config", "r") as configuration:
        line_list = [line.rstrip('\n') for line in configuration]
        aws_variables = dict()
        for index in line_list:
          if "[" in index and "]" in index and "#" not in index:
            aws_variables["Environment"] = index.replace("[", "").replace("]", "")
          else:
            line_split = index.split()
            key = line_split[0]
            value = index.replace(key, "").replace(" = ", "").replace("=", "")
            aws_variables[key] = value
        
        if aws_variables["output"] != "json" or not aws_variables["output"]:
          print("Validation Failed: Incompatible Output.")
          sys.exit("  ↳ Please reconfigure AWS output to {json}.")
        else:
          if self.validateEndPoints():
            print("Validation was Successful.")
          else:
            print("Validation Failed: Region Error.")
            sys.exit("  ↳ Invalid region(s) entry. Correct entry example: {us-east-1}.")         

  def validateEndPoints(self):
    command = "aws iam get-user"
    stream = subprocess.Popen(
      shlex.split(command),
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True
    )

    output = str(stream.communicate(timeout = 15)[1])
    if "Invalid endpoint" in output:
      return False
    else:
      return True