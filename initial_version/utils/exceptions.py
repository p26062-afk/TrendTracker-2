class AppError(Exception):
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)
