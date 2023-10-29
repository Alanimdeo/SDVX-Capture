from ctypes import windll
from io import BytesIO
import keyboard
from PIL import ImageGrab, Image
from win10toast import ToastNotifier
import win32clipboard
import win32gui


class Capture:
    toast = ToastNotifier()
    capturing = False
    release_hook = None

    def screenshot(self):
        try:
            current_window = win32gui.GetForegroundWindow()

            sdvx = win32gui.FindWindow(None, r'SOUND VOLTEX EXCEED GEAR')
            if current_window != sdvx:
                return 2

            dimensions = win32gui.GetWindowRect(sdvx)

            image = ImageGrab.grab(dimensions)
            image = image.transpose(Image.ROTATE_270)

            output = BytesIO()
            image.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            return 0
        except Exception as e:
            print(e)
            return 1

    def capture(self):
        if self.capturing:
            return
        self.capturing = True
        self.release_hook = keyboard.on_release_key('f12', self.release)

        self.screenshot()

    def release(self, *_):
        self.capturing = False
        if self.release_hook is not None:
            keyboard.unhook_key(self.release_hook)

    def __init__(self):
        keyboard.add_hotkey('ctrl+f12', self.capture)
        self.toast.show_toast('SDVXCapture is running',
                              'Press Ctrl + F12 to capture\r\nPress Ctrl + Alt + F11 to quit')
        keyboard.wait('ctrl+alt+f11')
        keyboard.remove_hotkey('ctrl+f12')
        self.toast.show_toast('SDVXCapture is stopped', 'Goodbye!')
        exit()


if __name__ == '__main__':
    user32 = windll.user32
    user32.SetProcessDPIAware()
    Capture()
