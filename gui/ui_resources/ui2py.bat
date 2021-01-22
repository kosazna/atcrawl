@echo off

call conda activate dsc
call pyuic5 -x atcrawl_ui.ui -o ..\welcome_design.py
call pyuic5 -x atcrawl_crawler_ui.ui -o ..\crawler_design.py