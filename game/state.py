# game/state.py
from dataclasses import dataclass, field
from typing import List, Dict, Literal

LogCat = Literal["event","discovery","decision","question","item","ambient"]
ResearchCat = Literal["info","symbol","historical","technical","psychological","warning"]

@dataclass
class GameState:
    game_log: List[Dict] = field(default_factory=list)
    research_log: List[Dict] = field(default_factory=list)
    items: List[Dict] = field(default_factory=list)
