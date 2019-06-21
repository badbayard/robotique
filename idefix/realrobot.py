#!/usr/bin/env python3
from idefix import *
from ev3dev.ev3 import *
import pkgutil
import json


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
    def __init__(self, color: BoardColorCalibration, pulses_per_cm: float,
                 pulses_per_90_degrees: float):
        self.color = color
        self.pulses_per_cm = pulses_per_cm
        self.pulses_per_90_degrees = pulses_per_90_degrees


class RealBot(Bot):
    DEFAULT_SPEED = 200
    CORRECT_SPEED = 40
    DEFAULT_ROTATE_SPEED = 100
    ROTATE_PULSES_SLOWDOWN = 50
    ROTATE_PULSES_SLOWDOWN_PER_STAY = 40
    CM_PER_CELL = 30

    def __init__(self, motor_l: LargeMotor, motor_r: LargeMotor,
                 color_sensor: ColorSensor,
                 calibration: BotCalibration,
                 *args, **kwargs):
        super(RealBot, self).__init__(*args, **kwargs)
        self.motor_l, self.motor_r = motor_l, motor_r
        self.color_sensor = color_sensor
        self.calibration = calibration
        self.rotate_stays = 0
        self.last_rotation_reldir = None

    def read_color(self) -> BoardColor:
        return BoardColor.from_itensity(
            self.color_sensor.reflected_light_intensity,
            self.calibration.color)

    def move_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.rotate_stays = 0
        end = self.motor_l.position + self.calibration.pulses_per_cm * cm
        # correct_dir = None
        # supercorrecting = False
        # supercorrecting_start =  None
        if self.last_rotation_reldir in (RelativeDirection.Left, None):
            self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
            self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
        else:
            self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
            self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
        while self.motor_l.position <= end:
            col = self.read_color()
            if col == DirectionColorMap[self.dir][1]:  # Correct left
                # if supercorrecting:
                #    supercorrecting = False
                #   end += self.motor_l.position - supercorrecting_start
                self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                #correct_dir = RelativeDirection.Left
            elif  col == DirectionColorMap[self.dir][0]:  # Correcy right
                # if supercorrecting:
                #    supercorrecting = False
                #    end += self.motor_l.position - supercorrecting_start
                self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                # correct_dir = RelativeDirection.Right
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
        pulses = kwargs.get("pulses", self.calibration.pulses_per_90_degrees)
        fast_pulses = pulses - min(
            pulses,
            self.ROTATE_PULSES_SLOWDOWN +
            self.ROTATE_PULSES_SLOWDOWN_PER_STAY * self.rotate_stays)
        print("FP: " + str(fast_pulses))
        self.motor_l.run_to_rel_pos(position_sp=-fast_pulses, speed_sp=-speed)
        self.motor_r.run_to_rel_pos(position_sp=fast_pulses, speed_sp=speed)
        self.motor_l.wait_until_not_moving()
        self.motor_r.wait_until_not_moving()

        col_counter = ConsecutiveCounter(4)
        self.rotate_left(speed / 2)
        target_dir = self.dir.apply_relative(RelativeDirection.Left)
        target_color = DirectionColorMap[target_dir][1]
        while not col_counter.triggered_by(target_color):
            col_counter(self.read_color())
        self.stop()
        self.dir = target_dir
        self.last_rotation_reldir = RelativeDirection.Left
        self.rotate_stays += 1

    def turn_right(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        pulses = kwargs.get("pulses", self.calibration.pulses_per_90_degrees)
        fast_pulses = pulses - min(
            pulses,
            self.ROTATE_PULSES_SLOWDOWN +
            self.ROTATE_PULSES_SLOWDOWN_PER_STAY * self.rotate_stays)
        print("FP: " + str(fast_pulses))
        self.motor_l.run_to_rel_pos(position_sp=fast_pulses, speed_sp=speed)
        self.motor_r.run_to_rel_pos(position_sp=-fast_pulses, speed_sp=-speed)
        self.motor_l.wait_until_not_moving()
        self.motor_r.wait_until_not_moving()

        col_counter = ConsecutiveCounter(4)
        self.rotate_right(speed / 2)
        target_dir = self.dir.apply_relative(RelativeDirection.Right)
        target_color = DirectionColorMap[target_dir][0]
        while not col_counter.triggered_by(target_color):
            col_counter(self.read_color())
        self.stop()
        self.dir = target_dir
        self.last_rotation_reldir = RelativeDirection.Right
        self.rotate_stays += 1

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


CALIBRATION_JSON_FILENAME = 'robots.json'
CALIBRATION_JSON = json.loads(pkgutil.get_data(
    __package__, CALIBRATION_JSON_FILENAME))


def get_robot_calibration(hostname: str) -> BotCalibration:
    for robot in CALIBRATION_JSON['robots']:
        if robot['match_hostname'] == hostname:
            cc = robot['sensor_colors']
            return BotCalibration(
                color=[
                    ((cc['Black'][0], cc['Black'][1]), BoardColor.Black),
                    ((cc['Wood'][0], cc['Wood'][1]), BoardColor.Wood),
                    ((cc['Red'][0], cc['Red'][1]), BoardColor.Red),
                    ((cc['White'][0], cc['White'][1]), BoardColor.White)
                ],
                pulses_per_cm=robot['pulses_per_cm'],
                pulses_per_90_degrees=robot['pulses_per_90_degrees']
            )
    raise KeyError("No calibration for hostname '{}'".format(hostname))


class EV3Bot(RealBot):
    def __init__(self, hostname, *args, **kwargs):
        color_sensor = ColorSensor('in4')
        color_sensor.mode = 'COL-REFLECT'
        m_l = LargeMotor('outB')
        m_r = LargeMotor('outC')
        name, color = None, None
        for robot in CALIBRATION_JSON['robots']:
            if robot['match_hostname'] == hostname:
                name = robot['name']
                color = robot['color']
        super(EV3Bot, self).__init__(
            m_l, m_r,
            color_sensor,
            *args,
            name=name,
            color=color,
            **kwargs)


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

    calib = get_robot_calibration('green')
    b = Board(8, 8)
    bot = EV3Bot(calib, board=b)

    try:
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
