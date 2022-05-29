import click
from pathlib import Path
from oop.block import *

MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60


def get_source_and_target_file_streams(source_file_name: str, time_delta: int) -> tuple[TextIOWrapper, TextIOWrapper]:
    """Function returns file streams for original file (read mode) and for newly created file (write mode)"""
    name = Path(source_file_name).stem
    ext = Path(source_file_name).suffix
    src = Path(source_file_name).parent
    target_file_name = f'{src}/{name}_changed_{time_delta}{ext}'
    source_file_stream = open(source_file_name, 'r')
    target_file_stream = open(target_file_name, 'w+')
    print(f'Новый файл создан: {target_file_name}')
    return source_file_stream, target_file_stream


def fetch_subtitles_blocks(source_file_stream: TextIOWrapper) -> list[Block]:
    blocks = []
    for line in source_file_stream:
        if line != '\n':
            blocks.append(line)
        else:
            block = Block(blocks)
            yield block
            blocks = []


def create_target_file_content(source_file_stream: TextIOWrapper, target_file_stream: TextIOWrapper,
                               time_delta: int) -> None:
    """Function creates target file content (with modified timings) based on source file content"""
    for block in fetch_subtitles_blocks(source_file_stream):
        try:
            new_timing_line = block.timespan + time_delta
            target_file_stream.write(str(block.number))
            target_file_stream.write('\n')
            target_file_stream.write(str(new_timing_line))
            target_file_stream.write('\n')
            target_file_stream.write(''.join(block.content))
            target_file_stream.write('\n')
        except ValueError:
            continue
    source_file_stream.close()
    target_file_stream.close()
    return target_file_stream.name


def shift_time_subtitle(src_file: str, time_delta: int):
    try:
        source_file, target_file = get_source_and_target_file_streams(src_file, int(time_delta))
        new_file = create_target_file_content(source_file, target_file, time_delta)
        return new_file
    except FileNotFoundError:
        print(f'Проверьте существование файла: {src_file}')
        source_file_name = click.prompt('Введите имя исходного файла', type=str)


