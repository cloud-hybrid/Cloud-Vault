#!/usr/bin/env python3.7.3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

DOCUMENTATION = """
Module: 
Author: Jacob B. Sanders (@cloud-hybrid)
Summary:
- Requires SSH and Access Keys have been created on GitLab.
Documentation: https://vaultcipher.com/
- Dual Authentication must be enabled. 

@Development
- Projects are often referred to as a repository, which they are, 
  but really they are either a Group or Sub-Group. 
- If receiving: 
  urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)>
  Navigate to the Python root directory and open "Install Certificates.command"
"""
import sys
import time
import textwrap
import subprocess

try:
  import gitlab
except:
  install_check = input("PIP dependency {python-gitlab} is not installed. Correct? (Y/N): ")

  if install_check.upper() == "Y":
    command = "pip3 install python-gitlab"
    stream = subprocess.run(command)

    import gitlab

class LabVault(object):
  def __init__(self, private_access_key: str, gitlab_url: str = "https://gitlab.com"):
    for iterator in '|/-\\'*3 + "✔": 
      sys.stdout.write(f"  ↳ Initializing GitLab Wrappers" + "... " + iterator + "\r")
      sys.stdout.flush()
      time.sleep(0.25)
    print("\n")

    self.URL = gitlab_url
    self.API_Key = private_access_key
    self.gitlab = gitlab.Gitlab(self.URL, private_token = self.API_Key)

    self.characters = {
      "Bullet" : "◯",
      "Bullet-Full" : "●",
      "Bullet-Semi" : "◔",
      "Success" : "✔",
      "Failure" : "✕",
      "Progress-Empty" : "░",
      "Progress-Semi" : "▓",
      "Progress-Full" : "█"
    }

  def createConfiguration(self):
    """ Creates a default gitlab configuration file used by python-gitlab. """ 
    # Note: Need to find the .cfg file location and name, and open and write
    # to it

    template = textwrap.dedent(
      f"""
      [global]
      default = gitLab
      ssl_verify = true
      timeout = 15

      [gitLab]
      url = {self.URL}
      private_token = {self.API_Key}
      api_version = 4
      """
    ).strip()

    configuration = template
    return configuration

  def listDirectories(self):
    """ STDOUT::Prints GitLab Groups, Subgroups, and Projects """ 
    TAB = "  " + "↳" + " "
    TAB2 = "  " * 4 

    total_groups = 0
    total_projects = 0 

    Groups = self.gitlab.groups.list(as_list = True)
    for Group in Groups:
      print()
      print("Group: " + Group.name)
      print(f"{TAB}Projects: ")
      total_groups += 1
      for Project in Group.projects.list(as_list = True):
        print(f"{TAB2}○ " + Project.name)
        total_projects += 1

    print()
    print("Total Groups: " + str(total_groups))
    print()
    print("Total Projects: " + str(total_projects))
    print()

    Groups = self.gitlab.groups.list(as_list = True)

    # for Group in Groups:
    #   print("  Group:")
    #   print("    " + self.characters["Bullet"] + " " + Group.name)
    #   subgroups = Group.subgroups.list(as_list = True)
    #   if subgroups:
    #     for Subgroup in subgroups:
    #       print("    " + "Subgroups: ")
    #       print("      " + Subgroup.name)
    #   else:
    #     pass

  def cloneRepositories(self):
    pass

  @property
  def Key(self) -> str:
    property = self.API_Key
    return property

  @property
  def Information(self):
    pass