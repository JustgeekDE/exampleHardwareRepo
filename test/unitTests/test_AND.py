from pkg_resources import resource_string

from unittest import TestCase

import os, sys
sys.path.insert(0, os.getcwd())

from scoville.circuit import Circuit
from scoville.signal import SignalWithResistance, DelayedSignal
from scoville.eagleSchematic import EagleSchematic


class SimulationUnitTest(TestCase):

  def getCircuit(self):
    andSource = resource_string('hardware', 'singleGates/AND.sch')
    andcircuit = EagleSchematic(andSource)
    return Circuit(andcircuit.getSpiceData())

  def testLowLowShouldResultInLow(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run()
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testLowHighShouldResultInLow(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run()
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testHighLowShouldResultInLow(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run()
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testHighHighShouldResultInHigh(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run()
    self.assertGreater(circuit.getVoltage('AND'), 4.5)

  def testShouldNotUseTooMuchCurrent(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectCurrent('VP5V')

    circuit.run()
    self.assertLess(circuit.getMaxCurrent('VP5V'), .01)

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.run()
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.01)

    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
    circuit.run()
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.01)

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.run()
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.01)

  def testShouldSwitchOnIn1ns(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(DelayedSignal("B", 5.0, delay=10, startValue=0, resistance=10))
    circuit.inspectVoltage('AND')

    circuit.run(20, 0.01)
    self.assertLess(circuit.getMaxVoltage('AND', 1, 10), 0.5)
    self.assertGreater(circuit.getMinVoltage('AND', 11, 20), 4.5)

  def testShouldSwitchOffIn1ns(self):
    circuit = self.getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(DelayedSignal("B", value=0.0, delay=10, resistance=10, startValue=5.0))
    circuit.inspectVoltage('AND')

    circuit.run(20, 0.01)
    self.assertGreater(circuit.getMinVoltage('AND', 1, 10), 4.5)
    self.assertLess(circuit.getMaxVoltage('AND', 11, 20), 0.5)

