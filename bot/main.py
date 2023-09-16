from events import on_startup, on_shutdown
from misc import executor_
from handlers import *


def main():
    executor_.on_startup(on_startup)
    executor_.on_shutdown(on_shutdown)
    executor_.start_polling(reset_webhook=True, fast=True)


if __name__ == "__main__":
    main()

