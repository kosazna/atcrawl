# -*- coding: utf-8 -*-

from typing import Union, List
from bs4 import BeautifulSoup


def parse(soup: BeautifulSoup,
          element_tag: str,
          element_class: str,
          text: bool = True) -> Union[str, BeautifulSoup, None]:
    """
    Parse html code and returns the specified object or text.


    :param soup: BeautifulSoup
        BeautifulSoup object
    :param element_tag: str
        HTML tag of element
    :param element_class: str
        HTML class of element
    :param text: bool
        Whether to return the text or the BeautifulSoup object if found.
        (default: True)
    :return: str or BeautifulSoup or None
        If nothing is found None is returned.
    """
    try:
        content = soup.find(element_tag, {'class': element_class})
    except KeyError:
        content = None

    if content:
        return content.text if text else content
    return None


def multi_parse(soup: BeautifulSoup,
                element_tag: str,
                element_class: str,
                text: bool = True) -> Union[List[str],
                                            List[BeautifulSoup],
                                            None]:
    """
    Parse html code and returns the specified object or text.

    :param soup: BeautifulSoup
        BeautifulSoup object
    :param element_tag: str
        HTML tag of element
    :param element_class: str
        HTML class of element
    :param text: bool
        Whether to return the text or the BeautifulSoup object if found.
        (default: True)
    :return: list
        List of str if text=True.
        List of BeatufulSoup objects if text=False
        Empty list if nothing is found
    """
    try:
        content = soup.find_all(element_tag, {'class': element_class})
    except KeyError:
        content = None

    if content:
        return [i.text for i in content] if text else content
    return list()
