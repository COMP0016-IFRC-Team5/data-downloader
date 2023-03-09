__all__ = ['ALL_SUBTYPES']

FLOODS = ['flood', 'flash food', 'inundación', 'inondation', 'rain.csv',
          'rains.csv', 'heavy rain', 'strong rain', 'pluies extreme',
          'freezing rain', 'torrential rain', 'surge', 'tsunami', 'cloudburst',
          'rain out of saison', 'raudal.csv', 'rough seas', 'spate.csv',
          'tidal wave', 'torrent.csv', 'oleaje.csv', 'high tide', 'high waves',
          'litoral', 'corriente de resaca']

STORM_TYPOS = ['hail', 'strom', 'stond', 'strm', 'windtorm', 'tondering.csv']

STORMS = STORM_TYPOS + \
         ['storm', 'tormenta', 'tempête', 'gale', 'heavy wind', 'strong wind',
          'high wind', 'cyclone', 'hurricane', 'ouragan', 'typhoon', 'tornado',
          'severe colds', 'snow.csv', 'snowfall.csv', 'thunder lighting stroke',
          'thunder.csv', 'wind.csv', 'аянга.csv', 'cold.csv', "lightning.csv",
          'lightening.csv', 'foudre.csv', 'lighting', 'electrocution.csv']

EARTHQUAKES = ['earthquake', 'tremblement de terre', 'earth tremors',
              'ground vibratio']

LANDSLIDES = ['landslide', 'mudslide', 'rock slide', 'earth slip', 'rock fall',
             'rock+boulder slide']

GEOHAZARDS = ['wetland loss+degradation', 'flujo', 'mud volcano', 'collapse',
              'sedimentation.csv', 'avalanche.csv', 'land degradation', 'lahar',
              'hundimiento', 'colapso estructural', 'deslizamiento.csv',
              'desprendimiento de techo', 'volcano']

DROUGHTS = ['drought', 'dry spell', 'déficit hídrico', 'draught.csv']

# define other cates
ANIMALS = ['animal', 'fauna', 'bird', 'hippo', 'shark', 'elephant', 'snake',
           'rat.csv', 'rodent']

ACCIDENTS = ['intervention en mer', 'accident', 'accednts',
             'siniestros de tránsito', 'crash',
             'road', 'aircraft', 'building', 'boat', 'drown', 'sudden death',
             'socavamiento.csv', 'structure.csv', 'subsidence.csv',
             'trapped in a petrol tanker', 'tripped into a well', 'sinking.csv',
             'tree fallen', 'бичил уурхай нурангины осол', 'noyade.csv',
             'ahogado.csv', 'naufrage', 'ahogamiento', 'arbol caido',
             'caída de arbol', 'muerte por inmersión', 'maritime disaster',
             'failen trees', 'into a well']

INSECTS = ['insect', 'bug', 'pest', 'locust', 'worm', 'beetle', 'slug',
           'chenille', 'vermin infestation']

FIRES = ['fire', 'incendio', 'хээрийн түймэр', 'feux']

DISEASES = ['geomedical', 'intoxica', 'disease', 'virus', 'epidemic', 'fever',
            'epizootia', 'epizootie', 'epizooty', 'measle', 'meningitis',
            'cholera', 'fowl smallpox', 'tuberclosis', 'depress', 'plague',
            'malnutrition']

CHEMICALS = ['chemical', 'oil', 'spill', 'leak', 'aflatoxin', 'poisoning',
             'intoxicación', 'ozono', 'pollution', 'contamination', 'fuel',
             'fume', 'explosion', 'explosión', 'explotion', 'erosion',
             'erosión', 'erossion', 'eruption', 'materiales peligrosos']

SOCIETAL = ['food insecurity', 'hambruna', 'violence', 'conflict', 'war',
            'social unrest', 'panic', 'conmoción social', 'crime', 'rape',
            'robbery', 'civil', 'gun shot', 'suicide', 'terror', 'projectile',
            'pipeline vandalism', 'amenaza de bomba.csv', 'industrial disaster',
            'hunger+famine', 'famine']

TEMPERATURES = ['cold wave', 'vague de froid', 'onda fría', 'ola de frio',
                'ola de frío', 'heat wave', 'vague de chaleur',
                'extreme temperature', 'frost']

UNIDENTIFIED = ['w.csv']

ALL_SUBTYPES = {"FLOODS": FLOODS,
                "STORMS": STORMS,
                "EARTHQUAKES": EARTHQUAKES,
                "LANDSLIDES": LANDSLIDES,
                "GEOHAZARDS": GEOHAZARDS,
                "DROUGHTS": DROUGHTS,
                "ANIMALS": ANIMALS,
                "ACCIDENTS": ACCIDENTS,
                "INSECTS": INSECTS,
                "FIRES": FIRES,
                "DISEASES": DISEASES,
                "CHEMICALS": CHEMICALS,
                "SOCIETAL": SOCIETAL,
                "TEMPERATURES": TEMPERATURES,
                "UNIDENTIFIED": UNIDENTIFIED}
