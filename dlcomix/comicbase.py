#!/usr/bin/python
import os
from time import *
from datetime import datetime, timedelta
import re
from PIL import Image
import ConfigParser



gocomics_base = {'2_cows_and_a_chicken' : ['http://www.gocomics.com/features/290-2cowsandachicken',
    'http://www.gocomics.com/2cowsandachicken', '2008/06/30'],
    '9_to_5' : ['http://www.gocomics.com/features/2-9to5',
        'http://www.gocomics.com/9to5', '2001/04/13','9to5'],
    'the_academia_waltz' : ['http://www.gocomics.com/features/3-academiawaltz',
        'http://www.gocomics.com/academiawaltz', '2003/12/08'],
    'adam_at_home' : ['http://www.gocomics.com/features/4-adamathome',
        'http://www.gocomics.com/adamathome', '1995/06/20'],
    'agnes' : ['http://www.gocomics.com/features/5-agnes',
        'http://www.gocomics.com/agnes', '2002/01/01'],
    'andy_capp' : ['http://www.gocomics.com/features/6-andycapp',
        'http://www.gocomics.com/andycapp', '2002/01/01'],
    'animal_crackers' : ['http://www.gocomics.com/features/7-animalcrackers',
        'http://www.gocomics.com/animalcrackers', '2001/04/08'],
    'the_argyle_sweater' : ['http://www.gocomics.com/features/9-theargylesweater',
        'http://www.gocomics.com/theargylesweater', '2006/11/29'],
    'ask_shagg' : ['http://www.gocomics.com/features/10-askshagg',
        'http://www.gocomics.com/askshagg', '2002/08/12'],
    'bc' : ['http://www.gocomics.com/features/11-bc',
        'http://www.gocomics.com/bc', '2002/01/01'],
    'back_in_the_day' : ['http://www.gocomics.com/features/492-backintheday',
        'http://www.gocomics.com/backintheday', '2010/03/08'],
    'bad_reporter' : ['http://www.gocomics.com/features/12-badreporter',
        'http://www.gocomics.com/badreporter', '2005/08/12'],
    'baldo' : ['http://www.gocomics.com/features/13-baldo',
        'http://www.gocomics.com/baldo', '1998/11/22'],
    'ballard_street' : ['http://www.gocomics.com/features/14-ballardstreet',
        'http://www.gocomics.com/ballardstreet', '2002/01/01'],
    'the_barn' : ['http://www.gocomics.com/features/291-thebarn',
        'http://www.gocomics.com/thebarn', '2009/02/02'],
    'barney_and_clyde' : ['http://www.gocomics.com/features/515-barneyandclyde',
        'http://www.gocomics.com/barneyandclyde', '2010/06/07'],
    'basic_instructions' : ['http://www.gocomics.com/features/255-basicinstructions',
        'http://www.gocomics.com/basicinstructions', '2003/02/25'],
    'bewley' : ['http://www.gocomics.com/features/306-bewley',
        'http://www.gocomics.com/bewley', '2009/11/09'],
    'biographic' : ['http://www.gocomics.com/features/18-biographic',
        'http://www.gocomics.com/biographic', '2005/08/14'],
    'the big_picture' : ['http://www.gocomics.com/features/16-thebigpicture',
        'http://www.gocomics.com/thebigpicture', '2010/11/29'],
    'big_top' : ['http://www.gocomics.com/features/17-bigtop',
        'http://www.gocomics.com/bigtop', '2001/04/22'],
    'bird_brains' : ['http://www.gocomics.com/features/251-birdbrains',
        'http://www.gocomics.com/birdbrains', '2007/01/01'],
    'bleeker' : ['http://www.gocomics.com/features/19-bleeker',
        'http://www.gocomics.com/bleeker', '2006/07/27'],
    'bliss' : ['http://www.gocomics.com/features/281-bliss',
        'http://www.gocomics.com/bliss', '2008/07/28'],
    'bloomcounty' : ['http://www.gocomics.com/features/20-bloomcounty',
        'http://www.gocomics.com/bloomcounty',  '1980/12/04'],
    'bo_nanas' : ['http://www.gocomics.com/features/21-bonanas'
        'http://www.gocomics.com/bonanas','2004/01/01'],
    'bob_the_squirrel' : ['http://www.gocomics.com/features/22-bobthesquirrel',
        'http://www.gocomics.com/bobthesquirrel','2004/01/01'],
    'boomerangs' : ['http://www.gocomics.com/features/266-boomerangs',
        'http://www.gocomics.com/boomerangs','2008/06/23'],
    'the_boondocks' : ['http://www.gocomics.com/features/24-boondocks',
        'http://www.gocomics.com/boondocks','1999/04/19'],
    'bottomliners' : ['http://www.gocomics.com/features/26-bottomliners',
        'http://www.gocomics.com/bottomliners','2001/04/18'],
    'bound_and_gagged' : ['http://www.gocomics.com/features/27-boundandgagged',
        'http://www.gocomics.com/boundandgagged', '2001/04/08'],
    'brainwaves' : ['http://www.gocomics.com/features/28-brainwaves',
        'http://www.gocomics.com/brainwaves', '2005/05/16'],
    'brenda_starr' :  ['http://www.gocomics.com/features/29-brendastarr',
        'http://www.gocomics.com/brendastarr','2001/04/04'],
    'brewster_rockit' : ['http://www.gocomics.com/features/30-brewsterrockit'
        'http://www.gocomics.com/brewsterrockit', '2004/07/05'],
    'broom_hilda' : ['http://www.gocomics.com/features/31-broomhilda',
        'http://www.gocomics.com/broomhilda', '2001/04/08'],
    'cafe_con_leche' : ['http://www.gocomics.com/features/508-cafeconleche',
        'http://www.gocomics.com/cafeconleche','2010/05/07'],
    'calvin_and_hobbes'   : ['http://www.gocomics.com/features/32-calvinandhobbes',
        'http://www.gocomics.com/calvinandhobbes','1984/08/14',],
    'candorville' : ['http://www.gocomics.com/features/33-candorville',
        'http://www.gocomics.com/candorville','2004/01/01'],
    'cathy_classics' : ['http://www.gocomics.com/features/35-cathy',
        'http://www.gocomics.com/cathy','1996/03/11'],
    'cest_la_vie' : ['http://www.gocomics.com/features/38-cestlavie',
        'http://www.gocomics.com/cestlavie','2003/11/11'],
    'chuckle_bros' : ['http://www.gocomics.com/features/292-chucklebros',
        'http://www.gocomics.com/chucklebros','2009/02/02'],
    'citizen_dog' : ['http://www.gocomics.com/features/40-citizendog',
        'http://www.gocomics.com/citizendog','1995/05/15'],
    'the_city' : ['http://www.gocomics.com/features/41-thecity',
        'http://www.gocomics.com/thecity','2003/03/05'],
    'cleats' : ['http://www.gocomics.com/features/43-cleats',
        'http://www.gocomics.com/cleats','2001/01/01'],
    'close_to_home' : ['http://www.gocomics.com/features/44-closetohome',
        'http://www.gocomics.com/closetohome','1996/05/27'],
    'compu_toon' : ['http://www.gocomics.com/features/45-compu-toon',
        'http://www.gocomics.com/compu-toon','2001/04/23'],
    'cornered' : ['http://www.gocomics.com/features/47-cornered',
        'http://www.gocomics.com/cornered', '1997/09/01'],
    'cowtown' : ['http://www.gocomics.com/features/558-cowtown',
        'http://www.gocomics.com/cowtown','2010/12/13'],
    'cul_de_sac' : ['http://www.gocomics.com/features/48-culdesac',
        'http://www.gocomics.com/culdesac','2007/09/10'],
    'daddys_home' : ['http://www.gocomics.com/features/265-daddyshome',
        'http://www.gocomics.com/daddyshome','2008/03/08'],
    'dark_side_of_the_horse' : ['http://www.gocomics.com/features/535-darksideofthehorse',
        'http://www.gocomics.com/darksideofthehorse','2010/08/01'],
    'deep_cover' : ['http://www.gocomics.com/features/50-deepcover',
        'http://www.gocomics.com/deepcover','2002/03/27'],
    'diamond_lil' : ['http://www.gocomics.com/features/547-diamondlil',
        'http://www.gocomics.com/diamondlil','2010/10/04'],
    'dick_tracy' : ['http://www.gocomics.com/features/51-dicktracy',
        'http://www.gocomics.com/dicktracy','2001/04/08'],
    'dog_eat_doug' : ['http://www.gocomics.com/features/53-dogeatdoug',
        'http://www.gocomics.com/dogeatdoug','2005/01/02'],
    'dogs_of_ckennel' : ['http://www.gocomics.com/features/546-dogsofckennel',
        'http://www.gocomics.com/dogsofckennel','2010/10/04'],
    'domestic_abuse' : ['http://www.gocomics.com/features/54-domesticabuse',
        'http://www.gocomics.com/domesticabuse','2004/11/10'],
    'doodles' : ['http://www.gocomics.com/features/55-doodles',
        'http://www.gocomics.com/doodles','2001/04/08'],
    'doonesbury' : ['http://www.gocomics.com/features/56-doonesbury',
        'http://www.gocomics.com/doonesbury','1970/10/26'],
    'the_doozies' : ['http://www.gocomics.com/features/285-thedoozies',
        'http://www.gocomics.com/thedoozies','2008/12/01'],
    'the_duplex' : ['http://www.gocomics.com/features/57-duplex',
        'http://www.gocomics.com/duplex','1996/08/12'],
    'eek' : ['http://www.gocomics.com/features/58-eek',
        'http://www.gocomics.com/eek','2007/09/10'],
    'the_elderberries' : ['http://www.gocomics.com/features/59-theelderberries',
        'http://www.gocomics.com/theelderberries','2004/12/06'],
    'flight_deck' : ['http://www.gocomics.com/features/61-flightdeck',
        'http://www.gocomics.com/flightdeck','2002/01/01'],
    'flo_and_friends' : ['http://www.gocomics.com/features/62-floandfriends',
        'http://www.gocomics.com/floandfriends','2001/11/03'],
    'the_flying_mccoys' : ['http://www.gocomics.com/features/63-theflyingmccoys',
        'http://www.gocomics.com/theflyingmccoys','2005/05/09'],
    'for_better_or_for_worse' : ['http://www.gocomics.com/features/64-forbetterorforworse',
        'http://www.gocomics.com/forbetterorforworse', '1981/11/23'],
    'for_heavens_sake' : ['http://www.gocomics.com/features/65-forheavenssake',
        'http://www.gocomics.com/forheavenssake','2002/08/12'],
    'fort_knox' : ['http://www.gocomics.com/features/304-fortknox',
        'http://www.gocomics.com/fortknox','2009/10/05'],
    'foxtrot' : ['http://www.gocomics.com/features/66-foxtrot',
        'http://www.gocomics.com/foxtrot',  '1996/03/11'],
    'foxtrot_classics' : ['http://www.gocomics.com/features/67-foxtrotclassics',
        'http://www.gocomics.com/foxtrotclassics','2007/01/01'],
    'frank_and_ernest' : ['http://www.gocomics.com/features/68-frankandernest',
        'http://www.gocomics.com/frankandernest','2000/07/02'],
    'fred_basset' : ['http://www.gocomics.com/features/69-fredbasset',
        'http://www.gocomics.com/fredbasset','2001/04/08/'],
    'free_range' : ['http://www.gocomics.com/features/280-freerange',
        'http://www.gocomics.com/freerange','2007/02/03/'],
    'frog_applause' : ['http://www.gocomics.com/features/70-frogapplause',
        'http://www.gocomics.com/frogapplause','2006/12/20'],
    'the_fusco_brothers' : ['http://www.gocomics.com/features/71-thefuscobrothers',
        'http://www.gocomics.com/thefuscobrothers','1998/01/01'],
    'garfield' : ['http://www.gocomics.com/features/72-garfield',
        'http://www.gocomics.com/garfield','1978/06/19'],
    'garfield_minus_garfield' : ['http://www.gocomics.com/features/284-garfieldminusgarfield',
        'http://www.gocomics.com/garfieldminusgarfield','2008/11/03'],
    'gazoline_alley' : ['http://www.gocomics.com/features/73-gasolinealley',
        'http://www.gocomics.com/gasolinealley','2001/04/08'],
    'get_a_life' : ['http://www.gocomics.com/features/503-getalife',
        'http://www.gocomics.com/getalife','2010/04/14'],
    'gil_thorp' : ['http://www.gocomics.com/features/74-gilthorp',
        'http://www.gocomics.com/gilthorp','2001/04/18'],
    'ginger_megs' : ['http://www.gocomics.com/features/75-gingermeggs',
        'http://www.gocomics.com/gingermeggs','2004/04/01'],
    'girls_and_sport' : ['http://www.gocomics.com/features/76-girlsandsports',
        'http://www.gocomics.com/girlsandsports','2006/03/12'],
    'haiku_ewe' : ['http://www.gocomics.com/features/298-haikuewe',
        'http://www.gocomics.com/haikuewe','2009/03/09'],
    'heart_of_the_city' : ['http://www.gocomics.com/features/78-heartofthecity',
        'http://www.gocomics.com/heartofthecity','1999/07/01'],
    'heathcliff' : ['http://www.gocomics.com/features/79-heathcliff',
        'http://www.gocomics.com/heathcliff','2002/01/01'],
    'herb_and_jamaal' : ['http://www.gocomics.com/features/81-herbandjamaal',
        'http://www.gocomics.com/herbandjamaal','2002/01/01'],
    'home_and_away' : ['http://www.gocomics.com/features/267-homeandaway',
        'http://www.gocomics.com/homeandaway','2008/06/23'],
    'hubert_and_abby' : ['http://www.gocomics.com/features/84-hubertandabby',
        'http://www.gocomics.com/hubertandabby','2003/10/13'],
    'imagine_this' : ['http://www.gocomics.com/features/301-imaginethis',
        'http://www.gocomics.com/imaginethis','2009/04/08'],
    'in_the_beachers' : ['http://www.gocomics.com/features/86-inthebleachers',
        'http://www.gocomics.com/inthebleachers','1996/08/12'],
    'in_the_sticks' : ['http://www.gocomics.com/features/305-inthesticks',
        'http://www.gocomics.com/inthesticks/2009/10/11/'],
    'ink_pen' : ['http://www.gocomics.com/features/87-inkpen',
        'http://www.gocomics.com/inkpen','2005/11/07'],
    'its_all_about_you' : ['http://www.gocomics.com/features/257-itsallaboutyou',
        'http://www.gocomics.com/itsallaboutyou','2007/12/31'],
    'joe_vanilla' : ['http://www.gocomics.com/features/297-joevanilla',
        'http://www.gocomics.com/joevanilla','2009/02/16'],
    'la_cucaracha' : ['http://www.gocomics.com/features/91-lacucaracha',
        'http://www.gocomics.com/lacucaracha','2002/11/25'],
    'last_kiss' : ['http://www.gocomics.com/features/288-lastkiss',
        'http://www.gocomics.com/lastkiss','2009/01/19'],
    'legend_of_bill' : ['http://www.gocomics.com/features/299-legendofbill',
        'http://www.gocomics.com/legendofbill','2008/05/27'],
    'liberty_meadows' : ['http://www.gocomics.com/features/92-libertymeadows',
        'http://www.gocomics.com/libertymeadows','2002/01/01'],
    'lio' : ['http://www.gocomics.com/features/93-lio',
        'http://www.gocomics.com/lio','2006/05/15'],
    'little_dog_lost' : ['http://www.gocomics.com/features/94-littledoglost',
        'http://www.gocomics.com/littledoglost','2007/03/26'],
    'little_otto' : ['http://www.gocomics.com/features/296-littleotto',
        'http://www.gocomics.com/littleotto','2009/02/23'],
    'loose_parts' : ['http://www.gocomics.com/features/96-looseparts',
        'http://www.gocomics.com/looseparts','2001/04/08'],
    'love_is' : ['http://www.gocomics.com/features/282-loveis',
        'http://www.gocomics.com/loveis','2007/12/17'],
    'lucky_cow' : ['http://www.gocomics.com/features/97-luckycow',
        'http://www.gocomics.com/luckycow','2003/04/21'],
    'maintaining' : ['http://www.gocomics.com/features/98-maintaining',
        'http://www.gocomics.com/maintaining','2007/05/07'],
    'the_meaning_of_lila' : ['http://www.gocomics.com/features/99-meaningoflila',
        'http://www.gocomics.com/meaningoflila','2005/01/02'],
    'the_middletons' : ['http://www.gocomics.com/features/101-themiddletons',
        'http://www.gocomics.com/themiddletons','2001/04/08'],
    'momma' : ['http://www.gocomics.com/features/105-momma',
        'http://www.gocomics.com/momma','2002/01/01'],
    'mutt_and_jeff' : ['http://www.gocomics.com/features/107-muttandjeff',
        'http://www.gocomics.com/muttandjeff','2003/03/05'],
    'mythtickles' : ['http://www.gocomics.com/features/253-mythtickle',
        'http://www.gocomics.com/mythtickle','2007/11/15'],
    'nest_heads' : ['http://www.gocomics.com/features/109-nestheads',
        'http://www.gocomics.com/nestheads','2003/05/30'],
    'neurotica' : ['http://www.gocomics.com/features/110-neurotica',
        'http://www.gocomics.com/neurotica','2003/12/21'],
    'new_adventures_of_queen_victoria' : ['http://www.gocomics.com/features/111-thenewadventuresofqueenvictoria',
        'http://www.gocomics.com/thenewadventuresofqueenvictoria','2006/02/09'],
    'non_sequitur'     : ['http://www.gocomics.com/features/112-nonsequitur',
        'http://www.gocomics.com/nonsequitur','1992/02/16'],
    'the_norm' : ['http://www.gocomics.com/features/113-thenorm',
        'http://www.gocomics.com/thenorm','2006/12/10'],
    'on_a_claire day' : ['http://www.gocomics.com/features/115-onaclaireday',
        'http://www.gocomics.com/onaclaireday','2006/06/18'],
    'one_big_happy' : ['http://www.gocomics.com/features/116-onebighappy',
        'http://www.gocomics.com/onebighappy','2002/01/01'],
    'the_other_coast' : ['http://www.gocomics.com/features/118-theothercoast',
        'http://www.gocomics.com/theothercoast','2002/01/01'],
    'out_of_the_gene_pool_reruns' : ['http://www.gocomics.com/features/137-outofthegenepool',
        'http://www.gocomics.com/outofthegenepool','2001/12/31'],
    'overboard' : ['http://www.gocomics.com/features/119-overboard',
        'http://www.gocomics.com/overboard','1998/01/01'],
    'pibgorn' : ['http://www.gocomics.com/features/120-pibgorn',
        'http://www.gocomics.com/pibgorn','2002/03/11'],
    'pibgorn_sketches' : ['http://www.gocomics.com/features/269-pibgornsketches',
        'http://www.gocomics.com/pibgornsketches','2008/07/14'],
    'pickles' : ['http://www.gocomics.com/features/121-pickles',
        'http://www.gocomics.com/pickles','2003/01/01'],
    'pinkerton' : ['http://www.gocomics.com/features/254-pinkerton',
        'http://www.gocomics.com/pinkerton','2007/10/15'],
    'pluggers' : ['http://www.gocomics.com/features/123-pluggers',
        'http://www.gocomics.com/pluggers','2001/04/08'],
    'pooch_cafe' : ['http://www.gocomics.com/features/124-poochcafe',
        'http://www.gocomics.com/poochcafe','2003/04/27'],
    'pretenna' : ['http://www.gocomics.com/features/126-preteena',
        'http://www.gocomics.com/preteena','2001/04/23'],
    'the_quidmans' : ['http://www.gocomics.com/features/128-thequigmans',
        'http://www.gocomics.com/thequigmans','2001/04/18'],
    'rabbits_against_magic' : ['http://www.gocomics.com/features/289-rabbitsagainstmagic',
        'http://www.gocomics.com/rabbitsagainstmagic','2008/05/31'],
    'real_life_adventures' : ['http://www.gocomics.com/features/129-reallifeadventures',
        'http://www.gocomics.com/reallifeadventures','1998/01/01'],
    'red_and_rover' : ['http://www.gocomics.com/features/130-redandrover',
        'http://www.gocomics.com/redandrover','2003/01/01'],
    'red_meat' : ['http://www.gocomics.com/features/131-redmeat',
        'http://www.gocomics.com/redmeat','2002/03/19'],
    'reynolds_unwrapped' : ['http://www.gocomics.com/features/132-reynoldsunwrapped',
        'http://www.gocomics.com/reynoldsunwrapped','2000/12/14'],
    'ronaldinho_gaucho' : ['http://www.gocomics.com/features/133-ronaldinhogaucho',
        'http://www.gocomics.com/ronaldinhogaucho','2006/05/29'],
    'rubes' : ['http://www.gocomics.com/features/134-rubes',
        'http://www.gocomics.com/rubes','2002/01/01'],
    'scary_gary' : ['http://www.gocomics.com/features/293-scarygary',
        'http://www.gocomics.com/scarygary','2009/02/02'],
    'shoe' : ['http://www.gocomics.com/features/135-shoe',
        'http://www.gocomics.com/shoe','2001/04/08'],
    'shoecabbage' : ['http://www.gocomics.com/features/136-shoecabbage',
        'http://www.gocomics.com/shoecabbage','2003/04/02'],
    'skin_horse' : ['http://www.gocomics.com/features/283-skinhorse',
        'http://www.gocomics.com/skinhorse','2007/12/31'],
    'slowpoke' : ['http://www.gocomics.com/features/138-slowpoke',
        'http://www.gocomics.com/slowpoke','2002/07/22'],
    'speed_bump' : ['http://www.gocomics.com/features/140-speedbump',
        'http://www.gocomics.com/speedbump','2002/01/01'],
    'stone_soup' : ['http://www.gocomics.com/features/142-stonesoup',
        'http://www.gocomics.com/stonesoup','1995/11/20'],
    'strange_brew' : ['http://www.gocomics.com/features/143-strangebrew',
        'http://www.gocomics.com/strangebrew','2002/01/01'],
    'sylvia' : ['http://www.gocomics.com/features/145-sylvia',
        'http://www.gocomics.com/sylvia','2001/04/18'],
    'tank_mcmanara' : ['http://www.gocomics.com/features/146-tankmcnamara',
        'http://www.gocomics.com/tankmcnamara','1998/01/01'],
    'thatababy' : ['http://www.gocomics.com/features/545-thatababy',
        'http://www.gocomics.com/thatababy','2010/09/29'],
    'thin_lines' : ['http://www.gocomics.com/features/509-thinlines',
        'http://www.gocomics.com/thinlines','2010/05/10'],
    'tiny_sepuku' : ['http://www.gocomics.com/features/150-tinysepuku',
        'http://www.gocomics.com/tinysepuku','2003/04/03'],
    'toby' : ['http://www.gocomics.com/features/261-toby',
        'http://www.gocomics.com/toby','2008/02/11'],
    'tom_the_dancing_bug' : ['http://www.gocomics.com/features/151-tomthedancingbug',
        'http://www.gocomics.com/tomthedancingbug','1998/01/04'],
    'too_much_coffee_man' : ['http://www.gocomics.com/features/152-toomuchcoffeeman',
        'http://www.gocomics.com/toomuchcoffeeman','2003/05/18'],
    'wt_duck' : ['http://www.gocomics.com/features/287-wtduck',
        'http://www.gocomics.com/wtduck','2009/01/05'],
    'watch_your_head' : ['http://www.gocomics.com/features/154-watchyourhead',
        'http://www.gocomics.com/watchyourhead','2006/03/27'],
    'wee_pals' : ['http://www.gocomics.com/features/156-weepals',
        'http://www.gocomics.com/weepals','2005/01/02'],
    'wizard_of_id' : ['http://www.gocomics.com/features/158-wizardofid',
        'http://www.gocomics.com/wizardofid','2002/01/01'],
    'working_it_out' : ['http://www.gocomics.com/features/159-workingitout',
        'http://www.gocomics.com/workingitout','2005/01/02'],
    'yenny' : ['http://www.gocomics.com/features/160-yenny',
        'http://www.gocomics.com/yenny','2005/04/25'],
    'zack_hill' : ['http://www.gocomics.com/features/161-zackhill',
        'http://www.gocomics.com/zackhill','2003/01/01'],
    'ziggy' : ['http://www.gocomics.com/features/162-ziggy',
        'http://www.gocomics.com/ziggy','1998/01/01'],
	}


def define_host(comic, path=None, archive=None, full=None):
    if comic :
        if gocomics_base.has_key(comic):
            control_path(path+"download/"+comic)
            if full is False:
                single_gocomics(comic,path, archive)
            else :
                full_gocomics(comic, path, archive)
        else :
            for name in comic :
                if gocomics_base.has_key(name):
                    control_path(path+"download/"+name)
                    if full is False :
                        single_gocomics(name,path, archive)
                    else :
                        full_gocomics(name, path, archive)
                else :
                    print "La valeur "+name+" est erronee"


def single_gocomics(comic,path, archive):
    comic_file = gocomics_base[comic][1].replace('http://www.gocomics.com/','')
    gocomics(comic, path, comic_file)
    if archive is not False :
        create_archive(comic, path)

def full_gocomics(comic, path, archive):
    date = gocomics_base[comic][2]
    date = dl_rule(path, comic,date)
    if date <= datetime.today():
        url = gocomics_base[comic][1]
        gocomics_all(comic, url, path, date, archive)
        if archive is not False :
            create_archive(comic, path)

def gocomics_all(comic, url, path, first, archive):
    comic_name = gocomics_base[comic][1].replace('http://www.gocomics.com/','')
    first2 = datetime.strftime(first, "%Y/%m/%d")
    first2 = re.findall('(.*)/(.*)/(.*)', first2)[0][0]
    first_year = int(first2)
    last = datetime.today()
    last_year = int(datetime.strftime(last, "%Y"))
    while first_year <= last_year :
        if archive == True:
            tarfile = path+"download/"+comic+"/"+comic+"_"+first2+".tar"
            if os.path.isfile(tarfile):
                os.system("tar -xvf "+tarfile+" -C /")
                os.system("rm "+tarfile)
        first_year += 1
        first2 = str(first_year)
    while first <= last :
        iffile = path+"download/"+comic+"/"+comic_name+"_"+datetime.strftime(first, "%Y_%m_%d")+".gif"
        if os.path.exists(iffile):
            print comic_name+"_"+datetime.strftime(first, "%Y_%m_%d")+".gif"+" a déjà été téléchargé"
        else:
            wget = url+"/"+datetime.strftime(first, "%Y/%m/%d")
            os.system("wget -q -O /tmp/" +comic+" "+wget)
            file = open("/tmp/"+comic,"rb")
            htmlSource = file.read()
            link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
            file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
            if file:
                file = file[0][1].replace('/','_')+".gif"
                if not os.path.isfile(path+"download/"+comic+"/"+file):
                    os.system("wget -q -O " +path+"download/"+comic+"/"+file +" "+link[0])
                    print "Téléchargement de "+file
                    gocomic_crop_image(path+"download/"+comic+"/"+file)
        first = first + timedelta(1)
        dl_rule = path+".dl_rule"
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule, 'r'))
        dl_rules.set(comic, 'date', first)
        dl_rules.write(open(dl_rule,'w'))


def dl_rule(path, comic, date):
    dl_rule = path+".dl_rule"
    if not os.path.isfile(dl_rule):
        file(dl_rule,'w')
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.add_section(comic)
        dl_rule_date = datetime.strptime(date, "%Y/%m/%d")
        dl_rules.set(comic, 'date', dl_rule_date)
        dl_rules.write(open(dl_rule,'w'))
    else :
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule, 'r'))
        if dl_rules.has_section(comic):
            dl_rule_date = datetime.strptime(dl_rules.get(comic, 'date'), "%Y-%m-%d %H:%M:%S")
        else:
            dl_rules.add_section(comic)
            dl_rule_date = datetime.strptime(date, "%Y/%m/%d")
            dl_rules.set(comic, 'date', date)
            dl_rules.write(open(dl_rule,'w'))
    return dl_rule_date

def gocomics(comic,path=None, comic_file=None):
    url =  "%s/" % gocomics_base[comic][0]
    os.system("wget -O /tmp/" +comic_file+" "+url)
    file = open("/tmp/"+comic,"rb")
    htmlSource = file.read()
    link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
    file = file[0][1].replace('/','_')+".gif"
    os.system("wget -q -O " +path+"download/"+comic+"/"+file +" "+link[0])
    print "Téléchargement de "+file
    gocomic_crop_image(path+"download/"+comic+"/"+file)

def gocomic_crop_image(image):
    im = Image.open(image)
    largeur, hauteur = im.size[0], im.size[1]-25
    im = im.crop((0,0,largeur,hauteur))
    im.save(image)

def create_archive(name, path):
    first = gocomics_base[name][2]
    first = re.findall('(.*)/(.*)/(.*)', first)[0][0]
    first_year = int(first)
    last = datetime.today()
    last_year = int(datetime.strftime(last, "%Y"))
    archives = path+"archives/"
    dl_path = path+"download/"
    comic_path = dl_path+name+"/"
    control_path(archives)
    while first_year <= last_year :
        os.system("find "+dl_path+name+"  -name '*"+first+"*' | xargs tar -cvf  "+comic_path+name+"_"+first+".tar")
        if not os.path.exists(archives+name+"/"+name+"_"+first+".tar"):
            control_path(archives+name)
            os.system("ln -s "+comic_path+name+"_"+first+".tar "+archives+name+"/"+name+"_"+first+".tar")
        first_year += 1
        first = str(first_year)
    os.system("rm "+comic_path+"*.gif")


def control_path(path):
    if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename
