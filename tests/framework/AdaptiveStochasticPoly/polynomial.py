#***************************************
#* Simple analytic test ExternalModule *
#***************************************
#
import numpy as np

def evaluate(inp):
  return np.prod(list(1.+n for n in inp))

def run(self,Input):
  self.ans = self.x1**2*self.x2 + self.x1**2 + self.x1*self.x2 + self.x1 + self.x2 + 1.
  self.ans2 = self.x1*self.x2 + self.x1 + self.x2 + 1.