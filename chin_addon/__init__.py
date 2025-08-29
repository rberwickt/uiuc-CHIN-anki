#C:/Users/rtber/AppData/Roaming/Anki2/addons21

#basic guide https://addon-docs.ankiweb.net/a-basic-addon.html

# import dependencies
import sys
import os

addon_dir = os.path.dirname(__file__)
libs_path = os.path.join(addon_dir, "libs")
sys.path.insert(0, libs_path)

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# importing Chinese utils
from xpinyin import Pinyin
import opencc
conv_s = opencc.OpenCC('s2t') # s2t.json is simplified to trad.
conv_t = opencc.OpenCC('t2s') # t2s.json is trad. to simplified
p = Pinyin()


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    main_col = mw.col
    

    note_ids = main_col.find_notes('deck:"CHIN"')
    changed_num = 0
    for i in range(len(note_ids)):
        note = main_col.get_note(note_ids[i])
        data = note.fields # get each note
        changed = False
        """
        0 - simp. 
        1 - trad.
        2 - pinyin
        3 - def
        4 - ex. (chin)
        5 - ex. (pinyin)
        6 - ex. (eng.)
        """
        changed = False
        hasSimp = data[0] != ""
        hasTrad = data[1] != ""
        hasPinyin = data[2] != ""
        if not hasSimp and hasTrad:
            data[0] = conv_t.convert(data[1])
            changed = True
        if not hasTrad and hasSimp:
            data[1] = conv_s.convert(data[0])
            changed = True
        if not hasPinyin:
            if hasSimp:
                data[2] = p.get_pinyin(data[0], tone_marks="marks",splitter=" ")
                changed = True
            elif hasTrad:
                data[2] = p.get_pinyin(data[1], tone_marks="marks",splitter=" ")
                changed = True
        if changed:
            changed_num += 1
            note.flush()
        

    # show a message box
    mw.reset()
    showInfo(f"Changed {changed_num} notes")

# create a new menu item, "test"
action = QAction("Fill in CHIN", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

"""
{'id': 1714724553312, 
'mod': 1755826709, 
'name': 'CHIN', 
'usn': 0, 
'lrnToday': [1812, 0], 
'revToday': [1812, 20], 
'newToday': [1812, 2], 
'timeToday': [1812, 160401], 
'collapsed': False, 
'browserCollapsed': False, 
'desc': '', 
'dyn': 0, 
'conf': 1, 
'extendNew': 0, 
'extendRev': 0, 
'reviewLimit': None, 
'newLimit': None, 
'reviewLimitToday': None, 
'newLimitToday': None}
"""
