
class Server(Redis):
    def __init__(self, *args, **kwargs):
        """
        host: str, port: int, decode_responses: bool
        """
        super().__init__(*args, **kwargs)

    def get_int(self, key: str, default=0) -> int:
        val = self.get(key)
        if val is None:
            return default
        return int(val)

    def set_int(self, key: str, value: int):
        self.set(key, int(value))