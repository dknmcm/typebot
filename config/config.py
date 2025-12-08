BASE_WPM = 500.0

BASE_ERROR_RATE = 0.010
UNCORRECTED_ERROR_RATE = 0.008

WPM_VARIATION = 0.05

MIN_KEYSTROKE_DELAY = 0.0

MAX_THINKING_PAUSE = 0.2
THINKING_PAUSE_PROBABILITY = 0.01

SESSION_DURATION = 30.0
SESSION_START_DELAY = 1.0

# Sentence pause range (seconds)
SENTENCE_PAUSE_MIN = 0.0
SENTENCE_PAUSE_MAX = 0.05

# Word pause range (seconds)
WORD_PAUSE_MIN = 0.0
WORD_PAUSE_MAX = 0.03

# Correction delay range (seconds)
CORRECTION_DELAY_MIN = 0.0
CORRECTION_DELAY_MAX = 0.2

MAX_FATIGUE = 0.1

# Characters typed before maximum fatigue
FATIGUE_BUILDUP_CHARS = 200

# Chance of energy boost when fatigued (0.0 to 1.0)
ENERGY_BOOST_CHANCE = 0.4

# Increase error rate with fatigue
FATIGUE_ERROR_MULTIPLIER = 0.01

MIN_OCR_CONFIDENCE = 20.0

# Image preprocessing settings
OCR_IMAGE_SCALE_FACTOR = 3
OCR_CONTRAST_ENHANCEMENT = 2.0

# Screenshot capture interval (seconds)
SCREENSHOT_INTERVAL = 0.3

# Image change detection sensitivity
HASH_RESIZE_DIMENSIONS = (16, 16)

# Character pair timing adjustments (seconds)
CHAR_PAIR_ADJUSTMENTS = {
    'th': -0.02, 'er': -0.015, 'in': -0.015, 'an': -0.01,
    'qu': 0.03, 'xz': 0.05, 'qx': 0.06, 'tz': 0.04
}

# Common typo mappings (adjacent keys)
COMMON_TYPOS = {
    'a': ['s', 'q'], 's': ['a', 'd', 'w'], 'd': ['s', 'f'], 'f': ['d', 'g'],
    'g': ['f', 'h'], 'h': ['g', 'j'], 'j': ['h', 'k'], 'k': ['j', 'l'],
    'l': ['k', ';'], 'q': ['w'], 'w': ['q', 'e'], 'e': ['w', 'r'],
    'r': ['e', 't'], 't': ['r', 'y'], 'y': ['t', 'u'], 'u': ['y', 'i'],
    'i': ['u', 'o'], 'o': ['i', 'p'], 'p': ['o']
}
