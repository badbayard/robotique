from classes import *
from ev3dev.ev3 import *
try:
    from typing import Union, Optional, List
except ImportError:
    pass


class RealBot(Bot):
    DEFAULT_SPEED = 200
    CORRECT_SPEED = 40
    DEFAULT_ROTATE_SPEED = 50
    PULSES_PER_CM = 35.2
    CM_PER_CELL = 30

    def __init__(self, motorL: LargeMotor, motorR: LargeMotor,
                 colorSensor: ColorSensor, *args, **kwargs):
        super(RealBot, self).__init__(*args, **kwargs)
        self.motorL, self.motorR = motorL, motorR
        self.colorSensor = colorSensor

    def move_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        end = self.motorL.position + self.PULSES_PER_CM * cm
        while self.motorL.position <= end:
            col = BoardColor.from_itensity(
                self.colorSensor.reflected_light_intensity)
            #print("{} {} {} {} {}".format(col, self.motorL.position, end, speed, self.CORRECT_SPEED))
            if col == DirectionColorMap[self.dir][1]:
                self.motorL.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                self.motorR.run_forever(speed_sp=speed + self.CORRECT_SPEED)
            elif col == DirectionColorMap[self.dir][0]:
                self.motorL.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                self.motorR.run_forever(speed_sp=speed - self.CORRECT_SPEED)
        self.motorL.stop()
        self.motorR.stop()

    def wait_movement(self):
        self.motorL.wait_while('running')
        self.motorR.wait_while('running')

    def forward_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.move_cm(cm, speed)

    def forward(self, count: int = 1, speed: float = DEFAULT_SPEED,
                *args, **kwargs) -> None:
        raise NotImplementedError

    def backward_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.move_cm(-cm, speed)

    def backward(self, count: int = 1, speed: float = DEFAULT_SPEED,
                 *args, **kwargs) -> None:
        raise NotImplementedError


if __name__ == '__main__':
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

    colorSensor = ColorSensor('in4')
    colorSensor.mode = 'COL-REFLECT'

    """fwdSensor = UltrasonicSensor('in1')
    fwdSensor.mode = 'US-DIST-CM'
    leftSensor = UltrasonicSensor('in2')
    leftSensor.mode = 'US-DIST-CM'
    rightSensor = UltrasonicSensor('in3')
    rightSensor.mode = 'US-DIST-CM'"""

    mB = LargeMotor('outB')
    mC = LargeMotor('outC')

    b = Board(8, 8)
    bot = RealBot(board=b, motorL=mB, motorR=mC, colorSensor=colorSensor)
    bot.dir = Direction.West
    bot.forward_cm(210)
