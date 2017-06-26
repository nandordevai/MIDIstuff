

# author : mots@motscousus.com



# real life MIDI channels 1-16 are mapped to 0-15 in live python scripts
ALL_CHANNELS        = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

#shortcut used not to assign something.
NA=-1

######################################################################
#
# MAP REAL LIFE NOTE NUMBER AND CCS TO MORE HUMAN READABLE THINGS
#
# IF YOUR NOTE NUMBER ON YOUR MPD16 
# ARE NOT THE DEFAULT ONES CHANGE THEM BELOW
#
######################################################################

# PAD TO NOTE_NO MAPPINGS
# this are the default MPD16 note_no and cc

# BANK A
PAD_A_1     = 37
PAD_A_2     = 36
PAD_A_3     = 42
PAD_A_4     = 82
PAD_A_5     = 40
PAD_A_6     = 38
PAD_A_7     = 46
PAD_A_8     = 44
PAD_A_9     = 48
PAD_A_10    = 47
PAD_A_11    = 45
PAD_A_12    = 43
PAD_A_13    = 49
PAD_A_14    = 55
PAD_A_15    = 51
PAD_A_16    = 53

# BANK B
PAD_B_1     = 54
PAD_B_2     = 69
PAD_B_3     = 81
PAD_B_4     = 80
PAD_B_5     = 65
PAD_B_6     = 66
PAD_B_7     = 76
PAD_B_8     = 77
PAD_B_9     = 56
PAD_B_10    = 62
PAD_B_11    = 63
PAD_B_12    = 64
PAD_B_13    = 73
PAD_B_14    = 74
PAD_B_15    = 71
PAD_B_16    = 39

# SLIDER MAPPING
SLIDER_CC   = 7


######################################################################
#
# MAP OUR HUMAN READABLES NAMES TO FUNCTIONS
#
# i use bank B on all channels to control track and scene and
# record new clip
#
# i use bank B on channel 16 to launch clip on the current scene
# and switch between scenes
#
# bank A on other channels than 16 for classic live midi learn 
# mapping
#
# this can be changed by altering XXXX_FUNCTIONS_CHANNELS
#
######################################################################

# SONG MANIPULATION
FIRE_SCENE          = PAD_B_4
SCENE_DOWN          = PAD_B_8
SCENE_UP            = PAD_B_12
TRACK_LEFT          = PAD_B_15
TRACK_RIGHT         = PAD_B_16

MAIN_FUNCTIONS_NOTES        = [TRACK_LEFT,TRACK_RIGHT, SCENE_DOWN,SCENE_UP, FIRE_SCENE]
#set on what channel these function should be active
MAIN_FUNCTIONS_CHANNELS	    = ALL_CHANNELS


# SELECTED TRACK MANIPULATION
TRACK_VOL_CC        = SLIDER_CC
TRACK_TOGGLE_MUTE   = PAD_B_10
TRACK_TOGGLE_SOLO   = PAD_B_6
TRACK_TOGGLE_ARM    = PAD_B_14
TRACK_ARM           = NA
TRACK_UNARM         = NA
TRACK_VOL_DEC       = NA
TRACK_VOL_INC       = NA

TRACK_FUNCTIONS_NOTES	    = [TRACK_TOGGLE_ARM,TRACK_TOGGLE_MUTE,TRACK_TOGGLE_SOLO]
#set on what channel these function should be active
TRACK_FUNCTIONS_CHANNELS    = ALL_CHANNELS


# SELECTED CLIP MANIPULATION
TOGGLE_CLIP         = PAD_B_13
RECORD_EMPTY_CLIP   = PAD_B_9
RECORD_CLIP			= NA
REMOVE_CLIP         = NA

CLIP_FUNCTIONS_NOTES	    = [TOGGLE_CLIP, RECORD_EMPTY_CLIP]
#set on what channel these function should be active
CLIP_FUNCTIONS_CHANNELS     = ALL_CHANNELS


# CLIP TRIGGERS AND SCENE SELECTION
SCENE_DOWN_BIS      = PAD_A_3
SCENE_UP_BIS        = PAD_A_2
FIRE_SCENE_BIS      = PAD_A_4
TRG_CLIP_1          = PAD_A_13
TRG_CLIP_2          = PAD_A_14
TRG_CLIP_3          = PAD_A_15
TRG_CLIP_4          = PAD_A_16
TRG_CLIP_5          = PAD_A_9
TRG_CLIP_6          = PAD_A_10
TRG_CLIP_7          = PAD_A_11
TRG_CLIP_8          = PAD_A_12
TRG_CLIP_9          = PAD_A_5
TRG_CLIP_10         = PAD_A_6
TRG_CLIP_11         = PAD_A_7
TRG_CLIP_12         = PAD_A_8

CLIP_TRIGGERS_NAV_NOTES     = [SCENE_DOWN_BIS,SCENE_UP_BIS,FIRE_SCENE_BIS]
CLIP_TRIGGERS_NOTES	        = [TRG_CLIP_1,TRG_CLIP_2,TRG_CLIP_3,TRG_CLIP_4,TRG_CLIP_5,TRG_CLIP_6,TRG_CLIP_7,TRG_CLIP_8,TRG_CLIP_9,TRG_CLIP_10,TRG_CLIP_11,TRG_CLIP_12]
#set on what channel these function should be active, i use channel 16
#  the "-1" is here to map reallife midichannels [1-16]
#  to midi channels seen from a programming point [0-15]
#  you can put more than one channels separated by commas
CLIP_TRIGGERS_CHANNELS	    = [16 -1]


######################################################################
#
# USEFULL CONSTANTS
#
######################################################################


# MIDI STUFF

STATUS_MASK     = 0xF0
CHAN_MASK       = 0x0F

CC_STATUS	    = 0xb0
NOTEON_STATUS   = 0x90
NOTEOFF_STATUS  = 0x80

STATUS_ON       = 0x7f
STATUS_OFF      = 0x00
STATUS_OFF2     = 0x40
