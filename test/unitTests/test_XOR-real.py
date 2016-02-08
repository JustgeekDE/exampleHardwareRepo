from pkg_resources import resource_string

from unittest import TestCase

import os, sys
sys.path.insert(0, os.getcwd())

from scoville.arduinoTester import ArduinoInterface
from scoville.signal import SignalWithResistance


class XORUnitTests(TestCase):


  def getCircuit(self):
    interface = ArduinoInterface('/dev/tty.usbmodem1421')
    interface.inspectVoltage('XOR', 2)
    interface.inspectVoltage('AND', 0)
    interface.inspectVoltage('NOR', 1)
    return interface

  def testLowAndLow(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 0.0, 10), 2)
    circuit.setSignal(SignalWithResistance("B", 0.0, 10), 3)

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), 0.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertGreater(circuit.getVoltage('NOR'), 3.5)

  def testLowAndHigh(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 0.0, 10), 2)
    circuit.setSignal(SignalWithResistance("B", 5.0, 10), 3)

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), 4.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

  def testHighAndLow(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 5.0, 10), 2)
    circuit.setSignal(SignalWithResistance("B", 0.0, 10), 3)

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), 4.5)
    self.assertLess(circuit.getVoltage('AND'), 0.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

  def testHighAndHigh(self):
    circuit = self.getCircuit()
    circuit.setSignal(SignalWithResistance("A", 5.0, 10), 2)
    circuit.setSignal(SignalWithResistance("B", 5.0, 10), 3)

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), 0.5)
    self.assertGreater(circuit.getVoltage('AND'), 2.5)
    self.assertLess(circuit.getVoltage('NOR'), 0.5)

