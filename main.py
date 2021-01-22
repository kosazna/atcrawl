# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import sys
    from atcrawl.utilities import *
    import warnings

    warnings.filterwarnings('ignore')

    try:
        mode = str(sys.argv[1])
    except IndexError:
        mode = "GUI"

    if mode == 'CMD':
        log(f"atCrawl utilities\n")

        process = validate_input('action')

        if process == '1':
            from atcrawl.crawlers.antallaktika.runner import run

            run()
        elif process == '2':
            from atcrawl.crawlers.skroutz.runner import run

            run()
        else:
            pass
    else:
        from atcrawl.gui import *

        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()

        welcome_ui = WelcomeUI(main_window)
        main_window.show()
        sys.exit(app.exec_())
