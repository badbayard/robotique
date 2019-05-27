from classes import *
from ev3dev.ev3 import *
from time import sleep
from collections import deque, Counter
try:
    from typing import Union, Optional, List
except ImportError:
    pass


def most_frequent(l):
    occurence_count = Counter(l)
    return occurence_count.most_common(1)[0][0]


class RealBot(Bot):
    DEFAULT_SPEED = 200
    CORRECT_SPEED = 40
    DEFAULT_ROTATE_SPEED = 50
    PULSES_PER_CM = 35.2
    PULSES_PER_DEG = None
    CM_PER_CELL = 30

    def __init__(self, motor_l: LargeMotor, motor_r: LargeMotor,
                 color_sensor: ColorSensor, *args, **kwargs):
        super(RealBot, self).__init__(*args, **kwargs)
        self.motor_l, self.motor_r = motor_l, motor_r
        self.colorSensor = color_sensor

    def move_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        end = self.motor_l.position + self.PULSES_PER_CM * cm
        while self.motor_l.position <= end:
            col = BoardColor.from_itensity(
                self.colorSensor.reflected_light_intensity)
            if col == DirectionColorMap[self.dir][1]:
                self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
            elif col == DirectionColorMap[self.dir][0]:
                self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
        self.motor_l.stop()
        self.motor_r.stop()

    def wait_movement(self):
        self.motor_l.wait_while('running')
        self.motor_r.wait_while('running')

    def forward_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.move_cm(cm, speed)

    def forward(self, count: int = 1, speed: float = DEFAULT_SPEED,
                *args, **kwargs) -> None:
        self.forward_cm(count * self.CM_PER_CELL, speed)

    def backward_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.move_cm(-cm, speed)

    def backward(self, count: int = 1, speed: float = DEFAULT_SPEED,
                 *args, **kwargs) -> None:
        self.backward_cm(count * self.CM_PER_CELL, speed)

    def turn_left(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        raise NotImplementedError

    def turn_right(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        self.motor_l.stop()
        self.motor_r.stop()

    def rotate_left(self, speed: float):
        self.motor_l.run_forever(speed_sp=-1 * speed)
        self.motor_r.run_forever(speed_sp=speed)

    def rotate_right(self, speed: float):
        self.motor_l.run_forever(speed_sp=speed)
        self.motor_r.run_forever(speed_sp=-1 * speed)

    def find_direction(self):
        print("Detection direction cardinale:")
        sliding_colors = deque(maxlen=5)

        print("- Bande de couleur... ", end='')
        color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
        if color in (BoardColor.Unknown, BoardColor.Wood):
            self.rotate_left(140)
            sliding_colors.append(color)
            while most_frequent(sliding_colors) in (BoardColor.Unknown, BoardColor.Wood):
                color = BoardColor.from_itensity(
                    colorSensor.reflected_light_intensity)
                sliding_colors.append(color)
                sleep(0.05)
        first_color = color
        print(str(first_color))

        print("- Detection 2eme bande... ", end='')
        self.rotate_right(70)
        sliding_colors.clear()
        while True:
            color = BoardColor.from_itensity(
                colorSensor.reflected_light_intensity)
            avgcolor = sliding_colors.append(color)
            if color != first_color and color != BoardColor.Unknown:
                break
            sleep(0.05)
        self.rotate_left(70)
        sliding_colors.clear()
        while True:
            color = BoardColor.from_itensity(
                colorSensor.reflected_light_intensity)
            avgcolor = sliding_colors.append(color)
            if color == first_color:
                break
            sleep(0.05)
        '''while True:
            color = BoardColor.from_itensity(
                colorSensor.reflected_light_intensity)
            avgcolor = sliding_colors.append(color)
            if color != first_color and color not in (
            BoardColor.Unknown, BoardColor.Wood):
                break
            sleep(0.05)'''
        self.stop()

        second_color = color
        print(str(second_color))

        dirmap = {
            (BoardColor.Red, BoardColor.Black): Direction.North,
            (BoardColor.Black, BoardColor.White): Direction.East,
            (BoardColor.Black, BoardColor.Red): Direction.South,
            (BoardColor.White, BoardColor.Black): Direction.West
        }
        direction = dirmap[(second_color, first_color)]
        self.dir = direction

        print("Direction: " + str(direction))


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
    bot = RealBot(board=b, motor_l=mB, motor_r=mC, color_sensor=colorSensor)
    bot.find_direction()
    bot.forward_cm(30*2)
