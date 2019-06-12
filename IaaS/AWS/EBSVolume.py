from Vault.IaaS.AWS.AWSBaseObject import AWSBaseObject

from Vault.Tools.Progress import Progress
from Vault.Tools.HyperThread import HyperThread
from Vault.Tools.Environment import Environment

class EBSVolume(AWSBaseObject):
  def __init__(self, name: str, tags = None, template = None, environment = None):
    AWSBaseObject.__init__(self, environment = None)
    