from pkg_resources import resource_string

from unittest import TestCase

import os, sys
sys.path.insert(0, os.getcwd())

from scoville.circuit import Circuit
from scoville.signal import SignalWithResistance, DelayedSignal
from scoville.eagleSchematic import EagleSchematic


class SimulationUnitTest(TestCase):


  def getCircuit(self):
    schematicSource = resource_string('hardware', 'singleGates/XOR.sch')
    schematic = EagleSchematic(schematicSource)
    circuit = Circuit(schematic.getSpiceData())

    circuit.inspectVoltage('XOR')
    circuit.inspectVoltage('AND')
    circuit.inspectVoltage('NOR')
    return circuit

  def testLowAndLow(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), 0.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertGreater(circuit.getVoltage('NOR'), 3.5)

  def testLowAndHigh(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), 4.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

  def testHighAndLow(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), 4.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

  def testHighAndHigh(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), 0.5)
    self.assertGreater(circuit.getVoltage('AND'), 3.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

