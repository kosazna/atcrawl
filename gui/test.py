# from ctypes import windll

# def get_ppi():
#     LOGPIXELSX = 88
#     LOGPIXELSY = 90
#     user32 = windll.user32
#     user32.SetProcessDPIAware()
#     dc = user32.GetDC(0)
#     pix_per_inch = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
#     user32.ReleaseDC(0, dc)
#     return pix_per_inch

# print(get_ppi())


def get_dpi():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    app.quit()

    return int(dpi)


print(get_dpi())
