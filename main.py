import os

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *
from time import sleep

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

# screens
SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
STEPPER_SCREEN_NAME = 'stepper'
SERVO_SCREEN_NAME = "servo"
DC_SCREEN_NAME = "DC"
STEPPER_STARTUP_SCREEN_NAME = 'StepperStartup'
BUTTON_SCREEN_NAME = "button"
INPUT_SCREEN_NAME = "input"
OUTPUT_SCREEN_NAME = "output"
NEOPIXEL_SCREEN_NAME = "Neopixel"
ENCODER_SCREEN_NAME = "Encoder"
POTENTIOMETER_SCREEN_NAME = "Potentiometer"

# associated variables for StepperScreen
dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
microStepping = ""
stepperSpeed = ""
stepperAcceleration = ""
stepper0Distance = ""
stepper1Distance = ""
stepper2Distance = ""
stepper_num = ""
distanceUnits = ""
direction = ""
# StepperMotorStartupScreen variables
homingType = ""
homingDirection = ""
homingSpeed = ""
stepperLinearHomeValue = ""
stepperAngularHomeValue = ""
homingUnits = ""
homeMaxDistance = ""
hasTransmission = False
gearRatio = ""

# associated variables for DC and Servo
dpiComputer = DPiComputer()
dpiComputer.initialize()
speedDC0 = ""
speedDC1 = ""
my_angle0 = ""
my_angle1 = ""
servo_number = ""

# associated variables for Button Class, uses dpiComputer
button_num = ""
redValue_pressed = ""
greenValue_pressed = ""
blueValue_pressed = ""
redValue_not_pressed = ""
blueValue_not_pressed = ""
greenValue_not_pressed = ""

# associated variables for  Neopixel class, uses dpiComputer
neopixel0_redValue = ""
neopixel0_blueValue = ""
neopixel0_greenValue = ""
neopixel1_redValue = ""
neopixel1_blueValue = ""
neopixel1_greenValue = ""
numNeopixels0 = ""
neopixel_array0 = []
neopixel_array1 = []
numNeopixels1 = ""
index = ""

# variables for encoder, uses dpiComputer
encoder0_position = ""
encoder1_position = ""

# variables for potentiometer, uses dpiComputer
potentiometer0_value = ""
potentiometer1_value = ""


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    @staticmethod
    def exit_program():
        """
        Quit the program.
        :return: None
        """
        quit()


class PotentiometerScreen(Screen):
    """
    Class to handle the PotentiometerScreen and its associated touch events
    """
    potentiometer0_value = ""
    potentiometer1_value = ""

    def __init__(self, **kwargs):
        Builder.load_file('PotentiometerScreen.kv')
        super(PotentiometerScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.readPotentiometer, .01)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program.
        :return: None
        """
        quit()

    # reads the analog value from the potentiometer, and updates the associated label
    def readPotentiometer(self, dt):
        potentiometer0_value = str(dpiComputer.readAnalog(0))
        self.ids.potentiometer0_label.text = "Potentiometer 0 Value: " + potentiometer0_value
        potentiometer1_value = str(dpiComputer.readAnalog(1))
        self.ids.potentiometer1_label.text = "Potentiometer 1 Value: " + potentiometer1_value


class EncoderScreen(Screen):
    """
    Class to handle the EncoderScreen and its associated touch events
    """
    encoder0_position = ""
    encoder1_position = ""

    def __init__(self, **kwargs):
        Builder.load_file('EncoderScreen.kv')
        super(EncoderScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.readEncoder, .01)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program.
        :return: None
        """
        quit()

    # reads the encoder position, and updates associated label
    def readEncoder(self, dt):
        encoder0_position = str(dpiComputer.readEncoder(0))
        self.ids.encoder0_value.text = "Encoder 0 Position: " + encoder0_position
        encoder1_position = str(dpiComputer.readEncoder(1))
        self.ids.encoder1_value.text = "Encoder 1 Position: " + encoder1_position


class NeopixelScreen(Screen):
    """
    Class to handle the Neopixel screen and its associated touch events
    """
    neopixel0_redValue = ""
    neopixel0_blueValue = ""
    neopixel0_greenValue = ""
    neopixel1_redValue = ""
    neopixel1_blueValue = ""
    neopixel1_greenValue = ""
    numNeopixels0 = ""
    numNeopixels1 = ""
    neopixel_array = []
    neopixel_array1 = []
    index = ""

    def __init__(self, **kwargs):
        Builder.load_file('NeopixelScreen.kv')
        super(NeopixelScreen, self).__init__(**kwargs)

    def transition_back(self):
        """
        Transition back to the main screen. Powers off all Neopixels. Reset buttons and labels
        :return:
        """
        global neopixel_array
        global neopixel_array1
        global numNeopixels0
        global numNeopixels1
        global neopixel0_redValue
        global neopixel0_greenValue
        global neopixel0_blueValue
        global neopixel1_redValue
        global neopixel1_greenValue
        global neopixel1_blueValue
        global index
        index = ""
        numNeopixels0 = "200"
        numNeopixels1 = "200"
        neopixel0_redValue = ""
        neopixel0_blueValue = ""
        neopixel0_greenValue = ""
        neopixel1_redValue = ""
        neopixel1_blueValue = ""
        neopixel1_greenValue = ""

        neopixel_array = [(0, 0, 0)] * int(numNeopixels0)
        dpiComputer.writeNeopixelByArray(0, neopixel_array)
        neopixel_array1 = [(0, 0, 0)] * int(numNeopixels1)
        dpiComputer.writeNeopixelByArray(1, neopixel_array1)

        # deselect neopixel strip labels
        self.ids.neopixel0.text = "Neopixel 0"
        self.ids.neopixel1.text = "Neopixel 1"

        # deselect number of neopixel and index labels
        self.ids.num_neopixels.text = "Number of Neopixels"
        self.ids.index.text = "Index"

        # deselect color labels
        self.ids.set_red.text = "Set Red Value"
        self.ids.set_green.text = "Set Green Value"
        self.ids.set_blue.text = "Set Blue Value"

        # reset labels
        self.ids.red_value.text = "R1: "
        self.ids.green_value.text = "G1: "
        self.ids.blue_value.text = "B1: "

        self.ids.number_neopixels_value.text = "Number of Neopixels:"
        self.ids.index_value.text = "Index: "

        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program.
        :return: None
        """
        quit()

    # selects Neopixel 0
    def selectNeopixel0(self):
        global index
        global numNeopixels0
        numNeopixels0 = ""
        index = ""
        self.ids.neopixel0.text = "Neopixel 0*"
        self.ids.neopixel1.text = "Neopixel 1"
        self.ids.red_value.text = "R1: "
        self.ids.green_value.text = "G1: "
        self.ids.blue_value.text = "B1: "

        self.ids.number_neopixels_value.text = "Number of Neopixels:"
        self.ids.index_value.text = "Index: " + index

    # selects Neopixel 1
    def selectNeopixel1(self):
        global index
        global numNeopixels1
        numNeopixels1 = ""
        index = ""
        self.ids.neopixel1.text = "Neopixel 1*"
        self.ids.neopixel0.text = "Neopixel 0"
        self.ids.red_value.text = "R1: "
        self.ids.green_value.text = "G1: "
        self.ids.blue_value.text = "B1: "
        self.ids.number_neopixels_value.text = "Number of Neopixels:"
        self.ids.index_value.text = "Index: " + index

    # select number of neopixels to input
    def selectNumberOfNeopixels(self):
        self.ids.num_neopixels.text = "Number of Neopixels*"
        self.ids.index.text = "Index"

    # selects index to input
    def selectIndex(self):
        self.ids.num_neopixels.text = "Number of Neopixels"
        self.ids.index.text = "Index*"

    # selects red value to input
    def selectRed1(self):
        self.ids.set_red.text = "Set Red Value*"
        self.ids.set_green.text = "Set Green Value"
        self.ids.set_blue.text = "Set Blue Value"

    # selects green value to input
    def selectGreen1(self):
        self.ids.set_red.text = "Set Red Value"
        self.ids.set_green.text = "Set Green Value*"
        self.ids.set_blue.text = "Set Blue Value"

    # selects blue value to input
    def selectBlue1(self):
        self.ids.set_red.text = "Set Red Value"
        self.ids.set_green.text = "Set Green Value"
        self.ids.set_blue.text = "Set Blue Value*"

    # reads input from keyboard to set the colors
    def setColor(self, input):
        global neopixel0_redValue
        global neopixel0_greenValue
        global neopixel0_blueValue
        global neopixel0_redValue2
        global neopixel0_greenValue2
        global neopixel0_blueValue2
        global neopixel1_redValue
        global neopixel1_blueValue
        global neopixel1_greenValue
        if self.ids.neopixel0.text == "Neopixel 0*":
            if self.ids.set_red.text == "Set Red Value*":
                neopixel0_redValue += str(input)
                self.ids.red_value.text = "R1: " + neopixel0_redValue
            if self.ids.set_green.text == "Set Green Value*":
                neopixel0_greenValue += str(input)
                self.ids.green_value.text = "G1: " + neopixel0_greenValue
            if self.ids.set_blue.text == "Set Blue Value*":
                neopixel0_blueValue += str(input)
                self.ids.blue_value.text = "B1: " + neopixel0_blueValue

        if self.ids.neopixel1.text == "Neopixel 1*":
            if self.ids.set_red.text == "Set Red Value*":
                neopixel1_redValue += str(input)
                self.ids.red_value.text = "R1: " + neopixel1_redValue
            if self.ids.set_green.text == "Set Green Value*":
                neopixel1_greenValue += str(input)
                self.ids.green_value.text = "G1: " + neopixel1_greenValue
            if self.ids.set_blue.text == "Set Blue Value*":
                neopixel1_blueValue += str(input)
                self.ids.blue_value.text = "B1: " + neopixel1_blueValue

    # reads input for number of neopixels and index keyboard
    def readKeyboardInput(self, num):
        global numNeopixels0
        global numNeopixels1
        global index
        if self.ids.neopixel0.text == "Neopixel 0*":

            if self.ids.num_neopixels.text == "Number of Neopixels*":
                numNeopixels0 += str(num)
                self.ids.number_neopixels_value.text = "Number of Neopixels: " + numNeopixels0

            if self.ids.index.text == "Index*":
                index += str(num)
                self.ids.index_value.text = "Index: " + index

        if self.ids.neopixel1.text == "Neopixel 1*":
            if self.ids.num_neopixels.text == "Number of Neopixels*":
                numNeopixels1 += str(num)
                self.ids.number_neopixels_value.text = "Number of Neopixels: " + numNeopixels1

            if self.ids.index.text == "Index*":
                index += str(num)
                self.ids.index_value.text = "Index: " + index

    # removes input for number of neopixels and index keyboard
    def removeKeyboardInput(self):
        global numNeopixels0
        global numNeopixels1
        global index
        if self.ids.neopixel0.text == "Neopixel 0*":
            if self.ids.num_neopixels.text == "Number of Neopixels*":
                numNeopixels0 = numNeopixels0[:-1]
                self.ids.number_neopixels_value.text = "Number of Neopixels: " + numNeopixels0

            if self.ids.index.text == "Index*":
                index = index[:-1]
                self.ids.index_value.text = "Index: " + index

        if self.ids.neopixel1.text == "Neopixel 1*":
            if self.ids.num_neopixels.text == "Number of Neopixels*":
                numNeopixels1 = numNeopixels1[:-1]
                self.ids.number_neopixels_value.text = "Number of Neopixels: " + numNeopixels1

            if self.ids.index.text == "Index*":
                index = index[:-1]
                self.ids.index_value.text = "Index: " + index

    # deletes color value
    def removeColor(self):
        global neopixel0_redValue
        global neopixel0_greenValue
        global neopixel0_blueValue
        global neopixel1_redValue
        global neopixel1_blueValue
        global neopixel1_greenValue

        if self.ids.neopixel0.text == "Neopixel 0*":
            if self.ids.set_red.text == "Set Red Value*":
                neopixel0_redValue = neopixel0_redValue[:-1]
                self.ids.red_value.text = "R1: " + neopixel0_redValue
            if self.ids.set_green.text == "Set Green Value*":
                neopixel0_greenValue = neopixel0_greenValue[:-1]
                self.ids.green_value.text = "G1: " + neopixel0_greenValue
            if self.ids.set_blue.text == "Set Blue Value*":
                neopixel0_blueValue = neopixel0_blueValue[:-1]
                self.ids.blue_value.text = "B1: " + neopixel0_blueValue

        if self.ids.neopixel1.text == "Neopixel 1*":
            if self.ids.set_red.text == "Set Red Value*":
                neopixel1_redValue = neopixel1_redValue[:-1]
                self.ids.red_value.text = "R1: " + neopixel1_redValue
            if self.ids.set_green.text == "Set Green Value*":
                neopixel1_greenValue = neopixel1_greenValue[:-1]
                self.ids.green_value.text = "G1: " + neopixel1_greenValue
            if self.ids.set_blue.text == "Set Blue Value*":
                neopixel1_blueValue = neopixel1_blueValue[:-1]
                self.ids.blue_value.text = "B1: " + neopixel1_blueValue

    # sets the neopixels color
    def setIndividualNeopixel(self):
        global neopixel0_redValue
        global neopixel0_greenValue
        global neopixel0_blueValue
        global neopixel1_redValue
        global neopixel1_blueValue
        global neopixel1_greenValue
        global neopixel_array
        global neopixel_array1
        global index
        try:
            if self.ids.neopixel0.text == "Neopixel 0*":
                neopixel_array[int(index)] = (
                    int(neopixel0_redValue), int(neopixel0_greenValue), int(neopixel0_blueValue))
                dpiComputer.writeNeopixelByArray(0, neopixel_array)

            if self.ids.neopixel1.text == "Neopixel 1*":
                neopixel_array1[int(index)] = (
                    int(neopixel1_redValue), int(neopixel1_greenValue), int(neopixel1_blueValue))
                dpiComputer.writeNeopixelByArray(1, neopixel_array1)

            self.ids.error_neopixel.text = ""
        except ValueError:
            self.ids.error_neopixel.text = "Invalid input, review instructions again"

    # creates array of neopixels, and turns the neopixels off
    def setNeopixelsoff(self):
        global neopixel_array
        global neopixel_array1
        global numNeopixels0
        global numNeopixels1
        try:
            self.ids.error_neopixel.text = ""
            if self.ids.neopixel0.text == "Neopixel 0*":
                neopixel_array = [(0, 0, 0)] * int(numNeopixels0)
                dpiComputer.writeNeopixelByArray(0, neopixel_array)

            if self.ids.neopixel1.text == "Neopixel 1*":
                neopixel_array1 = [(0, 0, 0)] * int(numNeopixels1)
                dpiComputer.writeNeopixelByArray(1, neopixel_array1)
        except ValueError:
            self.ids.error_neopixel.text = "Invalid input, review instructions again"


class OutputScreen(Screen):
    """
    Class to handle the output screen and its associated touch events
    """

    def __init__(self, **kwargs):
        Builder.load_file('OutputScreen.kv')
        super(OutputScreen, self).__init__(**kwargs)

    def transition_back(self):
        """
        Transition back to the main screen. set output to low for all OUTPUTS
        :return:
        """
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_0, False)
        self.ids.OUT_0.text = "OUT 0: LOW"

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_1, False)
        self.ids.OUT_1.text = "OUT 1: LOW"

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, False)
        self.ids.OUT_2.text = "OUT 2: LOW"

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_3, False)
        self.ids.OUT_3.text = "OUT 3: LOW"

        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program. This should set all outputs to low
        :return: None
        """
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_0, False)

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_1, False)

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, False)

        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_3, False)
        quit()

    # toggles OUT 0 between HIGH and LOW
    def WriteValue0(self):
        if self.ids.OUT_0.text == "OUT 0: LOW":
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_0, True)
            self.ids.OUT_0.text = "OUT 0: HIGH"
        else:
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_0, False)
            self.ids.OUT_0.text = "OUT 0: LOW"

    # toggles OUT 1 between HIGH and LOW
    def WriteValue1(self):
        if self.ids.OUT_1.text == "OUT 1: LOW":
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_1, True)
            self.ids.OUT_1.text = "OUT 1: HIGH"
        else:
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_1, False)
            self.ids.OUT_1.text = "OUT 1: LOW"

    # toggles OUT 2 between HIGH and LOW
    def WriteValue2(self):
        if self.ids.OUT_2.text == "OUT 2: LOW":
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, True)
            self.ids.OUT_2.text = "OUT 2: HIGH"
        else:
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, False)
            self.ids.OUT_2.text = "OUT 2: LOW"

    # toggles OUT 3 between HIGH and LOW
    def WriteValue3(self):
        if self.ids.OUT_3.text == "OUT 3: LOW":
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_3, True)
            self.ids.OUT_3.text = "OUT 3: HIGH"
        else:
            dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_3, False)
            self.ids.OUT_3.text = "OUT 3: LOW"


class InputScreen(Screen):
    """
    Class to handle the Input screen and its associated touch events
    """

    def __init__(self, **kwargs):
        Builder.load_file('InputScreen.kv')
        super(InputScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.readInput, .1)

    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        self.ids.IN_0.text = "IN 0"
        self.ids.IN_1.text = "IN 1"
        self.ids.IN_2.text = "IN 2"
        self.ids.IN_3.text = "IN 3"
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program. This should reset all buttons
        :return: None
        """
        quit()

    # selects IN0 to read
    def selectIN0(self):
        self.ids.IN_0.text = "IN 0*"
        self.ids.IN_1.text = "IN 1"
        self.ids.IN_2.text = "IN 2"
        self.ids.IN_3.text = "IN 3"

    # selects IN1 to read
    def selectIN1(self):
        self.ids.IN_0.text = "IN 0"
        self.ids.IN_1.text = "IN 1*"
        self.ids.IN_2.text = "IN 2"
        self.ids.IN_3.text = "IN 3"

    # selects IN2 to read
    def selectIN2(self):
        self.ids.IN_0.text = "IN 0"
        self.ids.IN_1.text = "IN 1"
        self.ids.IN_2.text = "IN 2*"
        self.ids.IN_3.text = "IN 3"

    # selects IN3 to read
    def selectIN3(self):
        self.ids.IN_0.text = "IN 0"
        self.ids.IN_1.text = "IN 1"
        self.ids.IN_2.text = "IN 2"
        self.ids.IN_3.text = "IN 3*"

    # reads input of selected IN
    def readInput(self, dt):
        if self.ids.IN_0.text == "IN 0*":
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0):
                sleep(.1)
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0):  # a little debounce logic
                self.ids.sensor_value.text = "HIGH"

            else:
                self.ids.sensor_value.text = "LOW"

                sleep(.1)

        if self.ids.IN_1.text == "IN 1*":
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1):
                sleep(.1)
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1):  # a little debounce logic
                self.ids.sensor_value.text = "HIGH"

            else:
                self.ids.sensor_value.text = "LOW"

                sleep(.1)

        if self.ids.IN_2.text == "IN 2*":
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_2):
                sleep(.1)
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_2):  # a little debounce logic
                self.ids.sensor_value.text = "HIGH"

            else:
                self.ids.sensor_value.text = "LOW"

                sleep(.1)

        if self.ids.IN_3.text == "IN 3*":
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_3):
                sleep(.1)
            if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_3):  # a little debounce logic
                self.ids.sensor_value.text = "HIGH"

            else:
                self.ids.sensor_value.text = "LOW"

                sleep(.1)


class ButtonScreen(Screen):
    """
    Class to handle the button screen and its associated touch events
    """
    button_num = ""
    redValue_pressed = ""
    blueValue_pressed = ""
    greenValue_pressed = ""
    redValue_not_pressed = ""
    blueValue_not_pressed = ""
    greenValue_not_pressed = ""

    def __init__(self, **kwargs):
        Builder.load_file('ButtonScreen.kv')
        super(ButtonScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.getButtonStatus, .001)

    # transition back should unselect all buttons, reset labels, and disable clock
    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed
        redValue_pressed = ""
        greenValue_pressed = ""
        blueValue_pressed = ""
        redValue_not_pressed = ""
        greenValue_not_pressed = ""
        blueValue_not_pressed = ""

        Clock.unschedule(self.getButtonStatus)
        dpiComputer.writeRGBButtonColor(0, 0, 0, 0)
        dpiComputer.writeRGBButtonColor(1, 0, 0, 0)
        self.ids.button_1.text = "Button 1"
        self.ids.button_0.text = "Button 0"
        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

        # reset color labels:
        self.ids.red_value_not_pressed.text = "Red Value Not Pressed:"
        self.ids.green_value_not_pressed.text = "Green Value Not Pressed:"
        self.ids.blue_value_not_pressed.text = "Blue Value Not Pressed:"
        self.ids.red_value_pressed.text = "Red Value Pressed:"
        self.ids.green_value_pressed.text = "Green Value Pressed:"
        self.ids.blue_value_pressed.text = "Blue Value Pressed:"

        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def exit_program(self):
        """
        Quit the program. This should turn off  RGB buttons, reset kivy buttons and labels
        :return: None
        """
        Clock.unschedule(self.getButtonStatus)
        dpiComputer.writeRGBButtonColor(0, 0, 0, 0)
        dpiComputer.writeRGBButtonColor(1, 0, 0, 0)
        self.ids.button_1.text = "Button 1"
        self.ids.button_0.text = "Button 0"
        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"
        quit()

    # checks the button status, pressed or not pressed
    def getButtonStatus(self, dt):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed
        if self.ids.button_0.text == "Button 0*":
            button_value = dpiComputer.readRGBButtonSwitch(0)  # read the button
            if button_value:
                if redValue_pressed == "" or greenValue_pressed == "" or blueValue_pressed == "":
                    red = 255
                    green = 0
                    blue = 0

                else:
                    red = int(redValue_pressed)
                    green = int(greenValue_pressed)
                    blue = int(blueValue_pressed)
                self.ids.button_immediate_value.text = "Button pressed"
                dpiComputer.writeRGBButtonColor(0, red, green, blue)
            else:
                if redValue_not_pressed == "" or greenValue_not_pressed == "" or blueValue_not_pressed == "":
                    red = 64
                    green = 240
                    blue = 255

                else:
                    red = int(redValue_not_pressed)
                    green = int(greenValue_not_pressed)
                    blue = int(blueValue_not_pressed)
                self.ids.button_immediate_value.text = "Button not pressed"
                dpiComputer.writeRGBButtonColor(0, red, green, blue)

        if self.ids.button_1.text == "Button 1*":
            button_value = dpiComputer.readRGBButtonSwitch(1)  # read the button
            if button_value == True:
                if redValue_pressed == "" or greenValue_pressed == "" or blueValue_pressed == "":
                    red = 255
                    green = 0
                    blue = 0

                else:
                    red = int(redValue_pressed)
                    green = int(greenValue_pressed)
                    blue = int(blueValue_pressed)
                self.ids.button_immediate_value.text = "Button pressed"
                dpiComputer.writeRGBButtonColor(1, red, green, blue)  # set button to RED if pushed
            else:
                if (redValue_not_pressed == "") or (greenValue_not_pressed == "") or (blueValue_not_pressed == ""):
                    red = 64
                    green = 240
                    blue = 255

                else:
                    red = int(redValue_not_pressed)
                    green = int(greenValue_not_pressed)
                    blue = int(blueValue_not_pressed)
                self.ids.button_immediate_value.text = "Button not pressed"
                dpiComputer.writeRGBButtonColor(1, red, green, blue)

    # selects button 0 to use
    def selectButton0(self):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed
        redValue_pressed = ""
        greenValue_pressed = ""
        blueValue_pressed = ""
        redValue_not_pressed = ""
        greenValue_not_pressed = ""
        blueValue_not_pressed = ""
        self.ids.button_0.text = "Button 0*"
        self.ids.button_1.text = "Button 1"
        Clock.schedule_interval(self.getButtonStatus, .01)

    # selects button 1 to use
    def selectButton1(self):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed
        redValue_pressed = ""
        greenValue_pressed = ""
        blueValue_pressed = ""
        redValue_not_pressed = ""
        greenValue_not_pressed = ""
        blueValue_not_pressed = ""
        self.ids.button_0.text = "Button 0"
        self.ids.button_1.text = "Button 1*"
        Clock.schedule_interval(self.getButtonStatus, .01)

    # selects red not pressed value to input
    def selectRedNotPressed(self):
        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed*"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

    # selects green not pressed value to input
    def selectGreenNotPressed(self):
        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed*"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

    # selects blue not pressed value to input
    def selectBlueNotPressed(self):
        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed*"

        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

    # selects red pressed value to input
    def selectRedPressed(self):
        self.ids.set_red_pressed.text = "Set Red Value Pressed*"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

    # selects green pressed value to input
    def selectGreenPressed(self):
        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed*"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed"

        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

    # selects blue pressed value to input
    def selectBluePressed(self):
        self.ids.set_red_pressed.text = "Set Red Value Pressed"
        self.ids.set_green_pressed.text = "Set Green Value Pressed"
        self.ids.set_blue_pressed.text = "Set Blue Value Pressed*"

        self.ids.set_red_not_pressed.text = "Set Red Value\nNot Pressed"
        self.ids.set_green_not_pressed.text = "Set Green Value\nNot Pressed"
        self.ids.set_blue_not_pressed.text = "Set Blue Value\nNot Pressed"

    # reads input from keyboard to set the colors
    def setColor(self, input):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed

        if self.ids.set_red_not_pressed.text == "Set Red Value\nNot Pressed*":
            redValue_not_pressed += str(input)
            self.ids.red_value_not_pressed.text = "Red Value Not Pressed:" + redValue_not_pressed
        if self.ids.set_green_not_pressed.text == "Set Green Value\nNot Pressed*":
            greenValue_not_pressed += str(input)
            self.ids.green_value_not_pressed.text = "Green Value Not Pressed:" + greenValue_not_pressed
        if self.ids.set_blue_not_pressed.text == "Set Blue Value\nNot Pressed*":
            blueValue_not_pressed += str(input)
            self.ids.blue_value_not_pressed.text = "Blue Value Not Pressed: " + blueValue_not_pressed

        if self.ids.set_red_pressed.text == "Set Red Value Pressed*":
            redValue_pressed += str(input)
            self.ids.red_value_pressed.text = "Red Value Pressed:" + redValue_pressed
        if self.ids.set_green_pressed.text == "Set Green Value Pressed*":
            greenValue_pressed += str(input)
            self.ids.green_value_pressed.text = "Green Value Pressed:" + greenValue_pressed
        if self.ids.set_blue_pressed.text == "Set Blue Value Pressed*":
            blueValue_pressed += str(input)
            self.ids.blue_value_pressed.text = "Blue Value Pressed: " + blueValue_pressed

    # deletes color value
    def removeColor(self):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed

        if self.ids.set_red_not_pressed.text == "Set Red Value\nNot Pressed*":
            redValue_not_pressed = redValue_not_pressed[:-1]
            self.ids.red_value_not_pressed.text = "Red Value Not Pressed:" + redValue_not_pressed
        if self.ids.set_green_not_pressed.text == "Set Green Value\nNot Pressed*":
            greenValue_not_pressed = greenValue_not_pressed[:-1]
            self.ids.green_value_not_pressed.text = "Green Value Not Pressed:" + greenValue_not_pressed
        if self.ids.set_blue_not_pressed.text == "Set Blue Value\nNot Pressed*":
            blueValue_not_pressed = blueValue_not_pressed[:-1]
            self.ids.blue_value_not_pressed.text = "Blue Value Not Pressed: " + blueValue_not_pressed

        if self.ids.set_red_pressed.text == "Set Red Value Pressed*":
            redValue_pressed = redValue_pressed[:-1]
            self.ids.red_value_pressed.text = "Red Value Pressed:" + redValue_pressed
        if self.ids.set_green_pressed.text == "Set Green Value Pressed*":
            greenValue_pressed = greenValue_pressed[:-1]
            self.ids.green_value_pressed.text = "Green Value Pressed:" + greenValue_pressed
        if self.ids.set_blue_pressed.text == "Set Blue Value Pressed*":
            blueValue_pressed = blueValue_pressed[:-1]
            self.ids.blue_value_pressed.text = "Blue Value Pressed: " + blueValue_pressed

    # check to see if button is pressed, red is pressed, green is not pressed
    def testPressed(self):
        global redValue_pressed
        global greenValue_pressed
        global blueValue_pressed
        global redValue_not_pressed
        global greenValue_not_pressed
        global blueValue_not_pressed
        if self.ids.button_0.text == "Button 0*":
            button_value = dpiComputer.readRGBButtonSwitch(0)  # read the button
            if button_value == True:
                if redValue_pressed == "" or greenValue_pressed == "" or blueValue_pressed == "":
                    red = 255
                    green = 0
                    blue = 0

                else:
                    red = int(redValue_pressed)
                    green = int(greenValue_pressed)
                    blue = int(blueValue_pressed)
                self.ids.button_value.text = "Button pressed"
                dpiComputer.writeRGBButtonColor(0, red, green, blue)  # set button to RED if pushed
            else:
                if redValue_not_pressed == "" or greenValue_not_pressed == "" or blueValue_not_pressed == "":
                    red = 64
                    green = 240
                    blue = 255

                else:
                    red = int(redValue_not_pressed)
                    green = int(greenValue_not_pressed)
                    blue = int(blueValue_not_pressed)
                self.ids.button_value.text = "Button not pressed"
                dpiComputer.writeRGBButtonColor(0, red, green, blue)

        if self.ids.button_1.text == "Button 1*":
            button_value = dpiComputer.readRGBButtonSwitch(1)  # read the button
            if button_value == True:
                if redValue_pressed == "" or greenValue_pressed == "" or blueValue_pressed == "":
                    red = 255
                    green = 0
                    blue = 0

                else:
                    red = int(redValue_pressed)
                    green = int(greenValue_pressed)
                    blue = int(blueValue_pressed)
                self.ids.button_value.text = "Button pressed"
                dpiComputer.writeRGBButtonColor(1, red, green, blue)  # set button to RED if pushed
            else:
                if (redValue_not_pressed == "") or (greenValue_not_pressed == "") or (blueValue_not_pressed == ""):
                    red = 64
                    green = 240
                    blue = 255

                else:
                    red = int(redValue_not_pressed)
                    green = int(greenValue_not_pressed)
                    blue = int(blueValue_not_pressed)
                self.ids.button_value.text = "Button not pressed"
                dpiComputer.writeRGBButtonColor(1, red, green, blue)


class StepperStartupScreen(Screen):
    """
    Class to handle the Stepper Startup screen and its associated touch events. This screen is used to home the motor
    """
    stepper_num = ""
    homingUnits = ""
    homingType = ""
    stepperLinearHomeValue = ""
    stepperAngularHomeValue = ""
    homingDirection = ""
    homingSpeed = ""
    homeMaxDistance = ""
    hasTransmission = False
    gearRatio = ""

    def __init__(self, **kwargs):
        Builder.load_file('StepperStartupScreen.kv')
        super(StepperStartupScreen, self).__init__(**kwargs)
        dpiStepper.setMicrostepping(16)

    def transition_back(self):
        """
        Transition back to the main screen. reset buttons and labels. Disable motors
        :return:
        """
        global homingSpeed
        global homeMaxDistance
        global gearRatio
        gearRatio = ""
        homeMaxDistance = ""
        homingSpeed = ""
        self.ids.enable_motor.text = "Enable all motors"
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2"
        self.ids.home_speed.text = "Home Speed:"
        self.ids.gearRatio_value.text = "Gear Ratio"
        self.ids.home_max_distance.text = "Home Max Distance:"
        self.ids.rotational_homing.text = "Rotational Homing"
        self.ids.linear_homing.text = "Linear Homing"
        self.ids.CCW_homing.text = "CCW To Home"
        self.ids.CW_homing.text = "CW To Home"
        self.ids.steps_homing.text = "Home in Steps"
        self.ids.revolutions_homing.text = "Home in Revolutions"
        self.ids.millimeters_homing.text = "Home in Millimeters"
        self.ids.transmission.text = "Has Transmission"

        self.ids.home_speed.text = "Home Speed " + homingSpeed
        self.ids.home_max_distance.text = "Home Max Distance:" + homeMaxDistance
        self.ids.gearRatio_value.text = "Gear Ratio " + gearRatio + " to 1"

        dpiStepper.enableMotors(False)
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        dpiStepper.enableMotors(False)
        quit()

    # enables/disables motors
    def enableMotors(self):
        if self.ids.enable_motor.text == "Enable all motors":
            dpiStepper.enableMotors(True)
            self.ids.enable_motor.text = "Disable all motors"
        else:
            dpiStepper.enableMotors(False)
            self.ids.enable_motor.text = "Enable all motors"

    # selects stepper 0 to home
    def selectStepper0(self):
        global stepper_num
        global gearRatio
        global homeMaxDistance
        global homingSpeed
        homeMaxDistance = ""
        homingSpeed = ""
        gearRatio = ""
        stepper_num = "0"
        self.ids.motor_0.text = "Motor 0 *"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2"
        self.ids.home_speed.text = "Home Speed:"
        self.ids.gearRatio_value.text = "Gear Ratio"
        self.ids.home_max_distance.text = "Home Max Distance:"

    # Selects stepper 1 to home
    def selectStepper1(self):
        global stepper_num
        global gearRatio
        global homeMaxDistance
        global homingSpeed
        homeMaxDistance = ""
        homingSpeed = ""
        gearRatio = ""
        stepper_num = "1"
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1 *"
        self.ids.motor_2.text = "Motor 2"
        self.ids.home_speed.text = "Home Speed:"
        self.ids.gearRatio_value.text = "Gear Ratio"
        self.ids.home_max_distance.text = "Home Max Distance:"

    # selects stepper 2 to home
    def selectStepper2(self):
        global stepper_num
        global gearRatio
        global homeMaxDistance
        global homingSpeed
        homeMaxDistance = ""
        homingSpeed = ""
        gearRatio = ""
        stepper_num = "2"
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2*"
        self.ids.home_speed.text = "Home Speed:"
        self.ids.gearRatio_value.text = "Gear Ratio"
        self.ids.home_max_distance.text = "Home Max Distance:"

    # sets homing type to rotational
    def setRotationalHoming(self):
        global homingType
        homingType = "Rotational"
        self.ids.rotational_homing.text = "Rotational Homing *"
        self.ids.linear_homing.text = "Linear Homing"

    # sets homing type to linear
    def setLinearHoming(self):
        global homingType
        homingType = "Linear"
        self.ids.rotational_homing.text = "Rotational Homing"
        self.ids.linear_homing.text = "Linear Homing *"

    # changes value of hasTransmission to true or false
    def Transmission(self):
        global hasTransmission
        if self.ids.transmission.text == "Has Transmission":
            hasTransmission = True
            self.ids.transmission.text = "Has Transmission *"

        else:
            hasTransmission = False
            self.ids.transmission.text = "Has Transmission"

    # sets homing direction to CCW which is -1
    def setHomingDirectionToCCW(self):
        global homingDirection
        homingDirection = "-1"
        self.ids.CCW_homing.text = "CCW To Home *"
        self.ids.CW_homing.text = "CW To Home"

    # sets homing direction to CW which is 1
    def setHomingDirectionToCW(self):
        global homingDirection
        homingDirection = "1"
        self.ids.CCW_homing.text = "CCW To Home"
        self.ids.CW_homing.text = "CW To Home *"

    # sets homing units to steps/second
    def setHomingUnitsToSteps(self):
        global homingUnits
        homingUnits = "steps/second"
        self.ids.steps_homing.text = "Home in Steps *"
        self.ids.revolutions_homing.text = "Home in Revolutions"
        self.ids.millimeters_homing.text = "Home in Millimeters"

    # sets homing units to revolutions/second
    def setHomingUnitsToRevolutions(self):
        global homingUnits
        homingUnits = "rev/second"
        self.ids.steps_homing.text = "Home in Steps"
        self.ids.revolutions_homing.text = "Home in Revolutions *"
        self.ids.millimeters_homing.text = "Home in Millimeters"

    # sets homing units to millimeters/second
    def setHomingUnitsToMillimeters(self):
        global homingUnits
        homingUnits = "millimeters/second"
        self.ids.steps_homing.text = "Home in Steps"
        self.ids.revolutions_homing.text = "Home in Revolutions"
        self.ids.millimeters_homing.text = "Home in Millimeters *"

    # sets the speed the motor will travel to home with the appropriate units
    def setHomeSpeed(self, speed):
        global homingSpeed
        if self.ids.steps_homing.text == "Home in Steps *":
            homingSpeed += str(speed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + " steps/second"
        if self.ids.revolutions_homing.text == "Home in Revolutions *":
            homingSpeed += str(speed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + " revolutions/second"
        if self.ids.millimeters_homing.text == "Home in Millimeters *":
            homingSpeed += str(speed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + " millimeters/second"
        else:
            pass

    # sets the gear ratio between stepper and transmission
    def setGearRatio(self, ratio):
        global gearRatio
        if self.ids.transmission.text == "Has Transmission *":
            gearRatio += str(ratio)
            self.ids.gearRatio_value.text = "Gear Ratio " + gearRatio + " to 1"
        else:
            pass

    # removes input from keyboard associated with gearRatio
    def removeGearRatio(self):
        global gearRatio
        gearRatio = gearRatio[:-1]
        self.ids.gearRatio_value.text = "Gear Ratio " + gearRatio + " to 1"

    # deletes input from speed keyboard
    def removeSpeedNumber(self):
        global homingSpeed
        if self.ids.steps_homing.text == "Home in Steps *":
            print(homingSpeed)
            homingSpeed = homingSpeed[:-1]
            print(homingSpeed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + "steps/second"
        if self.ids.revolutions_homing.text == "Home in Revolutions *":
            print(homingSpeed)
            homingSpeed = homingSpeed[:-1]
            print(homingSpeed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + "revolutions/second"
        if self.ids.millimeters_homing.text == "Home in Millimeters *":
            print(homingSpeed)
            homingSpeed = homingSpeed[:-1]
            print(homingSpeed)
            self.ids.home_speed.text = "Home Speed " + homingSpeed + "millimeters/second"
        else:
            pass

    # sets the max distance with the appropriate units
    def setMaxDistance(self, distance):
        global homeMaxDistance
        if self.ids.steps_homing.text == "Home in Steps *":
            homeMaxDistance += str(distance)
            self.ids.home_max_distance.text = "Home Max Distance:\n " + homeMaxDistance + " steps"
        if self.ids.revolutions_homing.text == "Home in Revolutions *":
            homeMaxDistance += str(distance)
            self.ids.home_max_distance.text = "Home Max Distance:\n " + homeMaxDistance + " revolutions"
        if self.ids.millimeters_homing.text == "Home in Millimeters *":
            homeMaxDistance += str(distance)
            self.ids.home_max_distance.text = "Home Max Distance:\n " + homeMaxDistance + " millimeters"
        else:
            pass

    # removes input from distance keyboard
    def removeDistanceNumber(self):
        global homeMaxDistance
        if self.ids.steps_homing.text == "Home in Steps *":
            print(homeMaxDistance)
            homeMaxDistance = homeMaxDistance[:-1]
            print(homeMaxDistance)
            self.ids.home_max_distance.text = "Home Max Distance:\n " + homeMaxDistance + "steps"
        if self.ids.revolutions_homing.text == "Home in Revolutions *":
            print(homeMaxDistance)
            homeMaxDistance = homeMaxDistance[:-1]
            print(homeMaxDistance)
            self.ids.home_max_distance.text = "Home Max Distance:\n " + homeMaxDistance + "revolutions"
        if self.ids.millimeters_homing.text == "Home in Millimeters *":
            print(homeMaxDistance)
            homeMaxDistance = homeMaxDistance[:-1]
            print(homeMaxDistance)
            self.ids.home_max_distance.text = "Home Max Distance\n " + homeMaxDistance + "millimeters"
        else:
            pass

    # homes the motor based on given input
    def homeMotor(self):
        global homingDirection
        global homeMaxDistance
        global homingSpeed
        global homingType
        global gearRatio
        global homingUnits
        global hasTransmission
        try:
            self.ids.error_stepper_home.text = ""
            if homingType == "Linear":
                if hasTransmission:
                    if homingUnits == "steps/second":
                        dpiStepper.moveToHomeInSteps(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                     int(homeMaxDistance) * int(gearRatio))
                    if homingUnits == "rev/second":
                        dpiStepper.moveToHomeInRevolutions(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance) * int(gearRatio))
                    if homingUnits == "millimeters/second":
                        dpiStepper.moveToHomeInMillimeters(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance) * int(gearRatio))


                else:
                    if homingUnits == "steps/second":
                        dpiStepper.moveToHomeInSteps(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                     int(homeMaxDistance))
                    if homingUnits == "rev/second":
                        dpiStepper.moveToHomeInRevolutions(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance))
                    if homingUnits == "millimeters/second":
                        dpiStepper.moveToHomeInMillimeters(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance))

            if homingType == "Rotational":
                if hasTransmission:
                    if homingUnits == "steps/second":
                        dpiStepper.moveToHomeInSteps(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                     int(homeMaxDistance) * int(gearRatio))
                    if homingUnits == "rev/second":
                        dpiStepper.moveToHomeInRevolutions(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance) * int(gearRatio))
                    if homingUnits == "millimeters/second":
                        dpiStepper.moveToHomeInMillimeters(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance) * int(gearRatio))


                else:
                    if homingUnits == "steps/second":
                        dpiStepper.moveToHomeInSteps(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                     int(homeMaxDistance))
                    if homingUnits == "rev/second":
                        dpiStepper.moveToHomeInRevolutions(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance))
                    if homingUnits == "millimeters/second":
                        dpiStepper.moveToHomeInMillimeters(int(stepper_num), int(homingDirection), int(homingSpeed),
                                                           int(homeMaxDistance))
            else:
                pass

        except ValueError:
            self.ids.error_stepper_home.text = "Invalid input, review instructions again"


class StepperScreen(Screen):
    """
    Class to handle the StepperScreen and its functionality
    """
    microStepping = ""
    stepperSpeed = ""
    stepperAcceleration = ""
    stepper0Distance = ""
    stepper1Distance = ""
    stepper2Distamce = ""
    stepper_num = ""
    stepperLinearHomeValue = ""
    stepperAngularHomeValue = ""
    distanceUnits = ""
    direction = ""

    # checks to see if board is connected properly
    if dpiStepper.initialize() != True:
        print("Communication with the DPiStepper board failed.")

    # finds the velocity of given stepper
    def getVelocity(self, dt):
        global stepper_num
        global distanceUnits
        try:
            if distanceUnits == "steps":
                velocity = tuple(dpiStepper.getCurrentVelocityInStepsPerSecond(int(stepper_num)))
                self.ids.velocity.text = "Velocity: " + str(velocity[1]) + " steps/second"
            if distanceUnits == "revolutions":
                velocity = tuple(dpiStepper.getCurrentVelocityInRevolutionsPerSecond(int(stepper_num)))
                self.ids.velocity.text = "Velocity: " + str(velocity[1]) + " revolutions/second"
            if distanceUnits == "millimeters":
                velocity = tuple(dpiStepper.getCurrentVelocityInMillimetersPerSecond(int(stepper_num)))
                self.ids.velocity.text = "Velocity: " + str(velocity[1]) + " millimeters/second"

        except ValueError:
            pass

    # uses a clock to keep updating velocity
    def __init__(self, **kwargs):
        Builder.load_file('StepperScreen.kv')
        super(StepperScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.getVelocity, .001)
        dpiStepper.enableMotors(False)

    def transition_back(self):
        """
        Transition back to the main screen, disable motors, deselect buttons
        :return:
        """

        dpiStepper.enableMotors(False)
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2"
        self.ids.speed_value.text = "Speed:"
        self.ids.acceleration_value.text = "Accel:"
        self.ids.micro_value.text = "Microstepping:"
        self.ids.distance_value.text = "Distance:"

        self.ids.steps.text = "Steps"
        self.ids.revolution.text = "Revolutions"
        self.ids.milli.text = "Millimeters"

        self.ids.CCW_movement.text = "CCW Direction"
        self.ids.CW_Movement.text = "CW Direction"

        self.ids.enable_motor.text = "Enable all motors"
        SCREEN_MANAGER.current = STEPPER_STARTUP_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program. This should disable all steppers and do any cleanup necessary
        :return: None
        """
        dpiStepper.enableMotors(False)
        quit()

    # enables or disables all  stepper motors
    def enableMotors(self):
        if self.ids.enable_motor.text == "Enable all motors":
            dpiStepper.enableMotors(True)
            self.ids.enable_motor.text = "Disable all motors"
        else:
            dpiStepper.enableMotors(False)
            self.ids.enable_motor.text = "Enable all motors"

    # rotates Stepper motor  CW one time
    def runBasicMotionCW(self):
        global stepper_num
        microstepping = 8
        try:
            self.ids.error_stepper.text = ""
            dpiStepper.setMicrostepping(microstepping)
            speed_steps_per_second = 200 * microstepping
            accel_steps_per_second_per_second = speed_steps_per_second
            dpiStepper.setSpeedInStepsPerSecond(int(stepper_num), speed_steps_per_second)
            dpiStepper.setAccelerationInStepsPerSecondPerSecond(int(stepper_num), accel_steps_per_second_per_second)
            steps = 1600
            wait_to_finish_moving_flg = True
            dpiStepper.moveToRelativePositionInSteps(int(stepper_num), steps, wait_to_finish_moving_flg)

        except ValueError:
            self.ids.error_stepper.text = "Invalid input, review instructions again"

    # sets distanceUnits to steps
    def setUnitsToSteps(self):
        global distanceUnits
        distanceUnits = "steps"
        self.ids.steps.text = "Steps *"
        self.ids.revolution.text = "Revolutions"
        self.ids.milli.text = "Millimeters"

    # sets distanceUnits to revolutions
    def setUnitsToRevolutions(self):
        global distanceUnits
        distanceUnits = "revolutions"
        self.ids.steps.text = "Steps"
        self.ids.revolution.text = "Revolutions *"
        self.ids.milli.text = "Millimeters"

    # sets distanceUnits to millimeters
    def setUnitsToMillimeters(self):
        global distanceUnits
        distanceUnits = "millimeters"
        self.ids.steps.text = "Steps"
        self.ids.revolution.text = "Revolutions"
        self.ids.milli.text = "Millimeters *"

    # rotates stepper motor CCW one time
    def runBasicMotionCCW(self):
        global stepper_num
        try:
            self.ids.error_stepper.text = ""
            microstepping = 8
            dpiStepper.setMicrostepping(microstepping)
            speed_steps_per_second = 200 * microstepping
            accel_steps_per_second_per_second = speed_steps_per_second
            dpiStepper.setSpeedInStepsPerSecond(int(stepper_num), speed_steps_per_second)
            dpiStepper.setAccelerationInStepsPerSecondPerSecond(int(stepper_num), accel_steps_per_second_per_second)

            steps = -1600
            wait_to_finish_moving_flg = True
            dpiStepper.moveToRelativePositionInSteps(int(stepper_num), steps, wait_to_finish_moving_flg)

        except ValueError:
            self.ids.error_stepper.text = "Invalid input, review instructions again"

    # sets stepper_num to 0
    def selectStepper0(self):
        global stepper_num
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        global microStepping
        global stepperSpeed
        global stepperAcceleration
        stepper0Distance = ""
        stepper1Distance = ""
        stepper2Distance = ""
        microStepping = ""
        stepperSpeed = ""
        stepperAcceleration = ""
        stepper_num = "0"
        self.ids.motor_0.text = "Motor 0 *"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2"
        self.ids.speed_value.text = "Speed:"
        self.ids.acceleration_value.text = "Accel:"
        self.ids.micro_value.text = "Microstepping:"
        self.ids.distance_value.text = "Distance:"

    # sets stepper_num to 1
    def selectStepper1(self):
        global stepper_num
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        global microStepping
        global stepperSpeed
        global stepperAcceleration
        stepper0Distance = ""
        stepper1Distance = ""
        stepper2Distance = ""
        microStepping = ""
        stepperSpeed = ""
        stepperAcceleration = ""
        stepper_num = "1"
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1 *"
        self.ids.motor_2.text = "Motor 2"
        self.ids.speed_value.text = "Speed:"
        self.ids.acceleration_value.text = "Accel:"
        self.ids.micro_value.text = "Microstepping:"
        self.ids.distance_value.text = "Distance:"

    # sets stepper_num to 2
    def selectStepper2(self):
        global stepper_num
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        global microStepping
        global stepperSpeed
        global stepperAcceleration
        stepper0Distance = ""
        stepper1Distance = ""
        stepper2Distance = ""
        microStepping = ""
        stepperSpeed = ""
        stepperAcceleration = ""
        stepper_num = "2"
        self.ids.motor_0.text = "Motor 0"
        self.ids.motor_1.text = "Motor 1"
        self.ids.motor_2.text = "Motor 2 *"
        self.ids.speed_value.text = "Speed:"
        self.ids.acceleration_value.text = "Accel:"
        self.ids.micro_value.text = "Microstepping:"
        self.ids.distance_value.text = "Distance:"

    # sets direction to CCW which is -1
    def CCWMovement(self):
        global direction
        direction = "-1"
        self.ids.CCW_movement.text = "CCW Direction *"
        self.ids.CW_Movement.text = "CW Direction"

    # sets direction to CW which is 1
    def CWMovement(self):
        global direction
        direction = "1"
        self.ids.CCW_movement.text = "CCW Direction"
        self.ids.CW_Movement.text = "CW Direction *"

    # remove input from microstepping keyboard
    def removeNumMicrostepping(self):
        global microStepping
        print(microStepping)
        microStepping = microStepping[:-1]
        print(microStepping)
        self.ids.micro_value.text = 'Microstepping: ' + microStepping

    # remove input from speed keyboard
    def removeNumSpeed(self):
        global stepperSpeed
        global distanceUnits
        stepperSpeed = stepperSpeed[:-1]
        self.ids.speed_value.text = 'Speed: ' + stepperSpeed + " " + distanceUnits + "sec"

    # remove input from acceleration keyboard
    def removeNumAcceleration(self):
        global stepperAcceleration
        global distanceUnits
        stepperAcceleration = stepperAcceleration[:-1]
        self.ids.acceleration_value.text = 'Acceleration: ' + stepperAcceleration + " " + distanceUnits + "sec^2"

    # reads microstepping input from keyboard
    def readMicroStepping(self, microStep):
        print("setting Microstepping")
        global microStepping
        microStepping += str(microStep)
        dpiStepper.setMicrostepping(int(microStepping))
        self.ids.micro_value.text = 'Microstepping: ' + microStepping
        print(microStepping)

    # sets speed of stepper motor
    def setSpeed(self, speed):
        print("setting speed")
        global stepperSpeed
        global stepper_num
        global distanceUnits
        if self.ids.steps.text == "Steps *":
            stepperSpeed += str(speed)
            dpiStepper.setSpeedInStepsPerSecond(int(stepper_num), int(stepperSpeed))
            self.ids.speed_value.text = 'Speed: ' + stepperSpeed + " " + distanceUnits + "/sec"

        if self.ids.revolution.text == "Revolutions *":
            stepperSpeed += str(speed)
            dpiStepper.setSpeedInRevolutionsPerSecond(int(stepper_num), int(stepperSpeed))
            self.ids.speed_value.text = 'Speed: ' + stepperSpeed + " " + distanceUnits + "/sec"

        if self.ids.milli.text == "Millimeters *":
            stepperSpeed += str(speed)
            dpiStepper.setSpeedInMillimetersPerSecond(int(stepper_num), int(stepperSpeed))
            self.ids.speed_value.text = 'Speed: ' + stepperSpeed + " " + distanceUnits + "/sec"

    # sets acceleration for stepper motor
    def setAcceleration(self, Acceleration):
        global stepperAcceleration
        global stepper_num
        global distanceUnits
        if self.ids.steps.text == "Steps *":
            stepperAcceleration += str(Acceleration)
            dpiStepper.setAccelerationInStepsPerSecondPerSecond(int(stepper_num), int(stepperAcceleration))
            self.ids.acceleration_value.text = 'Accel: ' + stepperAcceleration + " " + distanceUnits + "/sec^2"

        if self.ids.revolution.text == "Revolutions *":
            stepperAcceleration += str(Acceleration)
            dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(int(stepper_num), int(stepperAcceleration))
            self.ids.acceleration_value.text = 'Accel: ' + stepperAcceleration + " " + distanceUnits + "/sec^2"

        if self.ids.milli.text == "Millimeters *":
            stepperAcceleration += str(Acceleration)
            dpiStepper.setAccelerationInMillimetersPerSecondPerSecond(int(stepper_num), int(stepperAcceleration))
            self.ids.acceleration_value.text = 'Accel: ' + stepperAcceleration + " " + distanceUnits + "/sec^2"

    # sets the number of steps using keyboard input
    def setDistance(self, numSteps):
        print("setting number of steps")
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        global distanceUnits
        if self.ids.motor_0.text == "Motor 0 *":
            stepper0Distance += str(numSteps)
            self.ids.distance_value.text = 'Distance: ' + stepper0Distance + " " + distanceUnits
        if self.ids.motor_1.text == "Motor 1 *":
            stepper1Distance += str(numSteps)
            self.ids.distance_value.text = 'Distance: ' + stepper1Distance + " " + distanceUnits
        if self.ids.motor_2.text == "Motor 2 *":
            stepper2Distance += str(numSteps)
            self.ids.distance_value.text = 'Distance: ' + stepper2Distance + " " + distanceUnits
        else:
            pass

    # delete keyboard input for steps
    def removeDistance(self):
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        if self.ids.motor_0.text == "Motor 0 *":
            print(stepper0Distance)
            stepper0Distance = stepper0Distance[:-1]
            print(stepper0Distance)
            self.ids.distance_value.text = 'Distance: ' + stepper0Distance + " " + distanceUnits
        if self.ids.motor_1.text == "Motor 1 *":
            print(stepper1Distance)
            stepper1Distance = stepper1Distance[:-1]
            print(stepper1Distance)
            self.ids.distance_value.text = 'Distance: ' + stepper1Distance + " " + distanceUnits
        if self.ids.motor_2.text == "Motor 2 *":
            print(stepper2Distance)
            stepper2Distance = stepper2Distance[:-1]
            print(stepper2Distance)
            self.ids.distance_value.text = 'Distance: ' + stepper2Distance + " " + distanceUnits
        else:
            pass

    # rotates all steppers with given input
    def runInput(self):
        global stepper0Distance
        global stepper1Distance
        global stepper2Distance
        global distanceUnits
        global direction
        try:
            self.ids.error_stepper.text = ""
            wait_to_finish_moving_flg = False
            if distanceUnits == "steps":
                dpiStepper.moveToRelativePositionInSteps(0, int(stepper0Distance) * int(direction),
                                                         wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInSteps(1, int(stepper1Distance) * int(direction),
                                                         wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInSteps(2, int(stepper2Distance) * int(direction),
                                                         wait_to_finish_moving_flg)
            if distanceUnits == "revolutions":
                dpiStepper.moveToRelativePositionInRevolutions(0, int(stepper0Distance) * int(direction),
                                                               wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInRevolutions(1, int(stepper1Distance) * int(direction),
                                                               wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInRevolutions(2, int(stepper2Distance) * int(direction),
                                                               wait_to_finish_moving_flg)

            if distanceUnits == "millimeters":
                dpiStepper.moveToRelativePositionInMillimeters(0, int(stepper0Distance) * int(direction),
                                                               wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInMillimeters(1, int(stepper1Distance) * int(direction),
                                                               wait_to_finish_moving_flg)
                dpiStepper.moveToRelativePositionInMillimeters(2, int(stepper2Distance) * int(direction),
                                                               wait_to_finish_moving_flg)
        except ValueError:
            self.ids.error_stepper.text = "Invalid input, review instructions again"

    # get status of stepper motor
    def getStatus(self):
        global stepper_num
        temp = ""
        try:
            self.ids.error_stepper.text = ""
            if int(stepper_num) == 0:
                stepperStatus = tuple(dpiStepper.getStepperStatus(int(stepper_num)))
                for item in stepperStatus:
                    temp += str(item) + ', '
                self.ids.status.text = "Status: " + temp

            if int(stepper_num) == 1:
                stepperStatus = tuple(dpiStepper.getStepperStatus(int(stepper_num)))
                for item in stepperStatus:
                    temp += str(item) + ', '
                self.ids.status.text = "Status: " + temp

            if int(stepper_num) == 2:
                stepperStatus = tuple(dpiStepper.getStepperStatus(int(stepper_num)))
                for item in stepperStatus:
                    temp += str(item) + ', '
                self.ids.status.text = "Status: " + temp

        except ValueError:
            self.ids.error_stepper.text = "Invalid input, review intructions again"

    # outputs position on screen
    def getPosition(self):
        global stepper_num
        global distanceUnits
        try:
            print(stepper_num)
            self.ids.error_stepper.text = ""
            if distanceUnits == "steps":
                position = tuple(dpiStepper.getCurrentPositionInSteps(int(stepper_num)))
                self.ids.position.text = "Position: " + str(position[1]) + " steps"
            if distanceUnits == "revolutions":
                position = tuple(dpiStepper.getCurrentPositionInRevolutions(int(stepper_num)))
                self.ids.position.text = "Position: " + str(position[1]) + " revolutions"
            if distanceUnits == "millimeters":
                position = tuple(dpiStepper.getCurrentPositionInMillimeters(int(stepper_num)))
                self.ids.position.text = "Position: " + str(position[1]) + " millimeters"

        except ValueError:
            self.ids.error_stepper.text = "Invalid input, review instructions again"


class ServoScreen(Screen):
    """
    Class to handle the ServoScreen and its functionality
    """
    my_angle0 = ""
    my_angle1 = ""
    servo_number = ""

    def __init__(self, **kwargs):
        """
        Load the ServoScreen.kv file.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('ServoScreen.kv')
        super(ServoScreen, self).__init__(**kwargs)

    def transition_back(self):
        """
        Transition back to the main screen. Reset all buttons
        :return:
        """
        global my_angle1
        global my_angle0
        my_angle0 = ""
        my_angle1 = ""
        self.ids.servo_0.text = "Servo 0"
        self.ids.servo_1.text = "Servo 1"
        self.ids.angle_lable.text = 'Servo angle: ' + my_angle0 + my_angle1
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program.
        :return: None
        """
        quit()

    # selects servo 0 to input data or run basic movement
    def selectServo0(self):
        global servo_number
        servo_number = str(0)
        self.ids.servo_0.text = "Servo 0 *"
        self.ids.servo_1.text = "Servo 1"

    # selects servo 1 to input data or run basic movement
    def selectServo1(self):
        global servo_number
        servo_number = str(1)
        self.ids.servo_0.text = "Servo 0"
        self.ids.servo_1.text = "Servo 1 *"

    # rotates servo motor 180 degrees, then back to 0 degrees
    def rotateServo(self):
        global servo_number
        try:
            self.ids.error_servo.text = ""
            i = 0
            for i in range(180):
                dpiComputer.writeServo(int(servo_number), i)
            sleep(1.5)
            for i in range(180, 0, -1):
                dpiComputer.writeServo(int(servo_number), i)

        except ValueError:
            self.ids.error_servo.text = "Invalid input, review instructions again"

    # use keyboard to input desired angle, range 0-180
    def setServoAngle(self, ang):
        print("setting angle")
        global my_angle0
        global my_angle1
        if self.ids.servo_0.text == "Servo 0 *":
            my_angle0 += str(ang)
            self.ids.angle_lable.text = 'Servo angle: ' + my_angle0
            print(my_angle0)
        if self.ids.servo_1.text == "Servo 1 *":
            my_angle1 += str(ang)
            self.ids.angle_lable.text = 'Servo angle: ' + my_angle1
            print(my_angle1)
        else:
            pass

    # delete number from keyboard input
    def removeNum(self):
        global my_angle0
        global my_angle1
        if self.ids.servo_0.text == "Servo 0 *":
            print(my_angle0)
            my_angle0 = my_angle0[:-1]
            print(my_angle0)
            self.ids.angle_lable.text = 'Servo angle: ' + my_angle0
        if self.ids.servo_1.text == "Servo 1 *":
            print(my_angle1)
            my_angle1 = my_angle1[:-1]
            print(my_angle1)
            self.ids.angle_lable.text = 'Servo angle: ' + my_angle1
        else:
            pass

    # rotate servo to inputted angle
    def rotateServoToAngle(self):
        global my_angle0
        global my_angle1
        print(my_angle1)
        try:
            self.ids.error_servo.text = ""
            if self.ids.servo_0.text == "Servo 0 *":
                dpiComputer.writeServo(0, int(my_angle0))
            if self.ids.servo_1.text == "Servo 1 *":
                dpiComputer.writeServo(1, int(my_angle1))

        except ValueError:
            self.ids.error_servo.text = "Invalid input, review instructions again"


class DCScreen(Screen):
    """
    Class to handle the DCScreen and its functionality
    """
    # variable used for speed and direction of DC motor. Range 0-180, 90 has the motor stop
    speedDC0 = ""
    speedDC1 = ""
    global servo_number

    def __init__(self, **kwargs):
        Builder.load_file('DCScreen.kv')
        super(DCScreen, self).__init__(**kwargs)

    def transition_back(self):
        """
        Transition back to the main screen, reset all buttons, stops motors
        :return:
        """
        global speedDC1
        global speedDC0
        speedDC0 = ""
        speedDC1 = ""
        self.ids.DC_0.text = "DC 0"
        self.ids.DC_1.text = "DC 1"
        self.ids.speed_value.text = 'Speed: ' + speedDC0 + speedDC1
        dpiComputer.writeServo(0, 90)
        dpiComputer.writeServo(1, 90)
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def exit_program():
        """
        Quit the program. Stops motors
        :return: None
        """
        dpiComputer.writeServo(0, 90)
        dpiComputer.writeServo(1, 90)
        quit()

    # selects DC 0 to input speed or run basic movement
    def selectDC0(self):
        global servo_number
        servo_number = str(0)
        self.ids.DC_0.text = "DC 0 *"
        self.ids.DC_1.text = "DC 1"

    # selects DC 1to input speed or run basic movement
    def selectDC1(self):
        global servo_number
        servo_number = str(1)
        self.ids.DC_0.text = "DC 0"
        self.ids.DC_1.text = "DC 1 *"

    # rotates the DC motor for 10 seconds
    def rotateDCMotor(self):
        print("rotating DC motor")
        global servo_number
        try:
            self.ids.error_DC.text = ""
            dpiComputer.writeServo(int(servo_number), 40)
            sleep(10)
            dpiComputer.writeServo(int(servo_number), 90)
            print("finished rotating")

        except ValueError:
            self.ids.error_DC.text = "Invalid Input, review instructions again"

    # uses keyboard to input speed/direction of DC Motor. Range 0-180, 90 has the motor stop
    def setSpeed(self, number):
        print("setting speed")
        global speedDC0
        global speedDC1
        if self.ids.DC_0.text == "DC 0 *":
            speedDC0 += str(number)
            self.ids.speed_value.text = 'Speed: ' + speedDC0
        if self.ids.DC_1.text == "DC 1 *":
            speedDC1 += str(number)
            self.ids.speed_value.text = 'Speed: ' + speedDC1
        else:
            pass

    # delete number from keyboard input
    def removeNum(self):
        global speedDC0
        global speedDC1
        if self.ids.DC_0.text == "DC 0 *":
            print(speedDC0)
            speedDC0 = speedDC0[:-1]
            self.ids.speed_value.text = 'Speed: ' + speedDC0
            print(speedDC0)
        if self.ids.DC_1.text == "DC 1 *":
            print(speedDC1)
            speedDC1 = speedDC1[:-1]
            self.ids.speed_value.text = 'Speed: ' + speedDC1
            print(speedDC1)
        else:
            pass

    # Runs DC motor with inputted speed until stop motor button pressed
    def runDCWithSpecificSpeed(self):
        print("rotating DC motor")
        global servo_number
        global speedDC0
        global speedDC1
        try:
            self.ids.error_DC.text = ""
            if self.ids.DC_0.text == "DC 0 *":
                dpiComputer.writeServo(0, int(speedDC0))
            if self.ids.DC_1.text == "DC 1 *":
                dpiComputer.writeServo(1, int(speedDC1))

        except ValueError:
            self.ids.error_DC.text = "Invalid input, review instructions"

    # stops all motors currently running
    def stopDCMotors(self):
        dpiComputer.writeServo(0, 90)
        dpiComputer.writeServo(1, 90)


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(StepperScreen(name=STEPPER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ServoScreen(name=SERVO_SCREEN_NAME))
SCREEN_MANAGER.add_widget(DCScreen(name=DC_SCREEN_NAME))
SCREEN_MANAGER.add_widget(StepperStartupScreen(name=STEPPER_STARTUP_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ButtonScreen(name=BUTTON_SCREEN_NAME))
SCREEN_MANAGER.add_widget(InputScreen(name=INPUT_SCREEN_NAME))
SCREEN_MANAGER.add_widget(OutputScreen(name=OUTPUT_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NeopixelScreen(name=NEOPIXEL_SCREEN_NAME))
SCREEN_MANAGER.add_widget(EncoderScreen(name=ENCODER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PotentiometerScreen(name=POTENTIOMETER_SCREEN_NAME))
"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
