def get_upper_parentwidget(widget, parent_position: int):
    """This function replaces this:
          self.parentWidget().parentWidget().parentWidget()
       with this:
          get_upper_parentwidget(self, 3)

    :param widget: QWidget
    :param parent_position: Which parent
    :return: Wanted parent widget
    """
    while parent_position > 0:
        widget = widget.parentWidget()
        parent_position -= 1
    else:
        return widget


def format_duration(duration: float):
    """Formats the duration (milliseconds) to a human readable way.

    :param duration: Duration in milliseconds
    :return: Duration in HOURS:MINUTES:SECONDS format. Example: 01:05:10
    """
    m, s = divmod(duration / 1000, 60)
    h, m = divmod(m, 60)
    if h:
        return "{0}:{1:0>2}:{2:0>2}".format(str(int(h)).zfill(2),
                                            str(int(m)).zfill(2), str(int(s)).zfill(2))
    else:
        return "{0}:{1:0>2}".format(str(int(m)).zfill(2), str(int(s)).zfill(2))


def check_keys(key_list: list, wanted_key_list: list):
    """Checks if the key list has every wanted key pressed (not in order).

    :param key_list: List of keys pressed.
    :param wanted_key_list: List of keys that needs to be pressed.
    :return: Returns whether the list of keys matches the wanted list.
    """
    valid_key_count = 0
    for wanted_key in wanted_key_list:
        if any(wanted_key == key for key in key_list):
            valid_key_count += 1

    return valid_key_count == len(wanted_key_list)
