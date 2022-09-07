#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul vystupuje v roli správce světa hry a jeho prostorů.
Má na starosti vzájemné propojení jednotlivých prostorů
a udržuje informaci o tom, ve kterém z nich se hráč právě nachází.
Vzájemné uspořádání prostorů se může v průběhu hry měnit –
prostory mohou v průběhu hry získávat a ztrácet sousedy.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################



############################################################################

class ANamed():
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        self._name = name
        super().__init__(**args)

    @property
    def name(self) -> str:
        """Vrátí název daného objektu.
        """
        return self._name


    def __repr__(self) -> str:
        """Vrátí uživatelský textový podpis jako název dané instance.
        """
        return self._name



############################################################################

class Item(ANamed):
    """Instance představují h-objekty v prostorech či batohu.
    """

    HEAVY: int = 999    # Váha nepřenositelného h-objektu

    def __init__(self, name:str, **args):
        """Vytvoří h-objekt se zadaným názvem. Podle prvního znaku
        pozná přenositelnost objektu a nastaví jeho váhu.
        Zbylé znaky argumentu si zapamatuje jako jeho název.
        """
        prefix    = name[0]   # Předpona indikující další vlastnosti
        real_name = name[1:]  # Název h-objektu používaný v příkazech
        super().__init__(real_name)
        self._weight = 1 if prefix == '_' else Item.HEAVY


    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        return self._weight



############################################################################

class AItemContainer():
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        super().__init__(**args)
        self._initial_item_names = initial_item_names


    def initialize(self) -> None:
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        self._items = [Item(name) for name in self._initial_item_names]
        self._names = [item.name.lower() for item in self._items]


    @property
    def items(self) -> list[Item]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        return self._items


    def item(self, name:str) -> Item:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        name = name.lower()
        if name in self._names:
            result = self._items[self._names.index(name)]
            return result
        return None


    def add_item(self, item:Item) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        # Přidá předmět i jeho ("zmenšený") název na konec odpovídajících
        # seznamů, takže budou mít oba shodný index
        self._items.append(item)
        self._names.append(item.name.lower())
        # Předpokládá, že se to vždy podaří. Potomek, pro nějž by to
        # nemuselo platit, přebije metodu vlastní verzí.
        return True


    def remove_item(self, item_name:str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        name = item_name.lower()
        if name in self._names:
            index  = self._names.index(name)
            # Ví, že název i předmět mají ve svých seznamech shodné indexy
            name   = self._names.pop(index)
            result = self._items.pop(index)
            return result
        # Název v seznamu názvů není
        return None



############################################################################

class Bag(AItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    def __init__(self, initial_item_names:tuple[str]):
        """Definuje batoh jako kontejner h-objektů s omezenou kapacitou.
        """
        super().__init__(initial_item_names)


    def initialize(self) -> None:
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        super().initialize()


    def add_item(self, item:Item) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        # Předpokládáme, že v batohu je málo předmětů a že to sčítání vah
        # nebude nijak zdržovat - alternativou by byl atribut instance
        if sum(i.weight for i in self.items) + item.weight > self.capacity:
            return False
        else:
            super().add_item(item)
            return True


    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        return 2



############################################################################

class Place(ANamed, AItemContainer):
    """Instance představují prostory, mezi nimiž hráč přechází.
    Prostory jsou definovány jako pojmenované kontejnery objektů.
    Prostory mohou obsahovat různé objekty,
    které mohou hráči pomoci v dosažení cíle hry.
    Každý prostor zná své aktuální bezprostřední sousedy
    a ví, jaké objekty se v něm v daném okamžiku nacházejí.
    Sousedé daného prostoru i v něm se nacházející objekty
    se mohou v průběhu hry měnit.
    """

    def __init__(self, name:str, description:str,
                 initial_neighbor_names:tuple[str],
                 initial_item_names    :tuple[str]
        ):
        super().__init__(name=name, initial_item_names=initial_item_names)
        self._description            = description
        self._initial_neighbor_names = tuple(name.lower() for name in
                                             initial_neighbor_names)


    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        super().initialize()
        self._name_2_neighbor = {name:_NAME_2_PLACE[name] for
                                 name in self._initial_neighbor_names}


    @property
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """
        return self._description


    @property
    def neighbors(self) -> tuple['IPlace']:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu TypeOfStep.GOTO.
        """
        return tuple(self._name_2_neighbor.values())



############################################################################

def initialize() -> None:
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
    propojení jednotlivých prostorů a jejich výchozí obsah,
    nastaví výchozí aktuální prostor a inicializuje batoh.
    """
    # dbg.prSE(0, 1, 'world.initialize')
    # dbg.prIN(0, f'{dbg.prDict(Place)}')
    BAG.initialize()
    for place in _PLACES: place.initialize()
    global _current_place
    _current_place = _NAME_2_PLACE['kolej']
    # dbg.prSE(0, 0, 'world.initialize')



def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
    tj. na prostor, v němž se hráč pravé nachází.
    """
    return _current_place


def places() -> tuple[Place]:
    """Vrátí n-tici odkazů na všechny prostory ve hře
    včetně těch aktuálně nedosažitelných či neaktivních.
    """
    return _PLACES


def place(name:str) -> Place:
    """Vrátí prostor se zadaným názvem.
    Pokud ve hře takový není, vrátí None.
    """
    result = _NAME_2_PLACE.get(name.lower())
    return result



############################################################################

_PLACES = (
    Place('Kolej',
          'Kolej',
         ('VSE', 'hriste'),
         ('_sesit', '#pocitac', '#stůl', '_sportovni_uniforma', ),
         ),
    Place('VSE',
          'Budova VSE zizkov',
          ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
          ()
         ),
    Place('Ekonomie',
          'Cviceni ekonimii',
          ('VSE','Matematika','Menza'),
          ('#spoluzaci','#ucitel')
         ),
    Place('Matematika',
          'Cviceni Matematika, dnes ma test',
          ('VSE','Ekonomie','Menza'),
          ('#spoluzaci','#ucitel','_mobil','_tahak')
         ),
    Place('Menza',
          'Menza',
          ('VSE','Ekonomie','Matematika'),
          ('#svickova','#pasta','#polevka','#voda','#dzus','#caj')
         ),
    Place('hriste',
          'hriste',
          ('VSE', 'Kolej'),
          ('#basketbal','#volleybal')
         ),
)

_NAME_2_PLACE = {p.name.lower():p for p in _PLACES}



############################################################################

# Jediná instance batohu
# V této hře neobsahuje žádnou výchozí sadu h-objektů =>
# jako argument předáváme prázdnou n-tici
BAG:Bag = Bag(())

# Aktuální prostor = prostor, v němž se hráč právě nachází
_current_place:Place



############################################################################
dbg.stop_mod(0, __name__)
