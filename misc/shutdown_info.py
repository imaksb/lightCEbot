from misc.graphic import Graphic


def get_information_about_graphic(
        group: int,
        graphic: Graphic
):
    shutdown = graphic.get_next_shutdown(group)

    text_to_send = f"<b>Група:</b> {group}\n<b>Наступне відключення:</b> "
    if shutdown:
        text_to_send += f"{shutdown[0]}:00 - {shutdown[1]}:00"
    else:
        text_to_send += "<code>не очікується</code>"

    return text_to_send
