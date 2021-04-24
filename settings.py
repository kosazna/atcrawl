# -*- coding: utf-8 -*-

from pathlib import Path
from atcrawl.utilities.funcs import load_user_settings

USER_SETTINGS_FILE = Path.home().joinpath(".atcrawl\\settings.json")
USER_SETTINGS = load_user_settings(USER_SETTINGS_FILE)

CAR_BRANDS = ['Abarth',
              'Acura',
              'Alfa Romeo',
              'Aston Martin',
              'Audi',
              'Autobianchi',
              'Bentley',
              'BMW',
              'Buick',
              'Cadillac',
              'Chevrolet',
              'Chrysler',
              'Citroen',
              'Cupra',
              'Dacia',
              'Daewoo',
              'Daihatsu',
              'DS',
              'Dodge',
              'Ferrari',
              'Fiat',
              'Ford',
              'GMC',
              'Honda',
              'Hummer',
              'Hyundai',
              'Infiniti',
              'Isuzu',
              'Iveco',
              'Jaguar ',
              'Jeep',
              'Kia',
              'Lamborghini',
              'Lada',
              'Lancia',
              'Land Rover',
              'Lexus',
              'Lincoln',
              'Lotus',
              'Maserati',
              'Mazda ',
              'Mercedes',
              'Mercury',
              'Mini',
              'Mitsubishi',
              'Nissan',
              'Opel',
              'Peugeot',
              'Pontiac',
              'Porsche',
              'Ram',
              'Renault',
              'Rover',
              'Saab',
              'Saturn',
              'Scion',
              'Seat',
              'Skoda',
              'Smart',
              'SsangYong',
              'Subaru',
              'Suzuki',
              'Tesla',
              'Toyota',
              'Volkswagen',
              'Volvo',
              'Zastava',
              'Wiesmann']


MANUFACTURES_BRANDS = ['A.B.S.',
                       'ABAKUS',
                       'ABE',
                       'AC ROLCAR',
                       'ACKOJA',
                       'AE',
                       'AFAM',
                       'AIC',
                       'AIRSTAL',
                       'AIRTEX',
                       'AISIN',
                       'AJUSA',
                       'AKS DASIS',
                       'AKUSAN',
                       'AL-KO',
                       'ALANKO',
                       'ALCO FILTER',
                       'ALEX LPG',
                       'ALKAR',
                       'ALLIGATOR',
                       'ALU-SV',
                       'AMC',
                       'AMIO',
                       'AMK AUTOMOTIVE',
                       'AQUAPLUS',
                       'ARIETE',
                       'ARNOTT',
                       'AS-PL',
                       'ASHIKA',
                       'ASMET',
                       'ASPOCK',
                       'ATE',
                       'AUGER',
                       'AUTEX',
                       'AUTLOG',
                       'AUTOFREN SEINSA',
                       'AUTOMEGA',
                       'B CAR',
                       'BANDO',
                       'BARUM',
                       'BE TURBO',
                       'BEHR THERMOT-TRONIK',
                       'BERAL',
                       'BERU',
                       'BF',
                       'BGA',
                       'BILSTEIN',
                       'BIMECC',
                       'BLIC',
                       'BLUE PRINT',
                       'BM CATALYSTS',
                       'BORG & BECK',
                       'BORGWARNER',
                       'BORSEHUNG',
                       'BOSAL',
                       'BOSCH',
                       'BOSS FILTERS',
                       'BOTTO RICAMBI',
                       'BOUGICORD',
                       'BPART',
                       'BPW',
                       'BRC',
                       'BRECK',
                       'BREMBO',
                       'BREMI',
                       'BTA',
                       'BTS TURBO',
                       'BUDWEG CALIPER',
                       'BUGIAD',
                       'CAFFARO',
                       'CALORSTAT BY VERNET',
                       'CAMPRO',
                       'CAR',
                       'CARTECHNIC',
                       'CASCO',
                       'CEI',
                       'CENTAURO',
                       'CENTRA',
                       'CERTOOLS',
                       'CHAMPION',
                       'CIFAM',
                       'CLEAN FILTER',
                       'COFLE',
                       'CONTINENTAL',
                       'CONTITECH',
                       'CONTITECH AIR SPRING',
                       'CORTECO',
                       'COVIND',
                       'CS GERMANY',
                       'CTR',
                       'CV PSH',
                       'CX',
                       'CZM',
                       'DACO GERMANY',
                       'DAKATEC',
                       'DANBLOCK',
                       'DAYCO',
                       'DELCO REMY',
                       'DELPHI',
                       'DENCKERMANN',
                       'DENSO',
                       'DID',
                       'DIEDERICHS',
                       'DINEX',
                       'DOLZ',
                       'DONALDSON',
                       'DPA',
                       'DR!VE+',
                       'DR.MOTOR AUTOMOTIVE',
                       'DRI',
                       'DT',
                       'DUNLOP',
                       'DYS',
                       'EAI',
                       'EBC BRAKES',
                       'EBERSPÄCHER',
                       'ECS',
                       'EIBACH',
                       'ELECTRIC LIFE',
                       'ELPIGAZ',
                       'ELRING',
                       'ELSTOCK',
                       'ELWIS ROYAL',
                       'EMPEX',
                       'ENERGIZER',
                       'ENGITECH',
                       'EPS',
                       'ERA',
                       'ERA BENELUX',
                       'ERNST',
                       'ERT',
                       'ESEN SKV',
                       'ET ENGINETEAM',
                       'EUROPEGAS',
                       'EURORICAMBI',
                       'EUROTEC',
                       'EXEDY',
                       'EXIDE',
                       'FA1',
                       'FACET',
                       'FAE',
                       'FAG',
                       'FAGUMIT',
                       'FAI AUTOPARTS',
                       'FAST',
                       'FEBEST',
                       'FEBI BILSTEIN',
                       'FERODO',
                       'FERODO RACING',
                       'FERSA BEARINGS',
                       'FILTRON',
                       'FISPA',
                       'FLENNOR',
                       'FORTUNE LINE',
                       'FRAM',
                       'FRECCIA',
                       'FREMAX',
                       'FRENKIT',
                       'FRIGAIR',
                       'FTE',
                       'GABRIEL',
                       'GALFER',
                       'GARRETT',
                       'GATES',
                       'GE',
                       'GENERAL RICAMBI',
                       'GIANT',
                       'GK',
                       'GLASER',
                       'GLYCO',
                       'GOETZE',
                       'GOETZE ENGINE',
                       'GOMET',
                       'GRAF',
                       'GSP',
                       'GUARNITAUTO',
                       'H&R',
                       'HALDEX',
                       'HASTINGS PISTON RING',
                       'HC-CARGO',
                       'HELLA',
                       'HELLA GUTMANN',
                       'HENGST FILTER',
                       'HENKEL PARTS',
                       'HEPU',
                       'HERTH+BUSS ELPARTS',
                       'HERTH+BUSS JAKOPARTS',
                       'HIDRIA',
                       'HIFLOFILTRO',
                       'HITACHI',
                       'HJS',
                       'HOLSET',
                       'HORPOL',
                       'HS',
                       'HUF',
                       'HUTCHINSON',
                       'IBRAS',
                       'ICER',
                       'IJS GROUP',
                       'IMASAF',
                       'INA',
                       'INGREMIO',
                       'INTERVALVES',
                       'IPD',
                       'IPSA',
                       'IZAWIT',
                       'IZI',
                       'JAEGER',
                       'JAGUAR',
                       'JANMOR',
                       'JAPANPARTS',
                       'JAPKO',
                       'JC PREMIUM',
                       'JMJ',
                       'JOHNS',
                       'JOST',
                       'JP GROUP',
                       'JTSPROCKETS',
                       'JURID',
                       'K&N FILTERS',
                       'KAMAR',
                       'KAMOKA',
                       'KANACO',
                       'KAVO PARTS',
                       'KAWE',
                       'KILEN',
                       'KLAXCAR FRANCE',
                       'KLOKKERHOLM',
                       'KME',
                       'KNECHT',
                       'KNORR-BREMSE',
                       'KOLBENSCHMIDT',
                       'KONI',
                       'KS TOOLS',
                       'KW',
                       'KYB',
                       'LAND ROVER',
                       'LANDI RENZO',
                       'LAUBER',
                       'LEMA',
                       'LEMFÖRDER',
                       'LESJÖFORS',
                       'LIFT-TEK',
                       'LINEX',
                       'LIZARTE',
                       'LKQ',
                       'LOVATO',
                       'LPGTECH',
                       'LPR',
                       'LRT',
                       'LUCAS',
                       'LUCAS DIESEL',
                       'LUCAS ELECTRICAL',
                       'LUK',
                       'LUMAG',
                       'LÖBRO',
                       'M-TECH',
                       'MAGNETI MARELLI',
                       'MAGNUM TECHNOLOGY',
                       'MAHLE ORIGINAL',
                       'MALÒ',
                       'MANN-FILTER',
                       'MAPCO',
                       'MASTER-SPORT',
                       'MAXGEAR',
                       'MEAT & DORIA',
                       'MECARM',
                       'MEKRA',
                       'MERITOR',
                       'MESSMER',
                       'METALCAUCHO',
                       'METELLI',
                       'METZGER',
                       'MEYER MOTOREN',
                       'MEYLE',
                       'MIRAGLIO',
                       'MOBILETRON',
                       'MONROE',
                       'MOOG',
                       'MOTAIR',
                       'MOTIVE',
                       'MOTO-PRESS',
                       'MOTORAD',
                       'MPBS',
                       'MTS',
                       'MULLER FILTER',
                       'NAP CLEANAIR',
                       'NARVA',
                       'NE',
                       'NEOLUX®',
                       'NEOTEC',
                       'NEXUS',
                       'NG',
                       'NGK',
                       'NHC',
                       'NIPPARTS',
                       'NISSENS',
                       'NK',
                       'NRF',
                       'NWB',
                       'NÜRAL',
                       'OBERLAND',
                       'OCAP',
                       'OPTIBELT',
                       'OPTIMAL',
                       'ORIGINAL IMPERIUM',
                       'OSRAM',
                       'OSSCA',
                       'OSVAT',
                       'OXIMO',
                       'PACOL',
                       'PASCAL',
                       'PAYEN',
                       'PEDOL',
                       'PETERS ENNEPETAL',
                       'PEX',
                       'PHILIPS',
                       'PHOENIX',
                       'PIERBURG',
                       'PLANET TECH',
                       'PNEUMATICS',
                       'POINT GEAR',
                       'POLMO',
                       'POLMO S.A.',
                       'POWER TRUCK',
                       'POWERFLEX',
                       'PRASCO',
                       'PRESTOLITE ELECTRIC',
                       'PRINS',
                       'PROAKCESS',
                       'PROFIT',
                       'PROKOM',
                       'PROPLAST',
                       'PROTECHNIC',
                       'PURFLUX',
                       'QUARO',
                       'QUICK BRAKE',
                       'RAPRO',
                       'REINHOCH',
                       'REINZ',
                       'REMSA',
                       'RIDEX',
                       'RIDEX REMAN',
                       'RK',
                       'RMS',
                       'ROADHOUSE',
                       'ROTINGER',
                       'ROTOVIS AUTOMOTIVE ELECTRICS',
                       'RTC TECHNICTURBOCHARGER',
                       'RTS',
                       'RUD',
                       'RUVILLE',
                       'RYMEC',
                       'RYWAL',
                       'S-TR',
                       'SACHS',
                       'SACHS PERFORMANCE',
                       'SAF',
                       'SAINT-GOBAIN',
                       'SALERI SIL',
                       'SASIC',
                       'SBP',
                       'SBS',
                       'SCHLÜTTER TURBOLADER',
                       'SCHRADER',
                       'SEALEY',
                       'SEIM',
                       'SIDAT',
                       'SIDEM',
                       'SIEGEL AUTOMOTIVE',
                       'SKF',
                       'SNR',
                       'SOGEFIPRO',
                       'SPIDAN',
                       'SPIDAN CHASSIS PARTS',
                       'SPJ',
                       'STABILUS',
                       'STARDAX',
                       'STARK',
                       'STATIM',
                       'STC',
                       'SUNSTAR',
                       'SUPLEX',
                       'SWAG',
                       'SWF',
                       'TAB',
                       'TCCI',
                       'TEAMEC',
                       'TEDGUM',
                       'TEKNOROT',
                       'TESLA',
                       'TEXTAR',
                       'THE NEWLINE',
                       'THERMOTEC',
                       'TOMASETTO',
                       'TOMEX BRAKES',
                       'TOPRAN',
                       'TRICLO',
                       'TRISCAN',
                       'TRUCKLIGHT',
                       'TRUCKLINE',
                       'TRUCKTEC AUTOMOTIVE',
                       'TRUCKTECHNIC',
                       'TRW',
                       'TRW ENGINE COMPONENT',
                       'TURBO MOTOR',
                       'TURBORAIL',
                       'TURBO´S HOET',
                       'TWINTEC',
                       'TYC',
                       'UFI',
                       'ULO',
                       'UNIPOINT',
                       'VADEN',
                       'VAICO',
                       'VALEO',
                       'VALTEK',
                       'VAN WEZEL',
                       'VANSTAR',
                       'VARTA',
                       'VDO',
                       'VEGAZ',
                       'VEMO',
                       'VICMA',
                       'VIGNAL',
                       'VIKA',
                       'WABCO',
                       'WAECO',
                       'WAHLER',
                       'WAI',
                       'WALKER',
                       'WEBASTO',
                       'WESTFALIA',
                       'WONDER',
                       'YAMATO',
                       'YAZUKA',
                       'YUASA',
                       'ZF GETRIEBE',
                       'ZF LENKSYSTEME',
                       'ZF PARTS',
                       'ZIMMERMANN',
                       '3K',
                       '3RG',
                       '555']
