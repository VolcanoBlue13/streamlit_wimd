import numpy as np
import altair as alt

def highlight_min(s):
    if s.dtype == np.object:
        is_min = [False for _ in range(s.shape[0])]
    else:
        is_min = s == s.min()

    return ["background: powderblue" if cell else "" for cell in is_min]

FONT = "Averta"
TITLE_FONT = "Averta"
FONTSIZE_TITLE = 16
FONTSIZE_SUBTITLE = 13
FONTSIZE_NORMAL = 13

NESTA_COLOURS = [
    "lightgrey",
    "#0000FF",
    "#18A48C",
    "#9A1BBE",
    "#EB003B",
    "#FF6E47",
    "#646363",
    "#0F294A",
    "#97D9E3",
    "#A59BEE",
    "#F6A4B7",
    "#FDB633",
    "#D2C9C0",
    "#FFFFFF",
    "#000000",
]

LSOA_IN_EXTREME_10 = ['W01000028',
 'W01000041',
 'W01000048',
 'W01000050',
 'W01000051',
 'W01000057',
 'W01000086',
 'W01000096',
 'W01000112',
 'W01000138',
 'W01000167',
 'W01000176',
 'W01000189',
 'W01000194',
 'W01000228',
 'W01000328',
 'W01000360',
 'W01000362',
 'W01000379',
 'W01000381',
 'W01000409',
 'W01000427',
 'W01000510',
 'W01000531',
 'W01000537',
 'W01000539',
 'W01000541',
 'W01000542',
 'W01000550',
 'W01000589',
 'W01000603',
 'W01000626',
 'W01000646',
 'W01000685',
 'W01000725',
 'W01000744',
 'W01000746',
 'W01000809',
 'W01000830',
 'W01000834',
 'W01000851',
 'W01000856',
 'W01000867',
 'W01000886',
 'W01000898',
 'W01000901',
 'W01000914',
 'W01000920',
 'W01000921',
 'W01000922',
 'W01000924',
 'W01000930',
 'W01000942',
 'W01000950',
 'W01000958',
 'W01000965',
 'W01000967',
 'W01000971',
 'W01000976',
 'W01000993',
 'W01001004',
 'W01001022',
 'W01001045',
 'W01001046',
 'W01001071',
 'W01001183',
 'W01001201',
 'W01001205',
 'W01001206',
 'W01001211',
 'W01001215',
 'W01001229',
 'W01001274',
 'W01001275',
 'W01001276',
 'W01001287',
 'W01001307',
 'W01001329',
 'W01001386',
 'W01001410',
 'W01001451',
 'W01001457',
 'W01001462',
 'W01001483',
 'W01001487',
 'W01001506',
 'W01001519',
 'W01001605',
 'W01001645',
 'W01001693',
 'W01001695',
 'W01001696',
 'W01001697',
 'W01001718',
 'W01001721',
 'W01001837',
 'W01001866',
 'W01001922',
 'W01001924',
 'W01001939',
 'W01001943',
 'W01001945',
 'W01001952']

def nestafont():
    """Define Nesta fonts"""
    return {
        "config": {
            "title": {"font": TITLE_FONT, "anchor": "start"},
            "axis": {"labelFont": FONT, "titleFont": FONT},
            "header": {"labelFont": FONT, "titleFont": FONT},
            "legend": {"labelFont": FONT, "titleFont": FONT},
            "range": {
                "category": NESTA_COLOURS,
                "ordinal": {
                    "scheme": NESTA_COLOURS
                },  # this will interpolate the colors
            },
        }
    }