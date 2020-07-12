from collections import OrderedDict

from ..en import Provider as AddressProvider


class Provider(AddressProvider):
    city_prefixes = ('North', 'East', 'West', 'South', 'New', 'Lake', 'Port')
    city_suffixes = (
        'town',
        'ton',
        'land',
        'ville',
        'berg',
        'burgh',
        'borough',
        'bury',
        'view',
        'port',
        'mouth',
        'stad',
        'furt',
        'chester',
        'mouth',
        'fort',
        'haven',
        'side',
        'shire',
    )
    counties = (
        'Bedfordshire',
        'Buckinghamshire',
        'Cambridgeshire',
        'Cheshire',
        'Cleveland',
        'Cornwall',
        'Cumbria',
        'Derbyshire',
        'Devon',
        'Dorset',
        'Durham',
        'East Sussex',
        'Essex',
        'Gloucestershire',
        'Greater London',
        'Greater Manchester',
        'Hampshire',
        'Hertfordshire',
        'Kent',
        'Lancashire',
        'Leicestershire',
        'Lincolnshire',
        'Merseyside',
        'Norfolk',
        'North Yorkshire',
        'Northamptonshire',
        'Northumberland',
        'Nottinghamshire',
        'Oxfordshire',
        'Shropshire',
        'Somerset',
        'South Yorkshire',
        'Staffordshire',
        'Suffolk',
        'Surrey',
        'Tyne and Wear',
        'Warwickshire',
        'West Berkshire',
        'West Midlands',
        'West Sussex',
        'West Yorkshire',
        'Wiltshire',
        'Worcestershire',
        'Flintshire',
        'Glamorgan',
        'Merionethshire',
        'Monmouthshire',
        'Montgomeryshire',
        'Pembrokeshire',
        'Radnorshire',
        'Anglesey',
        'Breconshire',
        'Caernarvonshire',
        'Cardiganshire',
        'Carmarthenshire',
        'Denbighshire',
        'Aberdeen City',
        'Aberdeenshire',
        'Angus',
        'Argyll and Bute',
        'City of Edinburgh',
        'Clackmannanshire',
        'Dumfries and Galloway',
        'Dundee City',
        'East Ayrshire',
        'East Dunbartonshire',
        'East Lothian',
        'East Renfrewshire',
        'Eilean Siar',
        'Falkirk',
        'Fife',
        'Glasgow City',
        'Highland',
        'Inverclyde',
        'Midlothian',
        'Moray',
        'North Ayrshire',
        'North Lanarkshire',
        'Orkney Islands',
        'Perth and Kinross',
        'Renfrewshire',
        'Scottish Borders',
        'Shetland Islands',
        'South Ayrshire',
        'South Lanarkshire',
        'Stirling',
        'West Dunbartonshire',
        'West Lothian',
        'Antrim',
        'Armagh',
        'Down',
        'Fermanagh',
        'Derry and Londonderry',
        'Tyrone',
    )
    building_number_formats = ('#', '##', '###')
    street_suffixes = (
        'alley',
        'avenue',
        'branch',
        'bridge',
        'brook',
        'brooks',
        'burg',
        'burgs',
        'bypass',
        'camp',
        'canyon',
        'cape',
        'causeway',
        'center',
        'centers',
        'circle',
        'circles',
        'cliff',
        'cliffs',
        'club',
        'common',
        'corner',
        'corners',
        'course',
        'court',
        'courts',
        'cove',
        'coves',
        'creek',
        'crescent',
        'crest',
        'crossing',
        'crossroad',
        'curve',
        'dale',
        'dam',
        'divide',
        'drive',
        'drive',
        'drives',
        'estate',
        'estates',
        'expressway',
        'extension',
        'extensions',
        'fall',
        'falls',
        'ferry',
        'field',
        'fields',
        'flat',
        'flats',
        'ford',
        'fords',
        'forest',
        'forge',
        'forges',
        'fork',
        'forks',
        'fort',
        'freeway',
        'garden',
        'gardens',
        'gateway',
        'glen',
        'glens',
        'green',
        'greens',
        'grove',
        'groves',
        'harbor',
        'harbors',
        'haven',
        'heights',
        'highway',
        'hill',
        'hills',
        'hollow',
        'inlet',
        'inlet',
        'island',
        'island',
        'islands',
        'islands',
        'isle',
        'isle',
        'junction',
        'junctions',
        'key',
        'keys',
        'knoll',
        'knolls',
        'lake',
        'lakes',
        'land',
        'landing',
        'lane',
        'light',
        'lights',
        'loaf',
        'lock',
        'locks',
        'locks',
        'lodge',
        'lodge',
        'loop',
        'mall',
        'manor',
        'manors',
        'meadow',
        'meadows',
        'mews',
        'mill',
        'mills',
        'mission',
        'mission',
        'motorway',
        'mount',
        'mountain',
        'mountain',
        'mountains',
        'mountains',
        'neck',
        'orchard',
        'oval',
        'overpass',
        'park',
        'parks',
        'parkway',
        'parkways',
        'pass',
        'passage',
        'path',
        'pike',
        'pine',
        'pines',
        'place',
        'plain',
        'plains',
        'plains',
        'plaza',
        'plaza',
        'point',
        'points',
        'port',
        'port',
        'ports',
        'ports',
        'prairie',
        'prairie',
        'radial',
        'ramp',
        'ranch',
        'rapid',
        'rapids',
        'rest',
        'ridge',
        'ridges',
        'river',
        'road',
        'road',
        'roads',
        'roads',
        'route',
        'row',
        'rue',
        'run',
        'shoal',
        'shoals',
        'shore',
        'shores',
        'skyway',
        'spring',
        'springs',
        'springs',
        'spur',
        'spurs',
        'square',
        'square',
        'squares',
        'squares',
        'station',
        'station',
        'stravenue',
        'stravenue',
        'stream',
        'stream',
        'street',
        'street',
        'streets',
        'summit',
        'summit',
        'terrace',
        'throughway',
        'trace',
        'track',
        'trafficway',
        'trail',
        'trail',
        'tunnel',
        'tunnel',
        'turnpike',
        'turnpike',
        'underpass',
        'union',
        'unions',
        'valley',
        'valleys',
        'via',
        'viaduct',
        'view',
        'views',
        'village',
        'village',
        'villages',
        'ville',
        'vista',
        'vista',
        'walk',
        'walks',
        'wall',
        'way',
        'ways',
        'well',
        'wells')

    POSTAL_ZONES = (
        'AB', 'AL', 'B', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR',
        'BS', 'BT', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT',
        'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
        'DY', 'E', 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G', 'GL',
        'GY', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HS', 'HU', 'HX',
        'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L',
        'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M', 'ME', 'MK',
        'ML', 'N', 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX',
        'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S',
        'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR',
        'SS', 'ST', 'SW', 'SY', 'TA', 'TD', 'TF', 'TN', 'TQ', 'TR',
        'TS', 'TW', 'UB', 'W', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
        'WS', 'WV', 'YO', 'ZE',
    )

    POSTAL_ZONES_ONE_CHAR = [zone for zone in POSTAL_ZONES if len(zone) == 1]
    POSTAL_ZONES_TWO_CHARS = [zone for zone in POSTAL_ZONES if len(zone) == 2]

    postcode_formats = (
        'AN NEE',
        'ANN NEE',
        'PN NEE',
        'PNN NEE',
        'ANC NEE',
        'PND NEE',
    )

    _postcode_sets = OrderedDict((
        (' ', ' '),
        ('N', [str(i) for i in range(0, 10)]),
        ('A', POSTAL_ZONES_ONE_CHAR),
        ('B', 'ABCDEFGHKLMNOPQRSTUVWXY'),
        ('C', 'ABCDEFGHJKSTUW'),
        ('D', 'ABEHMNPRVWXY'),
        ('E', 'ABDEFGHJLNPQRSTUWXYZ'),
        ('P', POSTAL_ZONES_TWO_CHARS),
    ))

    city_formats = (
        '{{city_prefix}} {{first_name}}{{city_suffix}}',
        '{{city_prefix}} {{first_name}}',
        '{{first_name}}{{city_suffix}}',
        '{{last_name}}{{city_suffix}}',
    )
    street_name_formats = (
        '{{first_name}} {{street_suffix}}',
        '{{last_name}} {{street_suffix}}',
    )
    street_address_formats = (
        '{{building_number}} {{street_name}}',
        '{{secondary_address}}\n{{street_name}}',
    )
    address_formats = (
        "{{street_address}}\n{{city}}\n{{postcode}}",
    )
    secondary_address_formats = (
        'Flat #', 'Flat ##', 'Flat ##?', 'Studio #', 'Studio ##', 'Studio ##?')

    def postcode(self):
        """
        See
        http://web.archive.org/web/20090930140939/http://www.govtalk.gov.uk/gdsc/html/noframes/PostCode-2-1-Release.htm
        """
        postcode = ''
        pattern = self.random_element(self.postcode_formats)
        for placeholder in pattern:
            postcode += self.random_element(self._postcode_sets[placeholder])
        return postcode

    def city_prefix(self):
        return self.random_element(self.city_prefixes)

    def secondary_address(self):
        return self.bothify(self.random_element(self.secondary_address_formats))

    def county(self):
        return self.random_element(self.counties)