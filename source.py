import os
import random
import pickle
import time

import pygame
import neat

pygame.init()
pygame.font.init()

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
GEN = -1
IS_GEN = True

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def load_image(filename):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("flappy-bird", "img", filename)))

def load_sound(filename, volume):
    sound = pygame.mixer.Sound(os.path.join("flappy-bird", filename))
    sound.set_volume(volume)
    return sound

# Loading Assets
BIRD_IMGS = [load_image(f"bird{i}.png") for i in range(1, 4)]
PIPE_IMG = load_image("pipe.png")
BASE_IMG = load_image("base.png")
BGR_IMG = load_image("bg.png")

STAT_FONT = pygame.font.SysFont("comicsans", 20)

HIT_SFX = load_sound("hit.mp3", 0.05)
POINT_SFX = load_sound("point.mp3", 0.05)
VICTORY_SFX = load_sound("victory.mp3", 0.1)

def show_loading_screen(win):
    '''Display the loading Screen with a progress bar and messages.'''
    start_time = time.time()
    loading_bar_width = 400
    loading_bar_height = 20
    bar_x = (WINDOW_WIDTH - loading_bar_width) / 2
    bar_y = (WINDOW_HEIGHT - loading_bar_height) / 2

    messages = ["Fetching Data...", "Designing the bird...", "Setting up a new World..."]
    message_index = 0
    message_change_time = 2

    while time.time() - start_time < 6:  # Show loading screen for 6 seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        elapsed_time = time.time() - start_time
        if elapsed_time > message_change_time * (message_index + 1):
            message_index = (message_index + 1) % len(messages)  # Cycle through messages

        win.blit(BGR_IMG, (0,0))
        pygame.draw.rect(win, BLACK, (bar_x, bar_y, loading_bar_width, loading_bar_height), 2, 10)  # Border of the bar
        pygame.draw.rect(win, GREEN, (bar_x + 2, bar_y + 2, (time.time() - start_time) / 6 * (loading_bar_width - 4), loading_bar_height - 4), 0, 10)  # Filled part
        
        text = STAT_FONT.render(messages[message_index], True, BLACK)
        win.blit(text, ((WINDOW_WIDTH - text.get_width()) / 2, bar_y - text.get_height() - 10))
        pygame.display.update()

# Bird Class

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25       # tells the direction of the face of the bird
    ROTATION_VEL = 20       # tells the velocity of the bird
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        ''' Making the bird jump'''
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        '''Update bird's position on its velocity and tilt'''
        self.tick_count += 1
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2  #s = ut + 1/2 a t^2 -> assuming a = 3

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y <self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, win):
        '''Draw the bird on the Window'''
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        '''Get the mask vital for collision detections'''
        return pygame.mask.from_surface(self.img)

# Pipe Class

class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        '''Setting up the height of the top and the bottom pipes'''
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        ''' Moving the pipes here'''
        self.x -= self.VELOCITY

    def draw(self, win):
        '''Drawing the window here'''
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird) -> bool:
        '''Collision Detection Method'''
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

# Base Class

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        '''Movement of the base is managed here'''
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        '''Drawing the base '''
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

# Drawing and plaing all the elements together in the window

def draw_window(win, birds, pipes, base, score, gen, isgen, alive):
    '''Drawing the window here'''
    win.blit(BGR_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    if isgen:
        text = STAT_FONT.render("Gen: " + str(gen), 1, (0, 0, 0))
    else:
        text = STAT_FONT.render("Gen: -", 1, (0, 0, 0))

    win.blit(text, (10, 10))

    text = STAT_FONT.render('Alive: ' + str(alive), 1, (0, 0, 0))
    win.blit(text, (10, 50))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

# The main function that helps to find the best generation of the birds that can survive the entire game 

def main(genomes, config):

    global GEN
    GEN += 1
    nets = []
    birds = []
    ge = []

    for genID, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)

        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]

    ALIVE = len(birds)
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    run = True
    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Movements of the pipes are managed here

        pipe_ind = 0
        for i, pipe in enumerate(pipes):
            if len(birds) > 0 :
                if len(pipes) > 0 and birds[0].x < pipe.x + pipe.PIPE_TOP.get_width():
                    pipe_ind = i
                    break
            else:
                run = False
                break

        # The output conditions are mentioned here

        for x, bird in enumerate(birds):
            bird.move()
            if not pipe.collide(bird):
                ge[x].fitness += 0.1

            output  = nets[x].activate((bird.y , abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        removed = []
        add_pipe = False

        for pipe in pipes:
            for x, bird in enumerate(birds):

                if pipe.collide(bird):      # The colliding conditions are managed here

                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    ALIVE = len(birds)

                    HIT_SFX.play()

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            POINT_SFX.play()
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for curr in removed:
            removed.remove(curr)

        # Conditions if the bird touches the bottom floor or passes the topmost surface

        for x, bird in enumerate(birds):  
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                HIT_SFX.play()
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                ALIVE = len(birds)

        if score >= 15:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GEN, IS_GEN, ALIVE)


def run_game(winner, config):
    #This function runs the single perfect bird that can complete the game

    IS_GEN = False
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    run = True
    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_ind = 0

        for i, pipe in enumerate(pipes):
            if len(pipes) > 1 and bird.x < pipe.x + pipe.PIPE_TOP.get_width():
                pipe_ind = i
                break

        bird.move()
        output = net.activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

        if output[0] > 0.5:
            bird.jump()

        removed = []
        add_pipe = False

        for pipe in pipes:
            if pipe.collide(bird):
                HIT_SFX.play()
                print(f"Game Over! Final Score : {score}")
                pygame.quit()
                quit()
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe =True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed.append(pipe)
            
            pipe.move()

        if add_pipe:
            score += 1

            if score == 10:
                VICTORY_SFX.play()
            else:
                POINT_SFX.play()
            
            pipes.append(Pipe(600))

        for curr in removed:
            removed.remove(curr)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            HIT_SFX.play()
            print(f"Game Over! Final Socre : {score}")
            pygame.quit()
            quit()

        if score > 10:
            print(f"Success! Reached score of {score}")
            pygame.quit()
            quit()

        base.move()
        draw_window(win, [bird], pipes, base, score, GEN, IS_GEN, 1)

def run(config_path):
    '''Run the NEAT algorithm to find the best configuration'''
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()   
    p.add_reporter(stats)

    winner = p.run(main, 50)
    local_path = os.path.dirname(__file__)
    path = os.path.join(local_path, "winning.pkl")
    with open(path, "wb") as f:
        pickle.dump(winner, f)

    with open(path, 'rb') as f:
        winner = pickle.load(f)
    
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    show_loading_screen(win)

    run_game(winner, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)