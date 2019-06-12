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

import sys
import time
import threading

from Vault.Tools.ASCII import ASCII

class HyperThread(threading.Thread):
  def __init__(self, statement):
    super(HyperThread, self).__init__()
    self.statement = statement

  def run(self, Object):
    while Object.status == True:
      for iterator in '|/-\\': 
        sys.stdout.write(f"  ↳ {self.statement}" + "... " + iterator + "\r")
        time.sleep(0.25)
        sys.stdout.flush()
    sys.stdout.write(f"  ↳ {self.statement}" + "... " + ASCII().characters["Success"] + "\n")