#!/usr/bin/env python3
from classes import *
from ev3dev.ev3 import *
from time import sleep
try:
    from typing import Union, Optional, List
except ImportError:
    pass


class ConsecutiveCounter:
    __slots__ = ['trigger', 'value', 'count']

    def __init__(self, trigger: int = 0, value=None, count=1):
        self.trigger = trigger
        self.value = value
        self.count = count

    def __call__(self, value):
        if value == self.value:
            self.count += 1
        else:
            self.value = value
            self.count = 1

    def reset(self):
        self.value = None
        self.count = 1

    @property
    def triggered(self):
        return self.count >= self.trigger

    def triggered_by(self, value):
        return self.count >= self.trigger and self.value == value


class BotCalibration:
    def __init__(self, color: BoardColorCalibration, pulses_per_cm: float):
        self.color = color
        self.pulses_per_cm = pulses_per_cm


class RealBot(Bot):
    DEFAULT_SPEED = 200
    CORRECT_SPEED = 40
    DEFAULT_ROTATE_SPEED = 100
    PULSES_PER_DEG = None
    CM_PER_CELL = 30

    def __init__(self, motor_l: LargeMotor, motor_r: LargeMotor,
                 color_sensor: ColorSensor,
                 calibration: BotCalibration,
                 *args, **kwargs):
        super(RealBot, self).__init__(*args, **kwargs)
        self.motor_l, self.motor_r = motor_l, motor_r
        self.color_sensor = color_sensor
        self.calibration = calibration

    def read_color(self) -> BoardColor:
        return BoardColor.from_itensity(
            self.color_sensor.reflected_light_intensity,
            self.calibration.color)

    def move_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        end = self.motor_l.position + self.calibration.pulses_per_cm * cm
        #correct_dir = None
        #supercorrecting = False
        #supercorrecting_start =  None
        while self.motor_l.position <= end:
            col = self.read_color()
            if col == DirectionColorMap[self.dir][1]:
                #if supercorrecting:
                #    supercorrecting = False
                #   end += self.motor_l.position - supercorrecting_start
                self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                #correct_dir = RelativeDirection.Left
            elif col == DirectionColorMap[self.dir][0]:
                #if supercorrecting:
                #    supercorrecting = False
                #    end += self.motor_l.position - supercorrecting_start
                self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                #correct_dir = RelativeDirection.Right
            '''else:
                supercorrecting = True
                supercorrecting_start = self.motor_l.position
                if correct_dir is None:
                    correct_dir = RelativeDirection.Right
                if correct_dir == RelativeDirection.Left:
                    self.motor_l.run_forever(
                        speed_sp=speed - self.CORRECT_SPEED)
                    self.motor_r.run_forever(
                        speed_sp=speed + self.CORRECT_SPEED)
                elif correct_dir == RelativeDirection.Right:
                    pass'''
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
        self.motor_l.run_to_rel_pos(position_sp=500, speed_sp=-speed)
        self.motor_r.run_to_rel_pos(position_sp=-500, speed_sp=speed)

        '''col_counter = ConsecutiveCounter(4)
        self.rotate_left(speed)
        target_dir = self.dir.apply_relative(RelativeDirection.Left)
        target_color = DirectionColorMap[target_dir][1]
        while not col_counter.triggered_by(BoardColor.Wood):
            col_counter(self.read_color())
        while not col_counter.triggered_by(target_color):
            col_counter(self.read_color())
        self.stop()
        self.dir = target_dir'''

    def turn_right(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        col_counter = ConsecutiveCounter(4)
        self.rotate_right(speed)
        target_dir = self.dir.apply_relative(RelativeDirection.Right)
        target_color = DirectionColorMap[target_dir][0]
        while not col_counter.triggered_by(BoardColor.Wood):
            col_counter(self.read_color())
        while not col_counter.triggered_by(target_color):
            col_counter(self.read_color())
        self.stop()
        self.dir = target_dir

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
        col_counter = ConsecutiveCounter(4)

        print("- Bande de couleur...")
        self.rotate_left(140)
        while not col_counter.triggered or \
                col_counter.value in (BoardColor.Unknown, BoardColor.Wood):
            color = self.read_color()
            col_counter(color)

        print("- Bois a droite...")
        self.rotate_right(60)
        while not col_counter.triggered_by(BoardColor.Wood):
            col_counter(self.read_color())

        print("- Detection 1ere bande... ", end='')
        col_counter = ConsecutiveCounter(9)
        self.rotate_left(60)
        color = self.read_color()
        while not col_counter.triggered or \
                col_counter.value in (BoardColor.Unknown, BoardColor.Wood):
            color = self.read_color()
            col_counter(color)
        first_color = color
        print(str(first_color))

        print("- Detection 2eme bande... ", end='')
        col_counter.reset()
        while True:
            color = self.read_color()
            col_counter(color)
            if col_counter.triggered and \
               color not in (first_color, BoardColor.Wood, BoardColor.Unknown):
                break
        self.stop()

        second_color = color
        print(str(second_color))

        direction = ColorDirectionMap[(second_color, first_color)]
        self.dir = direction

        print("Direction: " + str(direction))


class EV3Bot(RealBot):
    def __init__(self, *args, **kwargs):
        color_sensor = ColorSensor('in4')
        color_sensor.mode = 'COL-REFLECT'
        m_l = LargeMotor('outB')
        m_r = LargeMotor('outC')
        super(EV3Bot, self).__init__(
            m_l, m_r,
            color_sensor,
            *args, **kwargs)


@enum.unique
class RobotColor(enum.Enum):
    Red = 96
    Green = 97
    Blue = 135


def get_robot_calibration(color: RobotColor) -> BotCalibration:
    if color == RobotColor.Red:
        return BotCalibration(
            color=[
                ((0, 22), BoardColor.Black),
                ((50, 65), BoardColor.Wood),
                ((70, 90), BoardColor.Red),
                ((92, 100), BoardColor.White)
            ],
            pulses_per_cm=35.2
        )
    if color == RobotColor.Green:
        return BotCalibration(
            color=[
                ((0, 20), BoardColor.Black),
                ((40, 55), BoardColor.Wood),
                ((58, 75), BoardColor.Red),
                ((80, 100), BoardColor.White)
            ],
            pulses_per_cm=35.2
        )
    if color == RobotColor.Blue:
        return BotCalibration(
            color=[
                ((0, 20), BoardColor.Black),
                ((50, 65), BoardColor.Wood),
                ((70, 85), BoardColor.Red),
                ((90, 100), BoardColor.White)
            ],
            pulses_per_cm=35.2
        )
    raise ValueError


if __name__ == '__main__':
    '''
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
        '''

    calib = get_robot_calibration(RobotColor.Green)
    b = Board(8, 8)
    bot = EV3Bot(calib, board=b)

    try:
        bot.turn_left()
        while True:
            time.sleep(1)
        print("done")
        sys.exit(0)
        bot.find_direction()
        print('Found dir', bot.dir)
        print('Motor L', bot.motor_l.position, 'Motor R', bot.motor_r.position)
        bot.turn_right()
        print('Motor L', bot.motor_l.position, 'Motor R', bot.motor_r.position)
        print('After turn right', bot.dir)
        bot.forward(1)
        bot.turn_left()
        print('After turn left', bot.dir)
        bot.forward(1)
        #bot.forward_cm(30*2)
    except:
        bot.stop()
