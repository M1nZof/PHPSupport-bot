from envreader import EnvReader, Field


class Config(EnvReader):
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
