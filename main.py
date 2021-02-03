# -*- coding: utf-8 -*-
from atcrawl.utilities import *
from atcrawl.crawlers.antallaktika.runner import antallaktika_run
from atcrawl.crawlers.skroutz.runner import skroutz_run
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    import sys

    try:
        mode = str(sys.argv[1])
    except IndexError:
        mode = "CMD"

    if mode == 'CMD':
        log(f"atCrawl utilities\n")

        process = validate_input('action')

        if process == '1':
            antallaktika_run()
        elif process == '2':
            skroutz_run()
        else:
            print("\nΔεν έχεις πρόσβαση σε αυτό το crawler.\n")
    else:
        from atcrawl.gui import *

        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()

        welcome_ui = WelcomeUI(main_window)
        main_window.show()
        sys.exit(app.exec_())
