def get_bot_message(lang: str, key: str) -> str:
    """Generate random string

    Args:
        lang (str): Langugae
        key (str): Option

    Returns:
        str: random string
    """
    return STRINGS[lang][key]


STRINGS = {
    'EN': {
        'Welcome': 'Hello! I\'m your ASR bot.',
        'EmptyMessage' : 'Empty Message, Try Again',
        'Tips': 'Please, Send Voice message. You can send ONLY Voice message',
        'HelpInfo': 'Send a voice message and receive a transcription\n\n'
                    'A brief manual on bot commands:\n'
                    '/start command will allow you to start the bot and reset the dialog\n'
                    '/help  command will allow you to get a brief overview of the bot and its commands'
    },
    'RU': {}
}