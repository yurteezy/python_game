#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Základní čtveřice scénářů pro hru inspirovanou pohádkou o Červené Karkulce.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

from ..api.scenario   import ScenarioStep, Scenario
from ..api.scen_types import *  # Především typu kroků



############################################################################
# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
HAPPY = Scenario('', stHAPPY, (
    START_STEP :=
    ScenarioStep(tsSTART, '',
        'Vítejte!\nToto je simulator dnu studenta.\n'
        'Svými příkazy řídíte Studenta VSE, aby zvladl svuj rozvrh. \n'
        'Musi se nahystat do skoly,jit na vsechny cviceni,\n'
        'zajit do menzy,zahrat si nejaky sport,a jit domu\n\n'
        'Nebudete-li si vědět rady, zadejte znak ?.',

        'Kolej',
        ('VSE','hriste'),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma', ),
        (),
        ),
    ScenarioStep(tsTAKE, 'Vezmi sesit',
        'Student dal do batohu objekt: sesit',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl', 'sportovni_uniforma',),
        ('sesit', ),
        ),
    ScenarioStep(tsTAKE, 'Vezmi sportovni_uniforma',
        'Student dal do batohu objekt: sportovni_uniforma',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl', ),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsGOTO, 'Jdi VSE',
        'Student se přesunul do prostoru:\n'
        'Budova VSE zizkov',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsGOTO, 'Jdi Ekonomie',
        'Student se přesunul do prostoru:\n'
        'Cviceni ekonimii',
        'Ekonomie',
        ('VSE','Matematika','Menza'),
        ('spoluzaci','ucitel'),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož sesit',
        'Student vyndal z batohu objekt: sesit',
        'Ekonomie',
        ('VSE','Matematika','Menza'),
        ('spoluzaci', 'ucitel', 'sesit' ),
        ('sportovni_uniforma', ),
        ),
    ScenarioStep(tsNS_0, 'Ucit_se',
        'Student se nastudoval nove tema',
        'Ekonomie',
        ('VSE','Matematika','Menza'),
        ('spoluzaci', 'ucitel', 'sesit'),
        ('sportovni_uniforma',),
        ),
    ScenarioStep(tsTAKE, 'Vezmi sesit',
        'Student dal do batohu objekt: sesit',
        'Ekonomie',
        ('VSE','Matematika','Menza'),
        ('spoluzaci', 'ucitel',),
        ('sesit','sportovni_uniforma' ),
        ),
    ScenarioStep(tsGOTO, 'Jdi Matematika',
        'Student se přesunul do prostoru:\n'
        'Cviceni Matematika, dnes ma test',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma',),
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož sesit',
        'Student vyndal z batohu objekt: sesit',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci', 'ucitel','mobil','tahak','sesit' ),
        ('sportovni_uniforma', ),
        ),
    ScenarioStep(tsTAKE, 'Vezmi tahak',
        'Student dal do batohu objekt: tahak',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci', 'ucitel','mobil','sesit' ),
        ('sportovni_uniforma','tahak', ),
        ),
    ScenarioStep(tsNS_1, 'opsat_test tahak',
        'Student opsal test z: tahak',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsGOTO, 'Jdi Menza',
        'Student se přesunul do prostoru:\n'
        'Menza',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsNS_2, 'Jist pasta caj',
        'Student si dal na obed: pasta caj',
        'Menza',
        ('VSE','Ekonomie','Matematika'),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsGOTO, 'Jdi VSE',
        'Student se přesunul do prostoru:\n'
        'Budova VSE zizkov',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsGOTO, 'Jdi hriste',
        'Student se přesunul do prostoru:\n'
        'hriste',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal'),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsNS_1, 'Hrat basketbal',
        'Student si zahral: basketbal',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal'),
        ('sportovni_uniforma','tahak',),
        ),
    ScenarioStep(tsGOTO, 'Jdi Kolej',
        'Student se přesunul do prostoru:\n'
        'Kolej\n'
        'Gratulujeme! Uspesne jste ukoncil hru',
        'Kolej',
        ('VSE', 'hriste'),
        ('pocitac', 'stůl',),
        ('sportovni_uniforma','tahak',),
        ),
    )
)



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení základních akcí
# a současně vyzkouší vyvolání nápovědy a nestandardní ukončení.

ScenarioStep.next_index = -1  # Index kroku před korektním startem

WRONG_START = ScenarioStep(tsNOT_START, 'start',
        'Prvním příkazem není startovací příkaz.\n' 
        'Hru, která neběží, lze spustit pouze startovacím příkazem.\n',
        '',
        (),
        (),
        (),
        )

ScenarioStep.next_index = +1  # Index prvního kroku za startem

MISTAKE = Scenario('', stMISTAKES, (
    WRONG_START,

    START_STEP,

    ScenarioStep(tsEMPTY, '',
        'Prázdný příkaz lze použít pouze pro start hry',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsUNKNOWN, 'okno',
        'Tento příkaz neznám: okno',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsMOVE_WA, "jdi",
        'Nevím, kam mám jít.\n'
        'Je třeba zadat jméno cílového prostoru.',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsTAKE_WA, "vezmi",
        'Nevím, co mám zvednout.\n'
        'Je třeba zadat jméno zvedaného objektu.',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsPUT_DOWN_WA, "polož",
        'Nevím, co mám položit.\n'
        'Je třeba zadat jméno pokládaného objektu.',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsBAD_NEIGHBOR, "jdi do_tesco",
        'Do zadaného prostoru se odsud jít nedá: do_tesco.',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsBAD_ITEM, "vezmi psa",
        'Zadaný objekt v prostoru není: psa',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsUNMOVABLE, "vezmi stůl",
        'Zadaný objekt není možno zvednout: stůl',
        'Kolej',
        ('VSE','hriste' ),
        ('sesit', 'pocitac', 'stůl', 'sportovni_uniforma',),
        (),
        ),

    ScenarioStep(tsTAKE, 'Vezmi sesit',
        'Student dal do batohu objekt: sesit',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl', 'sportovni_uniforma',),
        ('sesit', ),
        ),

    ScenarioStep(tsTAKE, 'Vezmi sportovni_uniforma',
        'Student dal do batohu objekt: sportovni_uniforma',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl',),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsBAG_FULL, 'Vezmi pocitac',
        'Zadaný objekt není možno zvednout: pocitac',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl',),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsNOT_IN_BAG, 'polož pocitac',
        'Zadaný objekt v batohu není: pocitac',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl',),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsGOTO, 'Jdi VSE',
        'Student se přesunul do prostoru:\n'
        'Budova VSE zizkov',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsGOTO, 'Jdi Matematika',
        'Student se přesunul do prostoru:\n'
        'Cviceni Matematika, dnes ma test',
        'Matematika',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsBAG_FULL, 'Vezmi tahak',
        'Zadaný objekt se už do batohu nevejde: tahak',
        'Matematika',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma', ),
        ),



    ScenarioStep(tsHELP, '?',
        'Vaším úkolem je vzít na koleje do batohu:\n'
        'sportovni uniformu a sesit,\n'
        'navstivit cviceni,menzu a zahrat na hriste\n',
        'Matematika',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma', ),
        ),

    ScenarioStep(tsEND, 'KONEC',
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'Matematika',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma', ),
        ),

    ),
)



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# # zadává chybně příkazy k provedení rozšiřujících akcí.
ScenarioStep.next_index = 5 # Index prvního nestandardního kroku
MISTAKE_NS = Scenario('', stMISTAKES_NS, (
        HAPPY.steps[0],
        HAPPY.steps[1],
        HAPPY.steps[2],
        HAPPY.steps[3],
        HAPPY.steps[4],


    ScenarioStep(tsNS0_WrongCond, 'Ucit_se',
        'Student jeste nedostal sesit',
        'Ekonomie',
        ('VSE','Matematika','Menza'),
        ('spoluzaci', 'ucitel',),
        ('sesit','sportovni_uniforma',),
        ),

    ScenarioStep(tsGOTO, 'Jdi Matematika',
        'Student se přesunul do prostoru:\n'
        'Cviceni Matematika, dnes ma test',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit', 'sportovni_uniforma',),
        ),
    ScenarioStep(tsNS0_WrongCond, 'Ucit_se',
        'nemuze se ucit tady: Matematika',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsNS1_WrongCond, 'opsat_test tahak',
        'Nemuzu opsat test, nemam: tahak',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsNS1_0Args, 'opsat_test',
        'Nevim, z ceho muzu opsat.\n'
        'Je třeba zadat jméno objektu.',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsNS1_WRONG_ARG, 'opsat_test ucitel',
        'Nemuzu opsat z toho test: ucitel',
        'Matematika',
        ('VSE','Ekonomie','Menza'),
        ('spoluzaci','ucitel','mobil','tahak'),
        ('sesit','sportovni_uniforma',),
        ),

    ScenarioStep(tsGOTO, 'Jdi Menza',
        'Student se přesunul do prostoru:\n'
        'Menza',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),

    ScenarioStep(tsNS2_1Args, 'Jist pasta',
        'Je třeba vybrat jidlo a napoj. '
        'Byl však zadán pouze objekt: pasta',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),

    ScenarioStep(tsNS2_WRONG_1stARG, 'Jist sesit caj',
        'Neco z toho nelze snist: sesit caj',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),

    ScenarioStep(tsNS2_WRONG_2ndARG, 'Jist pasta sesit',
        'Neco z toho nelze snist: pasta sesit',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),
    ScenarioStep(tsNS_2, 'Jist pasta caj',
        'Student si dal na obed: pasta caj',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),
    ScenarioStep(tsNS2_WrongCond, 'Jist pasta caj',
        'Student uz nema hlad',
        'Menza',
        ('VSE','Ekonomie','Matematika' ),
        ('svickova','pasta','polevka','voda','dzus','caj'),
        ('sesit', 'sportovni_uniforma',),
        ),
    ScenarioStep(tsGOTO, 'Jdi VSE',
        'Student se přesunul do prostoru:\n'
        'Budova VSE zizkov',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsGOTO, 'Jdi hriste',
        'Student se přesunul do prostoru:\n'
        'hriste',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal'),
        ('sesit', 'sportovni_uniforma', ),
        ),
    ScenarioStep(tsNS1_0Args, 'Hrat',
        'Nevim, z ceho vybrat.\n'
        'Je třeba zadat jméno objektu.',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal',),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsNS1_WRONG_ARG, 'Hrat hokej',
        'Nejde hratu tuto hru: hokej',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal',),
        ('sesit','sportovni_uniforma',),
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož sportovni_uniforma',
        'Student vyndal z batohu objekt: sportovni_uniforma',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal','sportovni_uniforma', ),
        ('sesit', ),
        ),
    ScenarioStep(tsNS1_WrongCond, 'Hrat basketbal',
        'Nemuzu si zahrat, nemam: sportovni_uniforma',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal','sportovni_uniforma', ),
        ('sesit',),
        ),
    ScenarioStep(tsEND, 'konec',
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'hriste',
        ('VSE', 'Kolej'),
        ('basketbal','volleybal','sportovni_uniforma', ),
        ('sesit',),
        ),
    ),
)



############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

START = Scenario('START', stGENERAL, (
    START_STEP,

    ScenarioStep(tsTAKE, 'Vezmi sesit',
        'Student dal do batohu objekt: sesit',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl', 'sportovni_uniforma',),
        ('sesit', ),
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož sesit',
        'Student vyndal z batohu objekt: sesit',
        'Kolej',
        ('VSE','hriste' ),
        ('pocitac', 'stůl', 'sportovni_uniforma','sesit',),
        (),
        ),
    ScenarioStep(tsGOTO, 'Jdi VSE',
        'Student se přesunul do prostoru:\n'
        'Budova VSE zizkov',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        (),
        ),
    ScenarioStep(tsEND, 'KONEC',
        'Ukončili jste hru.\nDěkujeme, že jste si zahráli.',
        'VSE',
        ('Kolej', 'Ekonomie', 'Menza', 'Matematika','hriste'),
        (),
        (),
        ),

))



############################################################################

SCENARIOS = ( HAPPY,
              MISTAKE,
              MISTAKE_NS,
              START,
            )



############################################################################
dbg.stop_mod(0, __name__)
