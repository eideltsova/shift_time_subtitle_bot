from io import TextIOWrapper
from typing import Any, List, Callable
from dataclasses import dataclass
import re

MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60

class Timestamp:
    def __init__(self, hour: int, minute: int, second: int, millisecond: int):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02}:{self.second:02},{self.millisecond:03}"

    def __sub__(self, diff: int) -> "Timestamp":
        self.total_second = (self.hour * MINUTES_PER_HOUR + self.minute) * SECONDS_PER_MINUTE + self.second
        total_second = self.total_second - diff
        minute, second = divmod(total_second, SECONDS_PER_MINUTE)
        hours, minute = divmod(minute, MINUTES_PER_HOUR)
        return Timestamp(hours, minute, second, self.millisecond)

    def __add__(self, diff: int) -> "Timestamp":
        self.total_second = (self.hour * MINUTES_PER_HOUR + self.minute) * SECONDS_PER_MINUTE + self.second
        total_second = self.total_second + diff
        if total_second < 0:
            raise ValueError
        minute, second = divmod(total_second, SECONDS_PER_MINUTE)
        hours, minute = divmod(minute, MINUTES_PER_HOUR)
        return Timestamp(hours, minute, second, self.millisecond)

    def _build_timestamp(self) -> "Timespan":
        return f'{self.hour:02}:{self.minute:02}:{self.second:02},{self.millisecond}'


class Timespan:
    def __init__(self, start_time: Timestamp, end_time: Timestamp):
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self) -> str:
        return f"{self.start_time} --> {self.end_time}"

    def __add__(self, time_delta: int) -> "Timespan":
        return Timespan(self.start_time + time_delta, self.end_time + time_delta)

    def __sub__(self, time_delta: int) -> "Timespan":
        return Timespan(self.start_time - time_delta, self.end_time - time_delta)

class Block:
    """"""

    def __init__(self, block: list):
        self.number = int(block[0].strip())
        self.timespan = self._extract_timespan(block[1])
        self.content = block[2:]

    def __str__(self) -> str:
        content = '\n'.join(self.content)
        return f"{self.number}\n{self.timespan}\n{content}"

    def _extract_timespan(self, timing_line: str) -> Timespan:
        match = re.match(r'^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', timing_line)
        start_timing, end_timing = match.group(1), match.group(2)

        start_hour, start_minute, fractional_second = start_timing.split(':')
        start_second, start_millisecond = fractional_second.split(',')
        start_timestamp = Timestamp(int(start_hour), int(start_minute), int(start_second), int(start_millisecond))

        end_hour, end_minute, fractional_second = end_timing.split(':')
        end_second, end_millisecond = fractional_second.split(',')
        end_timestamp = Timestamp(int(end_hour), int(end_minute), int(end_second), int(end_millisecond))

        return Timespan(start_timestamp, end_timestamp)

    def _check_number(self, number_line):
        if number_line < 0:
            raise ValueError('Number shouldn\'t be negative')
        return number_line


