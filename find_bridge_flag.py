from desmume.controls import Keys
from desmume.emulator import DeSmuME, DeSmuME_SDL_Window, SCREEN_HEIGHT, SCREEN_WIDTH


emu: DeSmuME = DeSmuME()
emu_memory = emu.memory

def from_boot_start_first_file(emu: DeSmuME, window: DeSmuME_SDL_Window, screenshot_name: str):
    for frame in range(1000):
        if frame % 100 == 0:
            print(frame)

        # title screen
        if frame == 350:
            emu.input.touch_set_pos(100, 100)
        elif frame == 351:
            emu.input.touch_release()
        elif frame == 400:
            emu.input.touch_set_pos(100, 100)
        elif frame == 401:
            emu.input.touch_release()

        # click file
        elif frame == 580:
            emu.input.touch_set_pos(100, 50)
        elif frame == 581:
            emu.input.touch_release()

        # click 'Start'
        elif frame == 625:
            emu.input.touch_set_pos(180, 170)
        elif frame == 626:
            emu.input.touch_release()

        # click 'Adventure'
        elif frame == 700:
            emu.input.touch_set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        elif frame == 701:
            emu.input.touch_release()

        elif frame == 950:
            emu.screenshot().save(f'screenshots/{screenshot_name}.png')

        emu.cycle()

        if window is not None:
            window.draw()

skip_addresses = [
    0x202d114,
]

addr_to_change = 0x21b3e71 

def to_bridge_from_mercay_town_cave(emu: DeSmuME, window: DeSmuME_SDL_Window, screenshot_name: str="testinggg.png"):
    for frame in range(550):
        
        global addr_to_change
        
        # set all the bits at the memory address we're interested in 
        emu_memory.unsigned[addr_to_change] = 0xff

        if frame % 100 == 0:
            print(frame, hex(addr_to_change))
        
        # touch bottom of screen to move link south of cave
        if frame == 0:
            emu.input.touch_set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT)

        elif frame == 100:
            emu.input.touch_release()

        # touch left side of screen to move link over to bridge screen
        elif frame == 101:
            emu.input.touch_set_pos(0, SCREEN_HEIGHT // 2)

        elif frame == 290:
            emu.input.touch_release()

        if frame == 410:
            emu.screenshot().save(f'screenshots_ram/{screenshot_name}.png')

        emu.cycle()

        if window is not None:
            window.draw()

def test_bridge(rom: str, screenshot_name: str):
    emu.open(rom)

    emu.input.keypad_rm_key(Keys.NB_KEYS)
    emu.input.keypad_rm_key(Keys.KEY_NONE)
    emu.input.keypad_rm_key(Keys.KEY_A)
    emu.input.keypad_rm_key(Keys.KEY_B)
    emu.input.keypad_rm_key(Keys.KEY_SELECT)
    emu.input.keypad_rm_key(Keys.KEY_START)
    emu.input.keypad_rm_key(Keys.KEY_RIGHT)
    emu.input.keypad_rm_key(Keys.KEY_LEFT)
    emu.input.keypad_rm_key(Keys.KEY_UP)
    emu.input.keypad_rm_key(Keys.KEY_DOWN)
    emu.input.keypad_rm_key(Keys.KEY_R)
    emu.input.keypad_rm_key(Keys.KEY_L)
    emu.input.keypad_rm_key(Keys.KEY_X)
    emu.input.keypad_rm_key(Keys.KEY_Y)
    emu.input.keypad_rm_key(Keys.KEY_DEBUG)
    emu.input.keypad_rm_key(Keys.KEY_BOOST)
    emu.input.keypad_rm_key(Keys.KEY_LID)
    emu.input.keypad_rm_key(Keys.NO_KEY_SET)
    
    window = None
    # uncomment this to actually render the desmume game window
    #    window: DeSmuME_SDL_Window = emu.create_sdl_window()
    

    # emu.savestate.load_file('outside.dst')
    from_boot_start_first_file(emu, window, screenshot_name)
    to_bridge_from_mercay_town_cave(emu, window, screenshot_name)

    global addr_to_change
    addr_to_change += 1

for i in range(0x21b3e71 , 0x21ba570):
    test_bridge('../ph_dpad.nds', f'test_{hex(i)}.png')
