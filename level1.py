import random, sys, pygame

number_of_variables = 2
# the minimum possible value x or y can take
min_value = 40
# the maximum possible value x or y can take
max_value = 760
# the number of particles in the swarm
number_of_particles = 40

w = 0.729    # inertia
c1 = 1.49 # cognitive (particle)
c2 = 1.49 # social (swarm)


pygame.init()
display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Shaggy PSO')
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
antImg = pygame.image.load('ant.png')
antImg = pygame.transform.scale(antImg, (35, 40))
def drawAnt(x,y):
    gameDisplay.blit(antImg, (x,y))

class Particle:

    def __init__(self, number_of_variables, min_value, max_value):

        # init x and y values
        self.positions = [0.0 for v in range(number_of_variables)]
        # init velocities of x and y
        self.velocities = [0.0 for v in range(number_of_variables)]

        for v in range(number_of_variables):
            # update x and y positions
            self.positions[v] = ((max_value - min_value) * random.random()
                                + min_value)
            # update x and y velocities
            self.velocities[v] = ((max_value - min_value) * random.random()
                                + min_value)

        # current fitness after updating the x and y values
        self.fitness = 0
        # the current particle positions as the best fitness found yet
        self.best_particle_positions = list(self.positions)
        # the current particle fitness as the best fitness found yet
        self.best_particle_fitness = self.fitness



class swarmObj(object):

    def __init__(self,number_of_variables,min_value,max_value,number_of_particles):
        self.number_of_variables = number_of_variables
        self.min_value = min_value
        self.max_value = max_value
        self.number_of_particles = number_of_particles
        self.swarm = [Particle(self.number_of_variables,self.min_value, self.max_value)
                            for __x in range(self.number_of_particles)]
        self.best_swarm_positions = [0.0 for v in range(self.number_of_variables)]
        self.best_swarm_fitness = sys.float_info.max
        self.w = 0.7 # inertia
        self.c1 = 1.5  # cognitive (particle)
        self.c2 = 1.5  # social (swarm)
        self.cursour_x = 300
        self.cursour_y = 300
        self.lastup = 0
        self.exploration = 0
        self.updateF()
        self.updateBest()

    def calculate_new_velocity_value(self,particle, v):

        if(random.randint(0,10)>=8):
            return random.randint(-10,10)
        self.exploration = self.exploration-1
        # generate random numbers
        r1 = random.random()
        r2 = random.random()

        if(self.exploration>=0):
            return (particle.best_particle_positions[v] - particle.positions[v])

        # the learning rate part

        part_1 = (self.w * particle.velocities[v])
        # the cognitive part - learning from itself

        part_2 = (self.c1 * r1 * (particle.best_particle_positions[v] - particle.positions[v]))
        # the social part - learning from others

        part_3 = (self.c2 * r2 * (self.best_swarm_positions[v] - particle.positions[v]))

        div = self.w+self.c1 * r1+self.c2 * r2
        new_velocity = (part_1 + part_2 + part_3)/div

        return new_velocity

    def initBest(self):
        self.best_swarm_positions = [0.0 for v in range(self.number_of_variables)]
        self.best_swarm_fitness = sys.float_info.max
        for particle in self.swarm:
            self.exploration = 50
            particle.fitness = self.Fitness(particle.positions)
            particle.velocities = [random.randint(-10,5),random.randint(5,10)]
            particle.best_particle_positions = [random.randint(80,720),random.randint(80,720)]
            particle.best_particle_fitness= self.Fitness(particle.best_particle_positions)
        self.updateBest()

    def init2(self):

        for particle in self.swarm:
            particle.best_particle_positions = [particle.positions[0]+random.choice([1,-1])*random.randint(50,250),
                                                particle.positions[0]+random.choice([1,-1])*random.randint(50,250)]
            particle.best_particle_fitness= self.Fitness(particle.best_particle_positions)
        self.updateBest()


    def Fitness(self,positions):
        #return math.sqrt((self.cursour_x - positions[0])**2 + (self.cursour_y - positions[1])**2)
        return (abs(self.cursour_x - positions[0]) + abs(self.cursour_y - positions[1]))

    def updateBest(self):
        for particle in self.swarm:  # check each particle
            if particle.fitness - self.best_swarm_fitness<-0.5:
                self.lastup = 0
                self.best_swarm_fitness = particle.fitness
                self.best_swarm_positions = list(particle.positions)
        self.lastup+=1
        if(self.lastup>20):
            self.lastup =0
            self.exploration = 40
            self.init2()
        print(self.lastup)

    def updateV(self):
        for particle in self.swarm:
            #print(particle.velocities)
            for v in range(self.number_of_variables):
                particle.velocities[v] = self.calculate_new_velocity_value(particle, v)
                if particle.velocities[v] < -10:
                    particle.velocities[v] = -10
                elif particle.velocities[v] > 10:
                    particle.velocities[v] = 10
            #print(particle.velocities)

    def updateP(self):
        for particle in self.swarm:
            for v in range(self.number_of_variables):
                particle.positions[v] += particle.velocities[v]

                if particle.positions[v] < min_value:
                    particle.positions[v] = min_value
                elif particle.positions[v] > max_value:
                    particle.positions[v] = max_value

    def updateF(self):
        for particle in self.swarm:
            particle.fitness = self.Fitness(particle.positions)
            # are the new positions a new best for the particle?
            if particle.fitness < particle.best_particle_fitness:
                particle.best_particle_fitness = particle.fitness
                particle.best_particle_positions = list(particle.positions)

    def updateC(self,x,y):
        self.cursour_x = x
        self.cursour_y = y


def loopMain(swarm):
    run = True

    for p in swarm.swarm:
        drawAnt(p.positions[0], p.positions[1])
        print(p.positions[0], p.positions[1], p.fitness)
    print(swarm.best_swarm_fitness)
    print(swarm.best_swarm_positions)

    while (run):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
               run = False

            if (event.type == pygame.MOUSEMOTION):
                x, y = pygame.mouse.get_pos()
                swarm.updateC(x,y)
                swarm.initBest()

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, (0,255,0), (swarm.cursour_x, swarm.cursour_y, 100, 100), 2)
        swarm.updateV()
        swarm.updateP()
        swarm.updateF()
        swarm.updateBest()
        for p in swarm.swarm:
            drawAnt(p.positions[0],p.positions[1])
        print(swarm.best_swarm_fitness)
        print(swarm.best_swarm_positions)
        print(swarm.cursour_x,swarm.cursour_y)
        pygame.display.update()
        clock.tick(15)
    pygame.quit()
    quit()

if(__name__=="__main__"):
    loopMain(swarmObj(number_of_variables,min_value,max_value,number_of_particles))
