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

  def __init__(self, environment = None):
    Progress.run("Performing AWS Configuration Checks")
    self.aws_configuration = self.validateConfiguration()
    self.aws_credentials = self.validateCredentials()

    self.aws_variables = {**self.aws_configuration, **self.aws_credentials}

    if environment == None:
      self.aws_environment = self.aws_variables["Environment-Default"]
    else:
      self.aws_environment = self.aws_variables[f"Environment-{environment}"]

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
            aws_variables["Environment-" + str(index).title().replace("[", "").replace("]", "")] = index
          elif "#" in index:
            pass
          else:
            line_split = index.split()
            if len(line_split) > 0:
              key = line_split[0]
              value = index.replace(key, "").replace(" = ", "").replace("=", "")
              aws_variables[key] = value

        if aws_variables["output"]:
          if aws_variables["output"] != "json":
            print("Validation Failed: Incompatible Output.")
            sys.exit("  ↳ Please reconfigure AWS output to {json}.")
          else:
            print("Configuration Validation was Successful." + "\n")
            return aws_variables
        else:
          print("Validation Failed: Default output N/A.")
          correct = input("  ↳ Correct? (Y/N): ")
          if correct.upper() == "Y":
            with open(f"/Users/{Environment().USERNAME}/.aws/config", "a") as configuration:
              configuration.write("output = json")
            configuration.close()
            Progress.run("Updating Configuration File")
            self.validateConfiguration()
          else:
            sys.exit("  ↳ Please add output = json in ~/.aws/config")

  def validateCredentials(self):
    if os.path.isfile(f"/Users/{Environment().USERNAME}/.aws/credentials") == False:
      configure_setup = input("AWS credentials do not exist. Execute setup? (Y/N): ")
      if configure_setup.upper() == "Y":
        time.sleep(0.25)
        print()
        command = "aws configure"
        subprocess.run(shlex.split(command))
      elif configure_setup.upper() == "N":
        sys.exit("  ↳ AWS Error: awscli is not configured.")
      else:
        sys.exit("  ↳ Input Error: Unknown Input.")
    else:
      print("Validating Credentials File: ")
      Progress.run("Loading")
      with open(f"/Users/{Environment().USERNAME}/.aws/credentials", "r") as credentials:
        line_list = [line.rstrip('\n') for line in credentials]
        aws_variables = dict()
        env_variables = dict()
        env_key = None
        for index in line_list:
          if "[" in index and "]" in index and "#" not in index:
            env_key = "Environment-" + str(index).title().replace("[", "").replace("]", "")
            env_variables[env_key] = {"Environment" : index}
          elif "#" in index:
            pass
          else:
            line_split = index.split()
            if len(line_split) > 0:
              if line_split[0] == "aws_access_key_id":
                key = line_split[0]
                value = index.replace(key, "").replace(" = ", "").replace("=", "")
                env_variables[env_key].update({key : value})
                aws_variables = {**aws_variables, **env_variables}
              elif line_split[0] == "aws_secret_access_key":
                key = line_split[0]
                value = index.replace(key, "").replace(" = ", "").replace("=", "")
                env_variables[env_key].update({key : value})
                aws_variables = {**aws_variables, **env_variables}

      Progress.run("Reading Environment and Credential Variables")
      print("Credential Validation was Successful." + "\n")
      time.sleep(0.5)
      return aws_variables