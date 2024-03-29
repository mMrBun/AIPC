import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os


# 修改系统壁纸
def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


# 修改系统音量 ，浮点0-1代表0-100%
def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume.iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)


# 修改系统亮度 ，浮点0-1代表0-100%
def set_brightness(brightness_level):
    brightness_level = int(brightness_level * 255)
    brightness = ctypes.c_ulong(brightness_level)
    ctypes.windll.kernel32.SetLastError(0)
    result = ctypes.windll.powrprof.PowerWriteACValueIndex(None, ctypes.c_wchar_p('SCHEME_CURRENT'),
                                                           ctypes.c_wchar_p('SUB_VIDEO'),
                                                           ctypes.c_wchar_p('Brightness'), brightness)
    error_code = ctypes.windll.kernel32.GetLastError()
    return result != 0, error_code


# 修改系统主题
def set_theme(theme_file_path):
    theme_directory = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Themes')

    current_theme_path = os.path.join(theme_directory, 'current.theme')

    new_theme_path = os.path.abspath(theme_file_path)

    with open(current_theme_path, 'w') as current_theme:
        current_theme.write('[Theme]\n')
        current_theme.write('DisplayName=New Theme\n')
        current_theme.write('ThemeName=New Theme\n')
        current_theme.write('ThemeUrl=file:///' + new_theme_path.replace('\\', '/') + '\n')


if __name__ == '__main__':
    set_wallpaper("path_to_your_image.jpg")
    set_volume(0.06)
    set_brightness(1)
    set_theme('path_to_your_theme_file.theme')

# pip install comtypes
# pip install pycaw
