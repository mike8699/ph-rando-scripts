#!/usr/bin/env python

from pathlib import Path
import sys
from typing import List

from ndspy import fnt, lz10, narc, rom

def extract_narc_subfolder_to_directory(narc_file: narc.NARC, folder: fnt.Folder, output_directory: Path):
    for file in folder.files:
        # Chop off the first directory (the user-provided output dir) + the path to the NARC file inside
        # the ROM to get the current working directory inside the current NARC file system:
        file_path = str(
            (output_directory / file)
                .relative_to(
                    '/'.join(str(output_directory.as_posix()).split('/')[:4])
                ).as_posix()
            )
        
        print(f'  extracting "{file_path}"... ', end='')
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        with open(output_directory / file, 'wb') as fd:
            fd.write(narc_file.getFileByName(file_path))
        print('done.')

    for subfolder_obj in folder.folders:
        subfolder_name, subfolder = subfolder_obj
        extract_narc_subfolder_to_directory(narc_file, subfolder, output_directory / subfolder_name)


def main(argv: List[str]):
    if len(argv) < 3:
        print('Usage: python ph_map_extract.py [location of .nds rom] [location to extract Map files to]', file=sys.stderr)
        exit(1)

    rom_path = Path(argv[1])

    narc_directory = Path(argv[2])

    ph_rom = rom.NintendoDSRom.fromFile(rom_path)

    map_folder: fnt.Folder = ph_rom.filenames.subfolder('Map')
    
    folder_obj: fnt.Folder
    for folder_obj in map_folder.folders:
        folder: fnt.Folder
        folder_name, folder = folder_obj

        file: str
        for file in folder.files:
            if not file.startswith('map'):
                continue

            file_path = f'Map/{folder_name}/{file}'

            narc_file = narc.NARC(lz10.decompress(ph_rom.getFileByName(file_path)))

            print(f'Entering "{file_path}"....')

            extract_narc_subfolder_to_directory(narc_file, narc_file.filenames, narc_directory / file_path)

if __name__ == '__main__':
    main(sys.argv)
