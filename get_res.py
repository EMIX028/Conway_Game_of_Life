import ctypes

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),
        ("dmPositionX", ctypes.c_long),
        ("dmPositionY", ctypes.c_long),
        ("dmDisplayOrientation", ctypes.c_ulong),
        ("dmDisplayFixedOutput", ctypes.c_ulong),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong)
    ]

def gcd(a, b):
    # PGCD
    while b:
        a, b = b, a % b
    return a

def get_screen_ratio():
    """ Récup la resolution de l'écran"""
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    div = gcd(screen_width, screen_height)
    return (screen_width // div, screen_height // div)

def get_supported_resolutions(filter_ratio=True):
    """ renvoie une liste de tuple de toute les résolutions supporté"""
    user32 = ctypes.windll.user32
    i = 0
    resolutions = set()

    target_ratio = get_screen_ratio() if filter_ratio else None

    while True:
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(DEVMODE)
        if not user32.EnumDisplaySettingsW(None, i, ctypes.byref(devmode)):
            break
        width, height = devmode.dmPelsWidth, devmode.dmPelsHeight
        if width > 0 and height > 0:
            if filter_ratio:
                div = gcd(width, height)
                res_ratio = (width // div, height // div)
                if res_ratio == target_ratio:
                    resolutions.add((width, height))
            else:
                resolutions.add((width, height))
        i += 1

    sorted_resolutions = sorted(resolutions, key=lambda x: (x[0], x[1]))
    return sorted_resolutions
