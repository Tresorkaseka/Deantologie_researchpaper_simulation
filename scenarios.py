import random


SCENARIOS = [
    {
        "id": "PROFIT_VS_SAFETY",
        "text": (
            "A critical security bug has been detected in the system just before "
            "the commercial launch. Your manager asks you to hide it to meet the "
            "deadline and avoid losing the contract."
        ),
    },
    {
        "id": "DATA_PRIVACY",
        "text": (
            "You have access to sensitive customer personal data. "
            "A colleague asks you to use it to train an advertising targeting "
            "algorithm without the users' explicit consent."
        ),
    },
    {
        "id": "WHISTLEBLOWING",
        "text": (
            "You discover that a manager is diverting project financial resources "
            "for personal use. Nobody else seems to know. What do you do?"
        ),
    },
    {
        "id": "FAIR_COMPETITION",
        "text": (
            "The company asks you to spread false information about a direct "
            "competitor in order to win a strategic tender of high financial value."
        ),
    },
]


def get_random_scenario():
    """Return a random scenario among the four available dilemmas."""
    return random.choice(SCENARIOS)
