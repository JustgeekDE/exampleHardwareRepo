import unittest
from pkg_resources import resource_string

from scoville.circuit import Circuit
from scoville.signal import SignalWithResistance, DelayedSignal
from scoville.eagleSchematic import EagleSchematic



class SimulationUnitTest(unittest.TestCase):

  def getCircuit(self):
    andSource = resource_string('hardware', 'singleGates/AND.sch')
    andcircuit = EagleSchematic(inputData)
    return circuit.getSpiceData()

  def testLowLowShouldResultInLow(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
        circuit.inspectVoltage('AND')

    circuit.run(200)
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testLowHighShouldResultInLow(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run(200)
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testHighLowShouldResultInLow(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run(200)
    self.assertLess(circuit.getVoltage('AND'), 0.5)

  def testHighHighShouldResultInHigh(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectVoltage('AND')

    circuit.run(200)
    self.assertGreater(circuit.getVoltage('AND'), 4.5)

  def testShouldNotUseTooMuchCurrent(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(SignalWithResistance("B", 5.0, 10))
    circuit.inspectCurrent('VP5V')

    circuit.run(200)
    self.assertLess(circuit.getMaxCurrent('VP5V'), .001)

    circuit.setSignal(SignalWithResistance("A", 0.0, 10))
    circuit.run(200)
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.001)

    circuit.setSignal(SignalWithResistance("B", 0.0, 10))
    circuit.run(200)
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.001)

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.run(200)
    self.assertLess(circuit.getMaxCurrent('VP5V'), 0.001)

  def testShouldSwitchOnIn50ns(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(DelayedSignal("B", 5.0, delay=100, startValue=0, resistance=10))
    circuit.inspectVoltage('AND')

    circuit.run(200, 0.05)
    self.assertLess(circuit.getMaxVoltage('AND', 0.01, 100), 0.5)
    self.assertGreater(circuit.getMinVoltage('AND', 100.05, 100), 4.5)

  def testShouldSwitchOffIn50ns(self):
    circuit = getCircuit()

    circuit.setSignal(SignalWithResistance("A", 5.0, 10))
    circuit.setSignal(DelayedSignal("B", value=0.0, delay=100, resistance=10, startValue=5.0))
    circuit.inspectVoltage('AND')

    circuit.run(200, 0.05)
    self.assertGreater(circuit.getMaxVoltage('AND', 0.01, 100), 4.5)
    self.assertLess(circuit.getMinVoltage('AND', 100.05, 100), 0.5)

if __name__ == '__main__':
  unittest.main()
