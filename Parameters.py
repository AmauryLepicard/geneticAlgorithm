# display parameters
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
BORDER_SIZE = 200

# asteroidsGroup parameters
ASTEROID_NUMBER = 10
ASTEROID_MAX_SPEED = 0.2
ASTEROID_MIN_MASS = 100000

ENABLE_ASTEROID_COLLISION = False
USE_IRREGULAR_POLYGONS = False

# ship parameters
SHIP_USING_NEURAL_NETWORK = True
SHIP_DRAG_COEFF = 0.95
SHIP_ACCELERATION = 0.001
SHIP_TURN_RATE = 0.005
SHIP_SIZE = 30
SHIP_FIRING_RATE = 250  # 500ms delay between shots

SHIP_USE_MOUSE = False

GA_USE_PROCESSES = False
GA_MUTATION_CHANCE = 0.02
GA_MUTATION_AMPLITUDE = 0.05
GA_BEST_RATIO = 0.2
GA_USE_ROULETTE_WHEEL = False
GA_ALLOW_MULTISELECT = True
GA_NUMBER_RUNS = 5
GA_SHOW_BESTPLAYER_GAME = False
