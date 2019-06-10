#!/usr/bin/env python3.7.3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

DOCUMENTATION = """
Module: 
Author: Jacob B. Sanders (@cloud-hybrid)
Summary:
Documentation: https://vaultcipher.com/

@Development
- Update @ Documentation Variables
- Add Examples 
- Add Metadata
"""

import os
import pwd
import sys
import shlex
import platform
import subprocess

class Environment(object):
  PLATFORM = platform.system()

  if PLATFORM == "Darwin" or PLATFORM == "Linux":
    USERNAME = pwd.getpwuid(os.getuid())[0]
  elif PLATFORM == "Windows":
    USERNAME = os.getlogin()
  else:
    USERNAME = None
  
  def __init__(self):
    pass

  def printUsername(self):
    print(self.USERNAME)

  def printPublicKey(self, buffer = False):
    """ Prints the default public SSH key to STDOUT/copies to the buffer. """

    if self.PLATFORM == "Darwin" or self.PLATFORM == "Linux":
      command = "cat ~/.ssh/id_rsa.pub"

      stream = subprocess.Popen([command],
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      output = stream.communicate(timeout = 15)[0]
      
      if buffer == True:
        return stream.communicate(timeout = 15)[0]
      else:
        print(output.strip())

  def printNetworkInterfaces(self):
    print(self.NetworkInterfaces)

  @property
  def LinuxSSHDirectory(self):
    property = f"/Users/{self.USERNAME}/.ssh/"
    return property

  @property
  def MacOSHomeDirectory(self):
    property = f"/Users/{self.USERNAME}/"
    return property

  @property
  def LinuxHomeDirectory(self):
    property = f"/Users/{self.USERNAME}/"
    return property

  @property
  def WindowsHomeDirectory(self):
    property = f"C:\\Users\\{self.USERNAME}\\"
    return property

  @property
  def WindowsRSAKey(self):
    property = f"C:\\Users\\{self.USERNAME}\\.ssh\\id_rsa.pub"
    return property

  @property
  def NetworkInterfaces(self):
    command = "echo $(networksetup -listallhardwareports)"

    stream = subprocess.Popen([command],
      shell = True,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    property = output.strip()

    return property

def main(argv):
  project = Environment()

  project.printUsername()
  project.printNetworkInterfaces()
  project.printPublicKey()


if __name__ == "__main__":
  main(sys.argv)