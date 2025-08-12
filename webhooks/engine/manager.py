
# Store bot handlers / WARNING! -> High RAM Usage!
class BotManager:
    _bots = {}

    @classmethod
    def add_bot(cls, token: str, bot_engine):
        cls._bots[token] = bot_engine

    @classmethod
    def get_bot(cls, token: str):
        return cls._bots.get(token)
