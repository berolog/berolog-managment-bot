import monobank
import os


MONO_TOKEN = os.getenv('MONO_TOKEN')

mono = monobank.Client(MONO_TOKEN)


def set_webhook(url):
    mono.create_webhook(url)
