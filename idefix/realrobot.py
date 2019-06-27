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

    def triggered_by(self, value, count: int = 0):
        if not self.value == value:
            return False
        if count == 0:
            return self.count >= self.trigger
        return self.count >= count

    def print(self):
        print(('\n' if self.count == 1 else '') +
              '\r{} x {}'.format(self.value, self.count), end='')


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
    ROTATE_PULSES_SLOWDOWN = 150
    ROTATE_PULSES_SLOWDOWN_PER_STAY = 40
    ROTATE_SLOWDOWN_SPEED = 70
    CM_PER_CELL = 30
    DISTANCE_TO_WALL = 6;

    def __init__(self, motor_l: LargeMotor, motor_r: LargeMotor,
                 distance_l: Optional[UltrasonicSensor],
                 distance_f: Optional[UltrasonicSensor],
                 distance_r: Optional[UltrasonicSensor],
                 color_sensor: Optional[ColorSensor],
                 gyro: Optional[GyroSensor],
                 calibration: BotCalibration,
                 board: Board,
                 *args, **kwargs):
        super(RealBot, self).__init__(*args, **kwargs)
        self.motor_l, self.motor_r = motor_l, motor_r
        self.distance_l = distance_l
        self.distance_f = distance_f
        self.distance_r = distance_r
        self.color_sensor = color_sensor
        self.gyro = gyro
        self.calibration = calibration
        self.rotate_stays = 0
        self.last_rotation_reldir = None

    def read_color(self) -> BoardColor:
        return BoardColor.from_itensity(
            self.color_sensor.reflected_light_intensity,
            self.calibration.color)

    def move_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        if self.gyro is None:
            self.move_cm_color(cm, speed)
        else:
            self.move_cm_gyro(cm, speed)

    def move_cm_color(self, cm: float, speed: float):
        self.rotate_stays = 0
        end = self.motor_l.position + self.calibration.pulses_per_cm * cm
        correct_dir = None
        if self.last_rotation_reldir in (RelativeDirection.Left, None):
            self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
            self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
        else:
            self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
            self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
        col_counter = ConsecutiveCounter(25)
        while self.motor_l.position <= end:
            col = self.read_color()
            col_counter(col)
            col_counter.print()
            if col_counter.triggered_by(DirectionColorMap[self.dir][1], 3):
                # Correct left
                correct_dir = RelativeDirection.Left
                self.motor_l.run_forever(speed_sp=speed - self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed + self.CORRECT_SPEED)
            elif col_counter.triggered_by(DirectionColorMap[self.dir][0], 3):
                # Correct right
                correct_dir = RelativeDirection.Right
                self.motor_l.run_forever(speed_sp=speed + self.CORRECT_SPEED)
                self.motor_r.run_forever(speed_sp=speed - self.CORRECT_SPEED)
            elif correct_dir is not None and col_counter.triggered_by(
                    BoardColor.Wood):
                self.motor_l.stop()
                self.motor_r.stop()
                tmpPosition = self.motor_l.position
                if correct_dir == RelativeDirection.Left:
                    self.motor_l.run_forever(speed_sp=-self.CORRECT_SPEED)
                    self.motor_r.run_forever(speed_sp=self.CORRECT_SPEED)
                    while True:
                        col = self.read_color()
                        col_counter(col)
                        col_counter.print()
                        if col == DirectionColorMap[self.dir][1]:
                            break
                elif correct_dir == RelativeDirection.Right:
                    self.motor_l.run_forever(speed_sp=self.CORRECT_SPEED)
                    self.motor_r.run_forever(speed_sp=-self.CORRECT_SPEED)
                    while True:
                        col = self.read_color()
                        col_counter(col)
                        col_counter.print()
                        if col == DirectionColorMap[self.dir][0]:
                            break
					self.motor_l.position = tmpPosition - 100
        self.motor_l.stop()
        self.motor_r.stop()

    def move_cm_gyro(self, cm: float, speed: float):
        raise NotImplementedError

    def wait_movement(self):
        self.motor_l.wait_while('running')
        self.motor_r.wait_while('running')

    def forward_cm(self, cm: float, speed: float = DEFAULT_SPEED):
        self.move_cm(cm, speed)

    def forward(self, count: int = 1, speed: float = DEFAULT_SPEED,
                *args, **kwargs) -> None:
        self.forward_cm(count * self.CM_PER_CELL, speed)

    def turn_left(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        if self.gyro is None:
            self.turn_left_color(speed, *args, **kwargs)
        else:
            pass  # TODO

    def turn_left_color(self, speed: float, *args, **kwargs):
        pulses = kwargs.get("pulses", self.calibration.pulses_per_90_degrees)
        fast_pulses = pulses - min(
            pulses,
            self.ROTATE_PULSES_SLOWDOWN +
            self.ROTATE_PULSES_SLOWDOWN_PER_STAY * self.rotate_stays)
        print("FP: " + str(fast_pulses))
        self.motor_l.run_forever(speed_sp=-speed)
        self.motor_r.run_forever(speed_sp=speed)
        #self.motor_l.wait_until_not_moving()
        #self.motor_r.wait_until_not_moving()

        col_counter = ConsecutiveCounter(5)
        col_brown_counter = ConsecutiveCounter(15)
        while not col_brown_counter.triggered_by(BoardColor.Wood):
		    if self.read_color() == BoardColor.Wood : 
                col_brown_counter(self.read_color())

        self.rotate_left(self.ROTATE_SLOWDOWN_SPEED)
        target_dir = self.dir.apply_relative(RelativeDirection.Left)
        target_color = DirectionColorMap[target_dir][1]
        while not col_counter.triggered_by(target_color):
            col_counter(self.read_color())
        self.stop()
        self.dir = target_dir
        self.last_rotation_reldir = RelativeDirection.Left
        self.rotate_stays += 1

    def turn_right(self, speed: float = DEFAULT_ROTATE_SPEED, *args, **kwargs):
        if self.gyro is None:
            self.turn_right_color(speed, *args, **kwargs)
        else:
            pass  # TODO

    def turn_right_color(self, speed: float, *args, **kwargs):
        pulses = kwargs.get("pulses", self.calibration.pulses_per_90_degrees)
        fast_pulses = pulses - min(
            pulses,
            self.ROTATE_PULSES_SLOWDOWN +
            self.ROTATE_PULSES_SLOWDOWN_PER_STAY * self.rotate_stays)
        print("FP: " + str(fast_pulses))
        self.motor_l.run_forever(speed_sp=speed)
        self.motor_r.run_forever(speed_sp=-speed)
        #self.motor_l.wait_until_not_moving()
        #self.motor_r.wait_until_not_moving()

        col_counter = ConsecutiveCounter(5)
        col_brown_counter = ConsecutiveCounter(15)
        while not col_brown_counter.triggered_by(BoardColor.Wood):
            if self.read_color() == BoardColor.Wood : 
			    col_brown_counter(self.read_color())

        self.rotate_right(self.ROTATE_SLOWDOWN_SPEED)
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

    def wall(self, dist_max: float = DISTANCE_TO_WALL, dir: Union[Direction, RelativeDirection]) -> Wall:
        if isinstance(dir, Direction):
            dir = self.dir.get_relative(dir)
            self.distance_f = self.distance_f.value() / 10
            if self.distance_f <= dist_max:
                distance_l.mode = 'US-DIST-CM'
                distance_r.mode = 'US-DIST-CM'
                if dir == RelativeDirection.Left:
                    self.distance_l = self.distance_l.value()
                if dir == RelativeDirection.Right:
                    self.distance_r = self.distance_r.value()
                distance_l.mode = 'US-LISTEN'   #repasse en mode listen pour ne pas interfere
                distance_r.mode = 'US-LISTEN'


    def write_info(self, board: Board, *args, **kwargs):
        raise NotImplementedError


CALIBRATION_JSON_FILENAME = 'robots.json'
CALIBRATION_JSON = json.loads(pkgutil.get_data(
    __package__, CALIBRATION_JSON_FILENAME).decode('utf-8'))


def robot_json_entry(hostname: str):
    for entry in CALIBRATION_JSON['robots']:
        if entry['match_hostname'] == hostname:
            return entry
    raise KeyError("No robot '{}'".format(hostname))


def get_robot_calibration(hostname: str) -> BotCalibration:
    robot = robot_json_entry(hostname)
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


class EV3Bot(RealBot):
    def __init__(self, hostname, *args, **kwargs):
        robot = robot_json_entry(hostname)
        name = robot['name']
        color = robot['color']

        per = robot['peripherals']
        try:
            distance_l = UltrasonicSensor(per['distance_l'])
            distance_l.mode = 'US-DIST-CM'
        except KeyError:
            distance_l = None
        distance_f = UltrasonicSensor(per['distance_f'])
        distance_f.mode = 'US-DIST-CM'
        try:
            distance_r = UltrasonicSensor(per['distance_r'])
            distance_r.mode = 'US-DIST-CM'
        except KeyError:
            distance_r = None
        try:
            color_sensor = ColorSensor(per['color_sensor'])
            color_sensor.mode = 'COL-REFLECT'
        except KeyError:
            color_sensor = None
        try:
            gyro = GyroSensor(per['gyro'])
            gyro.mode = 'GYR-TILT'
        except KeyError:
            gyro = None
        motor_l = LargeMotor(per['motor_l'])
        motor_r = LargeMotor(per['motor_r'])
        super(EV3Bot, self).__init__(
            motor_l, motor_r,
            distance_l, distance_f, distance_r,
            color_sensor, gyro,
            get_robot_calibration(hostname),
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

    b = Board(8, 8)
    import platform
    bot = EV3Bot(platform.node(), board=b)

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
