from aiogram.utils.keyboard import InlineKeyboardBuilder


async def queue_action_choice():
    builder = InlineKeyboardBuilder()

    builder.button(text="Check Queue", callback_data="show:queue")
    builder.button(text="Take a Place", callback_data="show:time_selector")

    builder.adjust(2)

    return builder.as_markup()


async def time_start_selector_buttons(next_time_available: str):
    builder = InlineKeyboardBuilder()
    if next_time_available != "24:00":
        start_time = int(next_time_available.split(":")[0])

        for time in range(start_time, 24):
            builder.button(text=f"{time}:00", callback_data=f"select:time_start:{time}")

        builder.adjust(4)

    else:
        builder.button(text="Everything is full", callback_data="cancel:time_selection")
        builder.adjust(1)

    return builder.as_markup()


async def time_finish_selector_buttons(start_time_selected: str):
    builder = InlineKeyboardBuilder()

    start_time = int(start_time_selected.split(":")[0]) - 1

    for time in range(start_time + 1, 25):
        builder.button(text=f"{time}:00", callback_data=f"select:time_finish:{start_time}_00-{time}_00")

    builder.adjust(4)

    return builder.as_markup()


async def time_selection_submit_btn(time_start: str, time_finish: str):
    builder = InlineKeyboardBuilder()

    builder.button(text="Cancel", callback_data="cancel:time_selection")
    builder.button(text="Submit", callback_data=f"submit:time_selection:{time_start}_00-{time_finish}_00")

    builder.adjust(2)

    return builder.as_markup()


async def my_time_menu_btn():
    builder = InlineKeyboardBuilder()

    builder.button(text="Close", callback_data="finish:time:close")
    builder.button(text="Finish Earlier", callback_data="finish:time:agree")
    builder.adjust(2)

    return builder.as_markup()


async def my_time_menu_delete_accept():
    builder = InlineKeyboardBuilder()

    builder.button(text="Cancel", callback_data="finish:time:cancel_t")
    builder.button(text="Delete", callback_data="finish:time:delete")

    builder.adjust(2)
    return builder.as_markup()
