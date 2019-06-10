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
"""

EXAMPLES = """
::Print Public Key
def main(argv):
  project = GitProject()
  print(project.Key)

  project.listRepositories()

  env = Environment()

  env.printPublicKey()
"""

import os
import sys

from Vault.VaultTools.Environment import Environment
from Vault.GitLab.LabVault import LabVault

def main(argv):
  private_key = os.environ["VAULT_LAB_API_TOKEN"]

  GitLab = LabVault(private_key)
  # GitLab.printRepositories()
  GitLab.cloneAllRepositories()

if __name__ == "__main__":
  main(sys.argv)
  