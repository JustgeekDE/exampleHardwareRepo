import os
import sys
import unittest

from pkg_resources import resource_string

from scoville.circuit import Circuit
from scoville.eagleSchematic import EagleSchematic
from unitTests import test_XOR, test_AND


def getCircuitFunction(schematicFileName):
  def getCircuit(self):
    schematicSource = resource_string('hardware', schematicFileName)
    schematic = EagleSchematic(schematicSource)
    circuit = Circuit(schematic.getSpiceData())
    return circuit

  return getCircuit


def runTests(schematicFileName, testClass):
  testClass.getCircuit = getCircuitFunction(schematicFileName)
  xorTests = unittest.TestLoader().loadTestsFromTestCase(testClass)
  return unittest.TextTestRunner(verbosity=2).run(xorTests)


if __name__ == '__main__':
  sys.path.insert(0, os.getcwd())
  resultXOR = runTests('singleGates/XOR.sch', test_XOR.XORUnitTests)
  resultAND = runTests('singleGates/AND.sch', test_AND.AndUnitTests)

  result = resultXOR.wasSuccessful() and resultAND.wasSuccessful()
  sys.exit(not result)
