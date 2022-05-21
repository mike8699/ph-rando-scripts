from pprint import pprint
from ndspy.rom import NintendoDSRom
from ndspy.narc import NARC
from ndspy.fnt import Folder
from ndspy import lz10
from zed.zmb import ZMB
from zed.common import Game

from patcher.items import ITEMS


def search_zmb(rompath: str, item_ids: list[int | str]):
    """
    Find a ZMB that contains the given items.

    Params:
        rompath: path to the ROM
        item_ids: list of item ids to search ZMBs for
    """
    for i, item_id in enumerate(item_ids):
        if isinstance(item_id, str):
            item_ids[i] = ITEMS[item_id]

    rom = NintendoDSRom.fromFile(rompath)
    locations = []
    for folder in rom.filenames.subfolder('Map').folders:
        folder_name = folder[0]
        file_path = f'Map/{folder_name}'
        for subfolder in folder:
            if isinstance(subfolder, Folder):
                for file in subfolder.files:
                    if not file.startswith('map'):
                        continue
                    narc_path = f'{file_path}/{file}'
                    narc_file = NARC(lz10.decompress(rom.getFileByName(narc_path)))
                    map_number = file[3:5]
                    zmb_filename = f'zmb/{folder_name}_{map_number}.zmb'
                    try:
                        zmb_file = ZMB(Game.PhantomHourglass, narc_file.getFileByName(f'zmb/{folder_name}_{map_number}.zmb'))
                        searching_for = [item for item in item_ids]  # deep clone the original list
                        for i, map_obj in enumerate(zmb_file.mapObjects):
                            if map_obj.unk08 in searching_for:
                                searching_for.pop(searching_for.index(map_obj.unk08))
                        if len(searching_for) == 0:
                            locations.append(f'{narc_path}/{zmb_filename}')
                    except:
                        # Some ZMB files fail for unknown reasons, just ignore them
                        continue
    return locations


locations = search_zmb('in_dpad.nds', ["small_key", "small_key", "small_red_rupee"])
pprint(locations)
