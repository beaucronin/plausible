class PlausibleException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class ItemNotFoundException(PlausibleException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)