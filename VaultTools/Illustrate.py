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

import sys
import time
import threading

from multiprocessing import Process, Queue


class Illustrate(object):
  def __init__(self):
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

    self.Queue = Queue()

  def run(self, processes, arguments = None, timeout = 60):
    reader_process = Process(target = self.readQueuedProcess, args = ((self.Queue),))
    reader_process.daemon = True
    reader_process.start()
    _start = time.time()

    for process in processes:
      print("Sending {0} to Queue().".format(process))
      self.writeQueuedProcess(process, self.Queue)
      reader_process.join()
      print("Time: {0} seconds".format((time.time() - _start)))

  def executeThread(self):
    for iterator in '|/-\\'*3 + "✔": 
      sys.stdout.write(f"  ↳ Initializing GitLab Wrappers" + "... " + iterator + "\r")
      sys.stdout.flush()
      time.sleep(0.25)

  def progress(self, size: int, thread, queue):
    thread.start()

    # How many ASCII spaces (width)
    progress_bar_size = size

  @staticmethod
  def readQueuedProcess(queue):
    """ Reads from the queue and spawns a seperate process. """

    while True:
      threading.Thread(target = HyperThread("NA").run())
      status = queue.get()
      if status == "DONE":
        break

  def writeQueuedProcess(self, process, queue):
    """ Writes to the queue. """

    queue.put(getattr(self, process)())
    queue.put("DONE")

  def example(self):
    for i in range(0, 3):
      time.sleep(1)

  def example2(self):
    for i in range(0, 2):
      time.sleep(1)

class HyperThread(threading.Thread):
  def __init__(self, name):
    super(HyperThread, self).__init__()
    self.name = name

  # self.run() gets ran implicitly from HyperThread's parent class
  def run(self):
    # print(f"Initiating New Thread: {self.name}")
    while True:
      for iterator in '|/-\\': 
        sys.stdout.write("In Progress...   " + iterator + "\r")
        time.sleep(0.35)
        sys.stdout.flush()
    sys.stdout.write("In Progress...   " + "✔" + "\n")

def main():
  i = Illustrate()
  i.run(["example", "example2"])


if __name__ == "__main__":
  main()