#!/usr/bin/env python3.7.3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

METADATA = {
  "Module" : "N/A",
  "Package" : "CloudVault",
  "Version" : "0.2",
  "Status" : "Beta::Working",
  "Update-Signature" : "07-01-2019"
  }

DOCUMENTATION = """
Module: N/A
Author: Jacob B. Sanders (@cloud-hybrid)
Summary: The entry point for the program.
Description:

Dependencies:
- python-gitlab (PIP3)
- brew
- envchain (brew)

@Development:
- Create a scanEmptyDirectories function in GitLab.py.
  - Have it get the following information:
    - Group Name
    - URL
    - Last Edit
    - Owners
    - Owner-Email

- Change the current method of capitializing Group/Project
  names to a better method where - and _ aren't being 
  replaced with spaces. Only capitalize the letters if
  seperated with " ", _, -.
  - Capitalize Projects. 

- Move private_key from __main__ to GitLab.py
"""

EXAMPLES = """
def main(argv):
  project = GitProject()
  print(project.Key)

  project.listRepositories()

  env = Environment()

  env.printPublicKey()
"""

import os
import sys

from Vault.Tools.Environment import Environment
from Vault.GitLab.LabVault import LabVault
from Vault.IaaS.AWS.AWSBaseObject import AWSBaseObject

def main(argv):
  # private_key = os.environ["GITLAB_API_TOKEN"]

  # GitLab = LabVault(private_access_key = private_key, gitlab_url = "https://gitlab.healthcareit.net")
  # GitLab.printRepositories()
  # GitLab.cloneAllRepositories()

  GitLabServer = AWSBaseObject()

if __name__ == "__main__":
  main(sys.argv)

  