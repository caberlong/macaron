import sys                                                                                          
import os
import tensorflow as tf                                                                             

from model.model_input import ModelInput

class Vocabulary:
  def __init__(self, root_dir:str):
    self._root_dir = root_dir
    self._vocabs = {}

  def updateVocab(self, key:str, value:str):
    if not key in self._vocabs:
        self._vocabs[key] = {}

    if not value in self._vocabs[key]:
      self._vocabs[key][value] = 1
    else:
      self._vocabs[key][value] = self._vocabs[key][value] + 1

  def computeVocabs(self):
    dataset = ModelInput(self._root_dir).dataset
    vocab_dir = '/'.join([os.path.dirname(self._root_dir), 'vocabulary'])
    for record in dataset:
      self.updateVocab('sector', record['sector'].numpy())
      self.updateVocab('industry', record['industry'].numpy())

    print('vocabs: %s' % self._vocabs)
