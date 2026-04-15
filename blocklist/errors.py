class LinkNotExistsError(Exception):
    def __init__(self) -> None:
        super().__init__("Link does not exist")
