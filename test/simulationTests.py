from pkg_resources import resource_string
import unittest, os, sys
from unitTests import test_XOR, test_AND

from scoville.eagleSchematic import EagleSchematic
from scoville.circuit import Circuit


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
  unittest.TextTestRunner(verbosity=2).run(xorTests)


if __name__ == '__main__':
    sys.path.insert(0, os.getcwd())
    runTests('singleGates/XOR.sch', test_XOR.XORUnitTests)
    runTests('singleGates/AND.sch', test_AND.AndUnitTests)