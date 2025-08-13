# game/deps.py
def check_agents_installed() -> bool:
    try:
        import agents  # noqa
        return True
    except Exception:
        return False
