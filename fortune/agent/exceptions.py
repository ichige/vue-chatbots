class InputRequiredException(Exception):
    """
    入力ダイアログの表示用例外クラス
    """
    def __init__(self, name: str, message: str, label: str, placeholder: str = "") -> None:
        self.name = name
        self.message = message
        self.label = label
        self.placeholder = placeholder
        super().__init__(f"Input required {name}")

    def to_dict(self) -> dict:
        """
        プロパティを dict 型で返す
        """
        return {
            "name": self.name,
            "message": self.message,
            "label": self.label,
            "placeholder": self.placeholder
        }