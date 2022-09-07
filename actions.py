#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul zodpovědný za reakci hry na zadávané příkazy.
Představuje správce akcí, který rozhoduje,
která akce dostane na starost zpracování aktuálního příkazu
a řídí celkové chování v závislosti na tom, je-li hra právě aktivní.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from abc import ABC, abstractmethod

from .      import world
from .world import ANamed, current_place
import operator



############################################################################

def execute_command(command:str) -> str:
    """Zpracuje zadaný příkaz a vrátí odpověď hry.
    Zadaný příkaz zanalyzuje a v závislosti na aktuální aktivitě hry
    rozhodne, která akce dostane na starost jeho zpracování.
    Vrátí odpověď hry na zadaný příkaz.
    """
    command = command.strip()
    if command:
        # Zadán string obsahující nebílé znaky
        if is_alive():
            return _execute(command)
        else:
            return ('Prvním příkazem není startovací příkaz.\n' 
            'Hru, která neběží, lze spustit pouze startovacím příkazem.\n')
    else:
        # Zadán prázdný string nebo string obsahující jen bílé znaky
        if is_alive():
            return 'Prázdný příkaz lze použít pouze pro start hry'
        else:
            _start_game()
            return ('Vítejte!\nToto je simulator dnu studenta.\n'
        'Svými příkazy řídíte Studenta VSE, aby zvladl svuj rozvrh. \n'
        'Musi se nahystat do skoly,jit na vsechny cviceni,\n'
        'zajit do menzy,zahrat si nejaky sport,a jit domu\n\n'
        'Nebudete-li si vědět rady, zadejte znak ?.'
            )


def _start_game():
    """Inicializuje stav hry a spustí hru.
    """
    _initialize()
    global _is_alive
    _is_alive = True


def _execute(command):
    """Realizuje zadaný příkaz.
    """
    words       = command.split()
    action_name = words[0].lower()
    action      = _NAME_2_ACTION.get(action_name)
    if not action:
        return f'Tento příkaz neznám: {words[0]}'

    for x in world.current_place().items:
        if x not in _OBJEKTY:
            _OBJEKTY.append(x)
    for x in world.BAG.items:
        if x not in _OBJEKTY:
            _OBJEKTY.append(x)


    answer = action.execute(words)
    return answer


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _is_alive


def _initialize():
    """V rámci startu hry inicializuje všechny potřebné objekty.
    """
    world.initialize()
    global _LATKA, _FOOD, _DRINK, _SPORT , _EATED, _OBJEKTY
    _LATKA = ('tahak', 'mobil')
    _FOOD = ('svickova', 'pasta', 'polevka')
    _DRINK = ('voda', 'dzus', 'caj')
    _SPORT = ('basketbal','volleybal')
    _EATED = False
    _OBJEKTY = []


############################################################################

class AAction(ANamed):
    """Společná rodičovská třída všech akcí.
    """

    def __init__(self, name:str, description:str):
        """Vytvoří rodičovský podobjekt dané akce, který si zapamatuje
        název dané akce a její popis.
        """
        super().__init__(name)
        self._description = description


    @property
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """
        return self._description


    @abstractmethod
    def execute(self, arguments:tuple[str]) -> str:
        """Metoda realizující reakci hry na zadání daného příkazu.
        Předávané pole je vždy neprázdné, protože jeho nultý prvek
        je zadaný název vyvolaného příkazu. Počet argumentů je závislý
        na konkrétním akci, ale pro každou akci je konstantní.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

class Goto(AAction):
    """Definuje povinnou akci přesouvající hráče do sousedního prostoru.
    """

    def __init__(self):
        super().__init__('Jdi',
                         'Přesune Studenta do zadaného prostoru')


    def execute(self, arguments:tuple[str]) -> str:
        """Přesune hráče do zadaného sousedního prostoru.
        """
        if len(arguments) < 2:
            return ('Nevím, kam mám jít.\n'
                    'Je třeba zadat jméno cílového prostoru.')
        place_name = arguments[1].lower()
        place      = world.place(place_name)
        if (not place) or (not place in current_place().neighbors):
            return f'Do zadaného prostoru se odsud jít nedá: {place_name}.'
        world._current_place = place
        msg = f'Student se přesunul do prostoru:\n{place.description}'

        if world.BAG.item('tahak') and place.name == 'Kolej':
            global _is_alive
            _is_alive = False
            msg += '\nGratulujeme! Uspesne jste ukoncil hru'

        return msg



############################################################################

class Take(AAction):
    """Definuje povinnou akci přesouvající objekt
    z aktuálního prostoru do batohu.
    """

    def __init__(self):
        super().__init__('Vezmi',
                         'Přesune zadaný předmět z prostoru do batohu')


    def execute(self, arguments:tuple[str]) -> str:
        """Přesune zadaný objekt z aktuálního prostoru do batohu.
        """
        if len(arguments) < 2:
            return ('Nevím, co mám zvednout.\n'
                    'Je třeba zadat jméno zvedaného objektu.')
        item_name = arguments[1]
        item      = current_place().remove_item(item_name)
        if not item:
            return f'Zadaný objekt v prostoru není: {item_name}'
        if item.weight == world.Item.HEAVY:
            current_place().add_item(item)
            return f'Zadaný objekt není možno zvednout: {item.name}'
        if world.BAG.add_item(item):
            return f'Student dal do batohu objekt: {item.name}'
        else:
            return f'Zadaný objekt se už do batohu nevejde: {item.name}'



############################################################################

class PutDown(AAction):
    """Definuje povinnou akci přesouvající objekt
    z batohu do aktuálního prostoru.
    """

    def __init__(self):
        super().__init__('polož',
                         'Přesune zadaný předmět z batohu do prostoru')



    def execute(self, arguments:tuple[str]) -> str:
        """Přesune zadaný objekt z batohu do aktuálního prostoru.
        """
        if len(arguments) < 2:
            return ('Nevím, co mám položit.\n'
                    'Je třeba zadat jméno pokládaného objektu.')
        item_name = arguments[1].lower()
        item      = world.BAG.remove_item(item_name)
        if not item:
            return f'Zadaný objekt v batohu není: {item_name}'
        current_place().add_item(item)
        return f'Student vyndal z batohu objekt: {item.name}'



############################################################################

class Help(AAction):
    """Definuje povinnou akci reagující na žádost o nápovědu.
    """

    def __init__(self):
        super().__init__('?',
            'Popíše cíl hry spolu s přehledem příkazů, jež jsou k dispozici')


    def execute(self, arguments:tuple[str]) -> str:
        """Vrátí text jednoduché nápovědy popisující
        všechny dostupné příkazy.
        """
        result = (
            'Vaším úkolem je vzít na koleje do batohu:\n'
        'sportovni uniformu a sesit,\n'
        'navstivit cviceni,menzu a zahrat na hriste\n' +
            '\n\n'.join(a.name + '\n' + a.description
                        for a in _NAME_2_ACTION.values())
        )
        return result



############################################################################

class END(AAction):
    """Definuje povinnou akci reagující na žádost o ukončení hry.
    """

    def __init__(self):
        super().__init__('Konec',
            'Ukončí hru a poděkuje hráči za hru')


    def execute(self, arguments:tuple[str]) -> str:
        """Ukončí hru a poděkuje hráči za hru.
        """
        global _is_alive
        _is_alive = False
        return 'Ukončili jste hru.\nDěkujeme, že jste si zahráli.'



############################################################################

class Study(AAction):
    """Definuje akci pomoci kterou studuje.
    """

    def __init__(self):
        super().__init__('Ucit_se',
                         'Student nastuduje latku')


    def execute(self, arguments:tuple[str]) -> str:
        """Provede akci studovani.
        """
        item = current_place().item('sesit')
        cp = str(current_place())
        if 'Ekonomie' not in cp:
            return f'nemuze se ucit tady: {cp}'
        if not item:
            return f'Student jeste nedostal sesit.'
        else:
            return f'Student se nastudoval nove tema'




############################################################################


class Cheat(AAction):
    """Opise test pri pomoci tahaku.
    """
    def __init__(self):
        super().__init__('opsat_test',
                         'Opise test pri pomoci tahaku')

    def execute(self, arguments:tuple[str]) -> str:
        """Zkontroluje jesli ma tahak a opise test.
        """
        if len(arguments) < 2:
            return ('Nevim, z ceho muzu opsat.\n'
                    'Je třeba zadat jméno objektu.')
        item_name = arguments[1].lower()
        item = world.BAG.item(item_name)
        cp = str(current_place())
        if 'Matematika' not in cp:
            return f'nema tady test: {cp}'
        if item_name not in _LATKA:
            return f'Nemuzu opsat z toho test: {item_name}'
        if not item:
            return f'Nemuzu opsat test, nemam: {item_name}'
        return f'Student opsal test z: {item_name}'




############################################################################

class Eat(AAction):
    """Sni jidlo, pokud jste spravne vybral.
    """
    global _EATED
    def __init__(self):
        super().__init__('Jist',
                         'Sni jidlo, ktere vybere')

    def execute(self, arguments:tuple[str], ) -> str:
        """Zkontroluje vyber a sni jidlo.
        """
        if len(arguments) < 3:
            msg = 'Je třeba vybrat jidlo a napoj. '
            if len(arguments) < 2:
                msg += 'Nebylo však zadáno nic.'
            else:
                msg += f'Byl však zadán pouze objekt: {arguments[1]}'
            return msg
        cp = str(current_place())
        global _EATED
        if _EATED:
            return f'Student uz nema hlad'
        if 'Menza' not in cp:
             return f'Nejste v menze: {cp}'
        item1 = arguments[1].lower()
        item2 = arguments[2].lower()
        if item1 in _FOOD:
            if item2 in _DRINK:
                _EATED = not _EATED
                return f'Student si dal na obed: {item1} {item2}'
        if item2 in _FOOD:
            if item1 in _DRINK:
                _EATED = not _EATED
                return f'Student si dal na obed: {item1} {item2}'
        else:return f'Neco z toho nelze snist: {item1} {item2}'


############################################################################
class Play(AAction):
    """Zahraji si hru.
    """
    def __init__(self):
        super().__init__('hrat',
                         'Zahraji si nejaky sport')

    def execute(self, arguments:tuple[str]) -> str:
        """Zahraje hru.
        """
        if len(arguments) < 2:
            return ('Nevim, z ceho vybrat.\n'
                    'Je třeba zadat jméno objektu.')
        item_name = arguments[1].lower()
        item = world.BAG.item('sportovni_uniforma')
        cp = str(current_place())
        if 'hriste' not in cp:
            return f'Nejste na hriste: {cp}'
        if not item:
            return f'Nemuzu si zahrat, nemam: sportovni_uniforma'
        if item_name not in _SPORT:
            return f'Nejde hratu tuto hru: {item_name}'
        return f'Student si zahral: {item_name}'




############################################################################

# Indikace toho, zda hra doopravdy běží (= je živá), nebo jen hibernuje
_is_alive = False

# Slovník se všemi definovanými akcemi indexovanými svými názvy
# převedenými na malá písmena
_NAME_2_ACTION = {
        'jdi'     : Goto(),
        'vezmi'   : Take(),
        'polož'   : PutDown(),
        'konec'   : (_END := END()), # Aby bylo možno akci spustit přímo
        '?'       : Help(),
        'ucit_se' : Study(),
        'opsat_test' : Cheat(),
        'jist'  : Eat(),
        'hrat'  : Play(),
    }

# Slovník, kde klíčem je název (malými písmeny) objektu
# a hodnotou je informace o tom, je-li daný objekt již vzhůru
# Názvy stačí, protože víme, že každý z objektů bude ve hře jen jeden
_AWAKE:dict[str:bool]

# Slovník, kde klíčem je název (malými písmeny) objektu,
# který lze pozdravit, a hodnotou je informace o tom, zda již byl pozdraven.
_GREETED:dict[str:bool]

# Slovník, kde klíčem je název (malými písmeny) objektu, jemuž lze popřát
# k narozeninám a hodnotou je informace o tom, zda mu již bylo popřáno.
_WISHED:dict[str:bool]



############################################################################
dbg.stop_mod(0, __name__)
