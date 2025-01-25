
def categorize_label(label: str) -> str:
    """
    Классифицирует метку на одну из трех категорий: kata, combinations или элементы.
    """
    # Ката
    if label in ["Heian-Nidan", ]:
        return "kata"
    
    # Комбинации (начинаются с цифр и содержат '+')
    if label[0].isdigit() or "+" in label:
        return "combinations"
    
    # Элементы (все остальное)
    return "elements"
