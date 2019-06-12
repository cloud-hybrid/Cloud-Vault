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
import threading
import subprocess

from Vault.Tools.ASCII import ASCII

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

class Server(object):
  @property
  def status(self):
    status = False
    return status

  def __init__(self):
    
    print("Creating Server Objects:")
    for iterator in '|/-\\': 
      sys.stdout.write(f"  ↳ Performing AWS Configuration Checks" + "... " + iterator + "\r")
      time.sleep(0.25)
      sys.stdout.flush()
    sys.stdout.write(f"  ↳ Performing AWS Configuration Checks" + "... " + ASCII().characters["Success"] + "\n")
    time.sleep(0.25)
    print()
    time.sleep(0.25)
    
    if os.path.exists("~/.aws") == False:
      configure_setup = input("AWS is not configured. Execute setup? (Y/N): ")
      if configure_setup.upper() == "Y":
        time.sleep(0.25)
        print()
        command = "aws configure"
        subprocess.run(shlex.split(command))
      elif configure_setup.upper() == "N":
        sys.exit("  ↳ AWS Error: awscli is not configured.")
      else:
        sys.exit("  ↳ Input Error: Unknown Input.")

class HyperThread(threading.Thread):
  def __init__(self, statement):
    super(HyperThread, self).__init__()
    self.statement = statement

  def run(self):
    while Server.status == True:
      for iterator in '|/-\\': 
        sys.stdout.write(f"  ↳ {self.statement}" + "... " + iterator + "\r")
        time.sleep(0.25)
        sys.stdout.flush()
    sys.stdout.write(f"  ↳ {self.statement}" + "... " + ASCII().characters["Success"] + "\n")