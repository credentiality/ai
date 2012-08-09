#!/usr/bin/python

import logging
import math
import random
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("")

# The sigmoid function takes x from -inf..inf and maps it
# to 0..1
def sigmoid(x):
  return 1.0 / (1.0 + math.exp(-x))

class Thought(object):
  """A node in the mind graph"""

  def __init__(self, name):
    logger.info("New thought: " + name)
    self.name = name
    self.activity = 0.0
    self.edges = {}

  def associate(self, other, strength):
    if (other in self.edges):
      self.edges[other] += strength
    else:
      self.edges[other] = strength
    logger.info("associate %s -> %s = %f",
                self.name, other.name, self.edges[other])

class Mind(object):
  def __init__(self):
    self.thoughts = []

  def new_thought(self, name):
    new_thought = Thought(name)
    self.thoughts.append(new_thought)
    return new_thought

  def decay(self):
    """Reduce activation over time"""
    for thought in self.thoughts:
      r = random.gauss(1.0, 0.25)
      thought.activity -= r
      logger.info("decay %s=%f", thought.name, sigmoid(thought.activity))

  def activate_neighbors(self):
    """Randomly activate neighbors"""
    for thought in self.thoughts:
      r = random.gauss(1.0, 0.25)
      level = r * sigmoid(thought.activity)
      for neighbor in thought.edges:
        strength = random.gauss(1.0, 0.25) * r
        thought.associate(neighbor, strength)

  def associate(self):
    """Make new thoughts associating active thoughts"""
    pass

  def chaos(self):
    """Randomly activate thoughts"""
    for thought in self.thoughts:
      r = random.gauss(1.0, 0.25)
      thought.activity += r
      logger.info("chaos: %s=%f", thought.name,
                  sigmoid(thought.activity))

  def think(self):
    """The main loop"""
    self.decay()
    self.activate_neighbors()
    self.associate()
    self.chaos()

mind = Mind()
a = mind.new_thought('a')
b = mind.new_thought('b')
a.associate(b, 1.0)
mind.think()
mind.think()
