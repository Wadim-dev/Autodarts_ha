"""Constants of the Autodarts integration."""

DOMAIN = "autodarts"
CONF_HOST = "host"
CONF_PORT = "port"
STANDARD_PORT = 3180
GERAETENAME = "Autodarts Board"

# event types of the game event entity (also triggers of the light effects)
EREIGNISSE = [
    "dart", "triple", "bull", "bullseye", "visit", "ton", "ton_forty", "one_eighty", "no_score", "bust",
    "three_in_a_bed", "checkout", "high_finish", "nine_darter", "leg_won", "set_won", "match_won",
    "nine_marks", "shanghai", "killer", "eliminated", "halved", "hole_in_one", "tournament_won",
]
