#!/usr/bin/env python3
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

import os
import sys
import time
import textwrap
import threading
import subprocess
import getpass
import concurrent.futures as ThreadPool

from Vault.VaultTools.Environment import Environment
from Vault.VaultTools.Illustrate import Illustrate

try:
  import gitlab
except:
  install_check = input("PIP dependency {python-gitlab} is not installed. Correct? (Y/N): ")
  if install_check.upper() == "Y":
    command = "pip3 install python-gitlab"
    stream = subprocess.run(command, shell = True)
    time.sleep(15)
    try:
      import gitlab
    except: 
      command = "sudo pip3 install python-gitlab"
      stream = subprocess.run(command, shell = True)
      time.sleep(15)
      import gitlab

class LabVault(object):
  @property
  def status(self):
    status = False
    return status

  # def __init__(self, private_access_key: str, gitlab_url: str = "https://gitlab.healthcareit.net"):
  def __init__(self, private_access_key: str, gitlab_url: str = "https://gitlab.com"):
    for iterator in '|/-\\' + "✔": 
      sys.stdout.write(f"  ↳ Initializing GitLab Wrappers" + "... " + iterator + "\r")
      sys.stdout.flush()
      time.sleep(0.25)
    print("\n")

    self.URL = gitlab_url
    self.API_Key = private_access_key
    self.https_username = input("Gitlab Username: ")
    self.https_password = getpass.getpass(prompt = "  " + Illustrate().characters["Arrow-Down-Right"] + " " + "Password: ")

    print()

    self.gitlab = gitlab.Gitlab(self.URL, private_token = self.API_Key, http_username = self.https_username, http_password = self.https_password)

    self.progress = False

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

  def printRepositories(self, order_type = "path"):
    """ STDOUT::Prints GitLab Groups, Subgroups, and Projects """ 
    TAB = " " * 2

    Groups = self.gitlab.groups.list(order_by = order_type, as_list = True)

    for Group in Groups:
      Projects = Group.projects.list(as_list = True)
      if Projects and not Group.subgroups.list():
        print(Group.name)
        for Project in Projects:
          print(f"{TAB}○" + " " + Project.name)
        print()

  def cloneAllRepositories(self, directory = None):
    TAB = " " * 2

    if directory == None:
      default = input("Targeted Clone Directory: NULL. Use $HOME Directory? (Y/N): ")
      if default.upper() == "N":
        directory = input("Path: ")
        if not os.path.exists(directory):
          sys.exit("Unable to Clone Repository. Local Directory Not Found")
      elif default.upper() == "Y":
        if Environment.PLATFORM == "Darwin":
          directory = Environment().MacOSHomeDirectory
        elif Environment.PLATFORM == "Linux":
          directory = Environment().LinuxHomeDirectory
        elif Environment.PLATFORM == "Windows":
          directory = Environment().WindowsHomeDirectory
        else:
          sys.exit("Error: Unsupported Operating System")
      else:
        sys.exit("Unknown Input")
    else:
      if not os.path.exists(directory):
        sys.exit("Unable to Clone Repository. Local Directory Not Found")

    if Environment.PLATFORM == "Darwin":
      vault_directory = directory + "Vault Gitlab/"
    elif Environment.PLATFORM == "Linux":
      vault_directory = directory + "Vault Gitlab/"
    elif Environment.PLATFORM == "Windows":
      vault_directory = directory + "Vault Gitlab\\"

    if not os.path.exists(vault_directory):
      LabVault.status = True
      HyperThread("Creating Gitlab Directory").start()
      self.createGitlabDirectory(vault_directory)
      LabVault.status = False
      time.sleep(2.5)
      print()

    Groups = self.gitlab.groups.list(as_list = True, order_by = "path")

    projects_cloned = 0

    for Group in Groups:
      if Environment.PLATFORM == "Darwin":
        directory = vault_directory + Group.full_path
        directory = directory.replace("-", " ")
        directory = directory.replace("_", " ")
        directory = directory.title()
      elif Environment.PLATFORM == "Linux":
        directory = vault_directory + Group.full_path
        directory = directory.replace("-", " ")
        directory = directory.replace("_", " ")
        directory = directory.title()
      elif Environment.PLATFORM == "Windows":
        directory = vault_directory + Group.full_path
        directory = directory.replace("/", "\\")
        directory = directory.replace("-", " ")
        directory = directory.replace("_", " ")
        directory = directory.title()

      print(Group.web_url)

      if not os.path.exists(directory):
        LabVault.status = True
        HyperThread("Creating Directory").start()
        self.createGitlabDirectory(directory)
        LabVault.status = False
        time.sleep(0.5)
        print()

      Projects = Group.projects.list(as_list = True)
      if Projects and not Group.subgroups.list():
        for Project in Projects:
          if Environment.PLATFORM == "Darwin":
            directory = vault_directory + Group.full_path
            directory = directory.replace("-", " ")
            directory = directory.replace("_", " ")
            directory = directory.title()
          elif Environment.PLATFORM == "Linux":
            directory = vault_directory + Group.full_path
            directory = directory.replace("-", " ")
            directory = directory.replace("_", " ")
            directory = directory.title()
          elif Environment.PLATFORM == "Windows":
            directory = vault_directory + Group.full_path
            directory = directory.replace("/", "\\")
            directory = directory.replace("-", " ")
            directory = directory.replace("_", " ")
            directory = directory.title()

          execution_location = os.getcwd()

          os.chdir(directory)

          if Environment.PLATFORM == "Darwin":
            command = f"git clone {Project.web_url}" + ".git"
          elif Environment.PLATFORM == "Linux":
            command = f"cd {directory} && git clone {Project.web_url}" + ".git"
          elif Environment.PLATFORM == "Windows":
            command = f"cd {directory} && git clone {Project.web_url}" + ".git"

          subprocess.run(command, shell = True)

          print()

          os.chdir(execution_location)

          projects_cloned += 1

  def createGitlabDirectory(self, path):
    time.sleep(2.5)
    os.makedirs(path)
    time.sleep(2.5)

  @property
  def Key(self) -> str:
    property = self.API_Key
    return property

class HyperThread(threading.Thread):
  def __init__(self, statement):
    super(HyperThread, self).__init__()
    self.statement = statement

  # self.run() gets ran implicitly from HyperThread's parent class
  def run(self):
    while LabVault.status == True:
      for iterator in '|/-\\': 
        sys.stdout.write(f"  ↳ {self.statement}" + "... " + iterator + "\r")
        time.sleep(0.25)
        sys.stdout.flush()
    sys.stdout.write(f"  ↳ {self.statement}" + "... " + Illustrate().characters["Success"] + "\n")