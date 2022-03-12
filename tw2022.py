
"""
My version of the classic BBS multiplayer game "Tradewars 2002"
"""

from dataclasses import dataclass, asdict, field, InitVar, replace
# maybe use for custom variable typing
# from typing import NewType
# from typing import Any
from typing import List
from random_word import RandomWords
rw = RandomWords()

SHIP_CLASSES = 'S A B C'.split()
SHIP_TYPES = 'Sloop Frigate Cruiser Battleship Carrier'.split()

@dataclass
class Asset(object):
    """
    Meta class for ships and whatnot
    TODO: refactor as dataclass
    """
    name: str
    owner: str
    atype: str
    location: str

def make_deck(name, owner, dtype):
    return [Deck(name, owner, dtype, self.deckcontents)]

@dataclass
class Deck(object):
    """
    Meta class to create and maintain iterables of objects in the game.
    """
    name: str
    owner: str
    dtype: str
    deckcontents: List[Asset] = field(default_factory=make_deck)

    @classmethod
    def add_item(cls, item):
        cls.deckcontents.append(item)

def make_ship(name, owner, atype, location, stype, sgrade):
    return Ship(name, owner, atype, location, stype, sgrade)

@dataclass
class Ship(Asset):
    """
    Spaceship class
    Note to self: subclassing a dataclass requires it's own decorator.
    """

    stype: str
    sgrade: str

    def rename(self, newname):
        sfields = fields(self)
        print(sfields)
        self.name = newname

def make_agent(name, base_location, credit):
    return Agent(name, base_location, credit)

@dataclass
class Agent(object):
    """
    Meta class for players and NPCs
    """

    name: str
    base_location: str
    credit: int
    propertylist: List[Deck] = field(default_factory=lambda:['Assets', self.name,
                                                             'Assets'])
    shipdeck: List[Deck] = field(default_factory=lambda:['Ships', self.name, 'Ships'])

def make_faction(name, base_location, credit):
    return [Faction(name, base_location, credit)]

@dataclass
class Faction(Agent):
    """
    Group of Agents, able to act as single entity
    """

    members: List = field(default_factory=list)


def make_PC(name, base_location, credit, plocation):
    return PlayerChar(name, base_location, credit, plocation)

@dataclass
class PlayerChar(Agent):
    """
    The Player Character
    """

    plocation: str = field(default=False)

def make_NPC(name, base_location, credit, plocation):
    return NPC(name, base_location, credit, plocation)

@dataclass
class NPC(PlayerChar):
    """
    Non-Player Character
    """

@dataclass
class Location:
    """
    Meta class for locations
    """

    name: str

def make_galaxy(name):
    return Galaxy(name)

@dataclass
class Galaxy(Location):
    """
    List of Locations
    """

    places: List = field(default_factory=list)

    def add_location(cls, location):
        cls.places.append(location)


def make_planet(name, galaxy, inhabited, pclass):
    return Planet(name, galaxy, inhabited, pclass)

@dataclass
class Planet(Location):
    """
    A Planet
    """

    galaxy: List[Galaxy]
    inhabited: bool
    pclass: str



startingFunds = 35000
shipBaseValue = 10000

def testworld():
    galaxy1 = make_galaxy("Milky Way")
    planet1 = make_planet("Earth", galaxy1, True, "M")
    planet2 = make_planet("Mars", galaxy1, False, "K")
    galaxy1.add_location(planet1)
    galaxy1.add_location(planet2)

    player1 = make_PC("Grant", planet1, startingFunds, planet1)
    npc1 = make_NPC("Lillian", planet1, startingFunds, planet1)

    fctn1 = make_faction("The Gang", planet1, startingFunds)

    fctn1[0].members.append(player1)
    fctn1[0].members.append(npc1)

    ship1 = make_ship("Enterprise", player1, "Ship", planet1, SHIP_TYPES[0],
            SHIP_CLASSES[0])

    ship2 = make_ship("Titanic", player1, "Ship", planet1, SHIP_TYPES[1],
            SHIP_CLASSES[2])

    player1.shipdeck.add_item(ship1)
    player1.shipdeck.add_item(ship2)
    return
