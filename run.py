from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from bot import (
    request_metric,
    request_stat,
    request_stat_value,
    main_message_handler,
    request_report,
    get_report,
)
from constants import BOT_TOKEN

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('add_metric', request_metric))
    application.add_handler(CommandHandler('add_stat', request_stat))
    application.add_handler(CommandHandler('get_report', request_report))

    application.add_handler(
        CallbackQueryHandler(request_stat_value, 'add_stat_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    )
    application.add_handler(
        CallbackQueryHandler(get_report, 'get_report_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    )

    application.add_handler(MessageHandler(None, main_message_handler))

    application.run_polling()
