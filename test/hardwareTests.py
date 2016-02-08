import unittest

import serial

from arduinoTester import ArduinoInterface
from unitTests import test_XOR


def getCircuitFunction(interface):
  def getCircuit(self):
    return interface

  return getCircuit


def runTests(interface, testClass):
  testClass.getCircuit = getCircuitFunction(interface)
  xorTests = unittest.TestLoader().loadTestsFromTestCase(testClass)
  unittest.TextTestRunner(verbosity=2).run(xorTests)


def setupInterface():
  serialInterface = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=115200, timeout=1)

  arduinoInterface = ArduinoInterface(serialInterface)
  arduinoInterface.mapOutput('A', 2)
  arduinoInterface.mapOutput('B', 3)

  arduinoInterface.mapInput('XOR', 2)
  arduinoInterface.mapInput('AND', 0)
  arduinoInterface.mapInput('NOR', 1)
  return (serialInterface, arduinoInterface)


if __name__ == '__main__':
  (serialInterface, arduinoInterface) = setupInterface()
  runTests(arduinoInterface, test_XOR.XORUnitTests)

  serialInterface.close()
