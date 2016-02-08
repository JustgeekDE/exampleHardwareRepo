from unittest import TestCase
from scoville.signal import GenericSignal

LOW = 0.0
HIGH = 5.0

MAX_LOW_VOLTAGE = 1.0
MIN_HIGH_OUTPUT_VOLTAGE = 4.5
MIN_HIGH_INTERNAL_VOLTAGE = 3.2


class XORUnitTests(TestCase):
  def setInspectionSignals(self, circuit):
    circuit.inspectVoltage('XOR')
    circuit.inspectVoltage('AND')
    circuit.inspectVoltage('NOR')

  def testLowAndLow(self):
    circuit = self.getCircuit()
    self.setInspectionSignals(circuit)

    circuit.setSignal(GenericSignal("A", LOW))
    circuit.setSignal(GenericSignal("B", LOW))

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), MAX_LOW_VOLTAGE)
    self.assertLess(circuit.getVoltage('AND'), MAX_LOW_VOLTAGE)
    self.assertGreater(circuit.getVoltage('NOR'), MIN_HIGH_INTERNAL_VOLTAGE)

  def testLowAndHigh(self):
    circuit = self.getCircuit()
    self.setInspectionSignals(circuit)

    circuit.setSignal(GenericSignal("A", LOW))
    circuit.setSignal(GenericSignal("B", HIGH))

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), MIN_HIGH_OUTPUT_VOLTAGE)
    self.assertLess(circuit.getVoltage('AND'), MAX_LOW_VOLTAGE)
    self.assertLess(circuit.getVoltage('NOR'), MAX_LOW_VOLTAGE)

  def testHighAndLow(self):
    circuit = self.getCircuit()
    self.setInspectionSignals(circuit)

    circuit.setSignal(GenericSignal("A", HIGH))
    circuit.setSignal(GenericSignal("B", LOW))

    circuit.run()

    self.assertGreater(circuit.getVoltage('XOR'), MIN_HIGH_OUTPUT_VOLTAGE)
    self.assertLess(circuit.getVoltage('AND'), MAX_LOW_VOLTAGE)
    self.assertLess(circuit.getVoltage('NOR'), MAX_LOW_VOLTAGE)

  def testHighAndHigh(self):
    circuit = self.getCircuit()
    self.setInspectionSignals(circuit)

    circuit.setSignal(GenericSignal("A", HIGH))
    circuit.setSignal(GenericSignal("B", HIGH))

    circuit.run()

    self.assertLess(circuit.getVoltage('XOR'), MAX_LOW_VOLTAGE)
    self.assertGreater(circuit.getVoltage('AND'), MIN_HIGH_INTERNAL_VOLTAGE)
    self.assertLess(circuit.getVoltage('NOR'), MAX_LOW_VOLTAGE)
