import re
from decimal import (
    Decimal,
    ROUND_DOWN,
    InvalidOperation,
)

from db import (
    add_metric as add_metric_db,
    get_user_metrics as get_user_metrics_db,
    add_stat as add_stat_db,
    get_metric_name as get_metric_name_db,
)
from report import generate_report
from utils import (
    ValidationError,
    _convert_buttons_to_reply_markup,
)

ADDING_METRIC_KEY = 'adding_metric'
METRIC_UUID_KEY = 'metric_uuid'


def reset_user_data(context):
    context.user_data.clear()


async def request_metric(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Please enter the name of the metric you want to add "
            "(up to 20 symbols):"
        ),
    )
    context.user_data[ADDING_METRIC_KEY] = True


async def add_metric(update, context):
    chat_id = update.effective_user.id
    name = update.effective_message.text[:20]

    try:
        add_metric_db(chat_id, name)
    except ValidationError as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=e.message,
        )
        return
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Metric {name} added successfully",
        )
        reset_user_data(context)


async def request_stat(update, context):
    chat_id = update.effective_user.id
    metrics = get_user_metrics_db(chat_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Select metric:',
        reply_markup=_convert_buttons_to_reply_markup([
            [
                (metric[1], f'add_stat_{metric[0]}')
                for metric in metrics
            ],
        ]),
    )
    reset_user_data(context)


async def request_stat_value(update, context):
    metric_uuid = update.callback_query.data.replace('add_stat_', '')
    reset_user_data(context)
    context.user_data[METRIC_UUID_KEY] = metric_uuid
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Enter a value:",
    )


async def add_stat(update, context):
    metric_uuid = context.user_data[METRIC_UUID_KEY]
    value = update.effective_message.text

    if re.match(r"^-?\d{1,7}(\.\d{2})?$", value) is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter a number from -9 999 999.99 to 9 999 999.99.",
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Enter a correct value (dot to separate the integer and decimal parts):",
        )
        return

    try:
        value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    except InvalidOperation:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid value. Please enter a number.",
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Enter a correct value (dot to separate the integer and decimal parts):",
        )
        return

    add_stat_db(update.effective_chat.id, metric_uuid, value)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Stat added successfully.",
    )
    reset_user_data(context)


async def request_report(update, context):
    chat_id = update.effective_user.id
    metrics = get_user_metrics_db(chat_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Select metric:',
        reply_markup=_convert_buttons_to_reply_markup([
            [
                (metric[1], f'get_report_{metric[0]}')
                for metric in metrics
            ],
        ]),
    )


async def get_report(update, context):
    metric_uuid = update.callback_query.data.replace('get_report_', '')
    metric_name = get_metric_name_db(metric_uuid)

    excel_stream = generate_report(metric_uuid, metric_name)

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=excel_stream,
        filename=f"{metric_name}.xlsx",
        caption="Your metric report",
    )


async def main_message_handler(update, context):
    if context.user_data.get(ADDING_METRIC_KEY, False):
        await add_metric(update, context)
    elif context.user_data.get(METRIC_UUID_KEY, False):
        await add_stat(update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I do not understand your request.",
        )
