#!/usr/bin/env python3.7.3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

DOCUMENTATION = """
Module: Illustrate
Author: Jacob B. Sanders (@cloud-hybrid)
Summary: Helper module for drawing and displaying progress.
Documentation: 
"""

class Illustrate(object):
  @property
  def characters(self):
    property = {
      "Arrow-Down-Right" : "↳",
      "Bullet" : "◯",
      "Bullet-Full" : "●",
      "Bullet-Semi" : "◔",
      "Success" : "✔",
      "Failure" : "✕",
      "Progress-Empty" : "░",
      "Progress-Semi" : "▓",
      "Progress-Full" : "█"
    }
    return property

  def __init__(self):
    pass