#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Balíček s kompletním řešením jádra dané hry bez uživatelského rozhraní.¤
Aplikace prochází testem dvojicí startovních scénářů obsahujících příkazy
aktivující povinné akce následovaných chybovým scénářem.
"""
import dbg
dbg.start_pkg(0, __name__, __doc__)
############################################################################

# Následující moduly je třeba importovat až při spuštění kontroly typů
# from ..api.scenario import Scenario
# from ..api.game_types import IGame


############################################################################

def authorID() -> str:
    """Vrátí identifikační řetězec autora/autorky programu
    zapsaný VELKÝMI PÍSMENY.
    Tímto řetězcem bývá login do informačního systému školy.
    """
    return 'IURN00'


def authorName() -> str:
    """Vrátí jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
    tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
    u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
    Má-li autor programu více křestních jmen, může je uvést všechna.
    """
    return 'IURTSEV Nikita'


def authorOrigName() -> str:
    """Vrátí jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní
    zapsané v jeho/jejím rodném jazyce.
    """
    return 'ЮРЦЕВ Никита'


def all_scenarios() -> tuple['Scenario']:
    """Vrátí n-tici definovaných scénářů.
    """
    from   .  import scenarios
    result = scenarios.SCENARIOS
    return result


def game() -> 'IGame':
    """Vrátí odkaz na objekt reprezentující hru.
    Tímto objektem je modul definující komunikační funkce hry
    """
    from . import main
    return main



############################################################################

def test_yourself():
    """Otestuje aktuální stav projektu.
    """
    from importlib  import import_module
    me = import_module(__package__)
    from ..tests    import test
    from ..tests    import Level
    test(me, Level.WHOLE)       # Testuje se úspěšné zprovoznění celé hry

# Test spustíte zadáním příkazu
# import game.a1h_whole as at; at.test_yourself()



############################################################################
# Možné úrovně testování

# test(me, Level.HAPPY)       # Testuje definici šťastného scénáře
# test(me, Level.SCENARIOS)   # Testuje základní čtveřici scénářů
# test(me, Level.ARCHITECTURE)# Testuje korespondenci s návrhem
         # architektury, tj. deklaraci navržených modulů a jejich atributů
# test(me, Level.START)       # Testuje spuštění projektu
# test(me, Level.WORLD)       # Testuje svět hry po jejím startu
# test(me, Level.BASIC)       # Testuje realizaci povinných akcí
# test(me, Level.MISTAKES)    # Testuje se, že základní akce jsou robustní
# test(me, Level.WHOLE)       # Testuje se úspěšné zprovoznění celé hry



############################################################################
dbg.stop_mod(0, __name__)
