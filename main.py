# -*- coding: utf-8 -*-
import warnings

from atcrawl.cli import *
from atcrawl.crawlers.antallaktika.cli import antallaktika_run
from atcrawl.crawlers.skroutz.cli import skroutz_run
from atcrawl.utilities import *

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    import sys

    try:
        mode = str(sys.argv[1])
    except IndexError:
        mode = "GUI"

    if mode == 'CLI':
        log(f"atCrawl utilities\n")

        process = validate_input('action')

        if process == '1':
            antallaktika_run()
        elif process == '2':
            skroutz_run()
        elif process == '6':
            merge_run()
        elif process == '7':
            filter_run()
        elif process == '8':
            sort_run()
        elif process == '9':
            download_images_run()
        elif process == '10':
            create_images_run()
        elif process == '11':
            split_file_run()
        else:
            print("\nΔεν έχεις πρόσβαση σε αυτή τη λειτουργία\n")
    else:
        from atcrawl.gui import *
        import ctypes
        myappid = 'com.aztool.atcrawl.app'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QIcon('atcrawl_app.ico'))
        main_window = QtWidgets.QMainWindow()

        welcome_ui = WelcomeUI(main_window)
        main_window.show()
        sys.exit(app.exec_())
