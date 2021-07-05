import sys
import time
from random import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cbook import index_of
from pylab import *
from simanneal import Annealer

# tes

laps = range(70)  # Creating Laps List, to use on graph as parameter.
pitstop_time = 30  # PitStop time to change tyre compounds
pitstopLaps = []  # The laps used for pitstop
fuel_consumption = 1.5  # Fuel per lap


class Tyres:

    def __init__(self, current_grip, initial_deg, switch_point, switch_deg):
        '''Tyres Constructor \n\n Soft: 2.0, 0.03, 1.8, 1.2 \n\n Medium: 1.6, 0.02, 1.3, 1.2 \n\n Hard: 1.1, 0.01, 0.85, 1.2'''

        self.current_grip = current_grip  # The grip in seconds per lap of a new tyre
        self.current_deg = initial_deg
        self.switch_point = switch_point  # Where grip loss changes from linear to high
        self.switch_deg = switch_deg  # A multiplier that is applied to degradation each lap

        self.initial_grip = current_grip  # Resetting current value
        self.initial_deg = initial_deg  # Linear loss in grip per lap as a fraction of time

    def __equal__(self, tyreA, tyreB):
        ''' The equality is that all the initial parameters are the same between both tyres'''
        tyre_1 = tyreA
        tyre_2 = tyreB

        if tyre_1 == tyre_2:
            return True
        else:
            return False

    def addLap(self, current_fuel, grip_loss_factor):
        '''Simulates the wear of the tyre after another lap has been completed'''

        fuel = current_fuel  # Deg due fuel effect
        grip_factor = grip_loss_factor  # Deg due car effect on tyres
        fuelEffect = self.fuel_effect(fuel)

        # Fallen of the Cliff
        if self.current_grip < 0.2:
            self.current_grip = 0
            return self.current_grip

        # High Phase - Grip is qual or less to switch_point (specific for each tyre)
        elif self.current_grip <= self.switch_point:
            # Grip reduced by initial deg scaled by fuel effect
            # self.current_deg *= self.switch_deg * fuelEffect
            self.current_deg = (self.current_deg *
                                self.switch_deg) * fuelEffect
            # self.current_deg = self.current_deg * self.switch_deg
            self.current_grip = (self.current_grip -
                                 self.current_deg) * grip_factor
            return self.current_grip

        # Lienar Phase - Grip bigger than switch_point (specific for each tyre)
        else:
            # Grip is reduced in a linear way
            self.current_grip = (self.current_grip - (self.current_deg *
                                                      fuelEffect)) * grip_factor

            return self.current_grip

    def calculateLapTime(self, fuel, lap_time_factor):
        '''Calculates and returns the laptime based on the current fuel level and state of the tyre.'''
        lap_time = 76
        fuel_current = fuel

        # Increasing LapTime if grip is at Fallen of the Cliff
        if self.current_grip < 0.2:
            lap_time = (lap_time * lap_time_factor) + 2

        # Decreasing the Laptime if grip is at High or Standard Phase
        elif self.current_grip >= 0.2:
            lap_time = (lap_time * lap_time_factor) - self.current_grip

        # (2-(2*(fuel_current/105))) Converts the current fuel into 105 = 0 or 0 = 2 and any value porportional between it
        lap_time -= (2-((fuel_current)/52.5))
        print(str(lap_time + (2-((fuel_current)/52.5))))
        return (lap_time)

    def reset(self):
        '''Resets the tyre to its initial state'''
        self.current_grip = self.initial_grip   # Restoring grip
        self.current_deg = self.initial_deg     # Removing compound effect from deg

    def fuel_effect(self, current_fuel):
        '''To calculate the fuel effect you take the current fuel on
        board and divide it by six times the total fuel at the start of the race. you will
        then add 0.83 to this number. The reason for this is that the fuel will make up
        1/6th of the total mass of the car at the start of the race (i.e. 5/6 = 0.83)
        '''
        tank_full = 105  # Max value for fuel tank
        fuel = current_fuel  # Current value for fuel tank
        return (fuel / (tank_full*6)) + 0.83  # Returning Fuel effec


class Car:

    laptime_list = []

    def __init__(self, initial_tyre, pitstop, pitstopLaps, pit_tyres, total_laps, lap_time_factor, grip_loss_factor):
        '''Car Constructor'''

        self.initial_tyre = initial_tyre  # Initial set of tyres
        self.pitstop = pitstop  # Quantity of pitstops per simulation
        self.pit_laps = pitstopLaps  # Laps where the pitstop will occur
        self.pit_tyres = pit_tyres  # Tyres changed in PitStop
        self.grip_loss_factor = grip_loss_factor    # Impact from car on tyre
        self.lap_time_factor = lap_time_factor  # How fast the car is
        self.total_laps = total_laps  # Total quantity of laps
        self.carPerformance = []  # Laptime for the car
        self.tyres_Used = []
        self.tyres_Used.append(self.initial_tyre)
        for tyres in self.pit_tyres:
            self.tyres_Used.append(tyres)

        self.raceTime = 5

    def isValidStrategy(self):
        '''Checks if a series of condititions are True'''
        # there are less than 2 pit stops
        if (self.pitstop < 2):
            print("False less than 2")
            return False
        # there are more stops than tyres and vice versa
        elif (len(self.pit_laps) != len(self.pit_tyres)):
            print("False pit_laps != pit_tyres")
            return False
        # not all three compounds of tyre are used in the strategy
        elif (soft and medium and hard not in self.tyres_Used):
            print("False not all tyres used")
            return False
        # the first stop cannot occur on lap zero
        # the last stop cannot occur on the last lap
        elif(0 or 69 in self.pit_laps):
            print("False pitstop 0 and 70")
            return False
        # the laps for pitstops must increase monotonically and cannot overlap
        elif(any(self.pit_laps[i] >= self.pit_laps[i + 1] for i in range(len(self.pit_laps)-1))):
            return False
        else:
            return True

    def simulateRace(self):
        '''Simulates a race using this strategy to calculate an overall racetime'''

        if(self.isValidStrategy == False):
            self.raceTime = 10000

        else:
            # ************************** Initial Race Values ******************************
            soft.reset
            medium.reset
            hard.reset

            fuel = 105
            currentTyre = self.initial_tyre
            pitstop_number = 0  # Tried to use 'i' from looping but Pylance doesnt recognize
            # ******************************************************************************

            for x in laps:

                if x in self.pit_laps:
                    # Changing tyre
                    currentTyre = self.pit_tyres[pitstop_number]
                    pitstop_number += 1
                    self.carPerformance.append(
                        currentTyre.calculateLapTime(fuel, self.lap_time_factor) + pitstop_time)
                    self.raceTime += self.carPerformance[x]
                    fuel -= fuel_consumption  # Reducing fuel per lap
                else:
                    self.carPerformance.append(currentTyre.calculateLapTime(
                        fuel, self.lap_time_factor))
                    self.raceTime += self.carPerformance[x]
                    currentTyre.addLap(
                        fuel, self.grip_loss_factor)
                    fuel -= fuel_consumption

        return self.raceTime

    def energy(self):
        '''Return the overall racetime of the strategy'''
        return self.raceTime

    def chooseRandomTyre(self):
        '''Return random tyre'''
        randomTyre = randint(0, 3)
        return self.tyres_Used[randomTyre]

    def changeCompound(self):
        '''Randomly pit stop lap and change the tyre'''
        randomLap = randint(0, 2)
        self.pit_tyres[randomLap] = self.chooseRandomTyre

    def changeLap(self):
        '''Chooses one of the pit in laps at random and flips a coin to determine if we should increment or decrement that lap'''
        randomPit = randint(0, 2)
        incr_decr = randint(0, 2)

        # Decrease pit_stop
        if incr_decr == 0:
            self.pit_laps[randomPit] = self.pit_laps[randomPit] - 1

        # Increase pit_stop
        elif incr_decr == 1:
            self.pit_laps[randomPit] = self.pit_laps[randomPit] + 1

    def move(self):
        '''Determine whether to change a tyre compound or a lap number using the helper functions above.'''
        tyre_or_lap = randint(0, 2)

        if tyre_or_lap == 0:
            self.changeCompound
        elif tyre_or_lap == 1:
            self.changeLap


# pick an initial state for s
# temperature = // how may temperature iterations do we want
# pick an initial temperature to start the annealing
# scale = // how much temperature should be removed by annealing process,
# generally set to value of initial temperature
# while temperature > 0:
    # // determines how much to cool the temperature on each iteration
    # temperature = temperature - scale
    # s_new = pick a random neighbour of s
    # e = E(s)
    # e’ = E(s_new)
    # // note random must be a uniform RNG
    # if P(e, e’, temperature) >= random(0,1)
    # s = s_new
    # output final state s


class AnnealingStrategy(Annealer):

    def __init__(self, car, lap_record):

        self.car = car
        self.lap_record = lap_record
        super(AnnealingStrategy, self).__init__(self.car)

    def move(self):
        # a = self.car.move
        # b = self.car.move
        # temp = self[a]
        # self.state[a] = self.state[b]
        # self.state[b] = temp

        # time.sleep(0.001)

        self.car.move

    def energy(self):
        # total = 0
        # for i in range(0, len(self.lap_record) -1):
        #     total += self.
        self.car.energy


def testTyeGripDef(tyre, starting_fuel, laps):
    # List used to store the grip_deg per lap
    grip_deg_list = []

    fuel = starting_fuel
    for x in laps:

        # Calculating grip deg
        grip_deg_list.append(tyre.addLap(fuel, 1))

        fuel -= fuel_consumption  # Reducing fuel per lap
        print("Lap: " + str(laps[x]) + "     Fuel: " + str("%.2f" %
                                                           fuel) + "     Lap Time: " + str("%.2f" % tyre.calculateLapTime(fuel, 1)) + "     Grip: " + str("%.4f" % tyre.current_grip))

    # Reset initial_grid for each tyre after laps
    tyre.reset()
    return grip_deg_list


def testTyreLapTime(tyre, starting_fuel, laps):
    # List used to store the grip_deg per lap

    laptime_list = []

    fuel = starting_fuel
    for x in laps:

        # Calculating grip deg
        tyre.addLap(fuel, 1)
        laptime_list.append(tyre.calculateLapTime(fuel, 1))
        fuel -= fuel_consumption  # Reducing fuel per lap

        print("Lap: " + str(laps[x]) + "     Fuel: " + str("%.2f" %
                                                           fuel) + "     Lap Time: " + str("%.2f" % laptime_list[x]) + "     Grip: " + str("%.4f" % tyre.current_grip))

    # Reset initial_grid for each tyre after laps
    tyre.reset()
    print(laptime_list)
    return laptime_list


def testSample(tyre, starting_fuel, laps):

    laptime_list = []
    currentTyre = tyre
    fuel = starting_fuel
    for x in laps:

        # First stop
        if (x == 20):
            # currentTyre.addLap(fuel, 1)
            currentTyre = soft

            # Adding 30secs of pitstop
            laptime_list.append(
                currentTyre.calculateLapTime(fuel, 1) + pitstop_time)
            fuel -= fuel_consumption  # Reducing fuel per lap
            # laptime_list.append(laptime_list[18] + 30)
            print("Lap: " + str(laps[x]+1) + "     Fuel: " + str("%.2f" %
                                                                 fuel) + "     Lap Time: " + str("%.2f" % laptime_list[x]) + "     Grip: " + str("%.4f" % currentTyre.current_grip))

        # Second stop
        elif (x == 50):
            # currentTyre.addLap(fuel, 1)
            currentTyre = hard
            # Adding 30secs of pitstop
            laptime_list.append(
                currentTyre.calculateLapTime(fuel, 1) + pitstop_time)
            fuel -= fuel_consumption  # Reducing fuel per lap
            # laptime_list.append(laptime_list[48] + 30)
            print("Lap: " + str(laps[x]+1) + "     Fuel: " + str("%.2f" %
                                                                 fuel) + "     Lap Time: " + str("%.2f" % laptime_list[x]) + "     Grip: " + str("%.4f" % currentTyre.current_grip))
        else:
            # Calculating grip deg
            laptime_list.append(currentTyre.calculateLapTime(fuel, 1))
            currentTyre.addLap(fuel, 1)
            fuel -= fuel_consumption  # Reducing fuel per lap
            print("Lap: " + str(laps[x]+1) + "     Fuel: " + str("%.2f" %
                                                                 fuel) + "     Lap Time: " + str("%.2f" % laptime_list[x]) + "     Grip: " + str("%.4f" % currentTyre.current_grip))

    # Reset initial_grid for each tyre after laps
    tyre.reset()
    # print(laptime_list)
    return laptime_list


# Tyres Compounds
soft = Tyres(2.0, 0.03, 1.8, 1.2)
medium = Tyres(1.6, 0.02, 1.3, 1.2)
hard = Tyres(1.1, 0.01, 0.85, 1.2)

tyres = []
tyres.append(medium)
tyres.append(hard)

pitstop_laps = []
pitstop_laps.append(20)
pitstop_laps.append(50)

mercedes = Car(soft, 2, pitstop_laps, tyres, 70, 0.987, 0.996)
ferrari = Car(soft, 2, pitstop_laps, tyres, 70, 0.99, 0.99)
redbull = Car(soft, 2, pitstop_laps, tyres, 70, 0.991, 0.982)


# ................................................... Annealing Strategy...................................................
# .....................................................................................................................


# test = AnnealingStrategy(mercedes, mercedes.carPerformance)
# test.steps = 100000
# state, e = test.anneal()

# annealingStrategy(mercedes)
# print(
#     mercedes.simulateRace())
# print(
#     ferrari.simulateRace())
# print(
#     redbull.simulateRace())


# subplot(1, 1, 1)

# plt.title('Annealing Strategy')
# plt.plot(laps, mercedes.carPerformance, '-x', markersize=4,
#          color='green', alpha=0.5, label='Mercedes')
# plt.plot(laps, ferrari.carPerformance, '-x', markersize=4,
#          color='red', alpha=0.5, label='Ferrari')
# plt.plot(laps, redbull.carPerformance, '-x', markersize=4,
#          color='blue', alpha=0.5, label='RedBull')
# plt.legend()
# plt.ylabel('Lap Time')
# plt.xlabel('Lap Number')
# plt.show()

def printGraphs(graph_number):

    if graph_number == 1:
        subplot(2, 2, 1)
        soft_grip_graph1 = testTyeGripDef(soft, 105, laps)
        medium_grip_graph1 = testTyeGripDef(medium, 105, laps)
        hard_grip_graph1 = testTyeGripDef(hard, 105, laps)
        plt.title('Degradation of all three compounds grip = 105Kg (full load)')
        plt.plot(laps, soft_grip_graph1, '-x', markersize=4,
                 color='red', alpha=0.5, label='Soft')
        plt.plot(laps, medium_grip_graph1, '-x', markersize=4,
                 color='green', alpha=0.5, label='Medium')
        plt.plot(laps, hard_grip_graph1, '-x', markersize=4,
                 color='blue', alpha=0.5, label='Hard')
        plt.legend()
        plt.ylabel('Grip Level')

        subplot(2, 2, 2)
        soft_grip_graph2 = testTyeGripDef(soft, 60, laps)
        medium_grip_graph2 = testTyeGripDef(medium, 60, laps)
        hard_grip_graph2 = testTyeGripDef(hard, 60, laps)

        plt.title('Degradation of all three compounds grip = 60Kg')
        plt.plot(laps, soft_grip_graph2, '-x', markersize=4,
                 color='red', alpha=0.5, label='Soft')
        plt.plot(laps, medium_grip_graph2, '-x', markersize=4,
                 color='green', alpha=0.5, label='Medium')
        plt.plot(laps, hard_grip_graph2, '-x', markersize=4,
                 color='blue', alpha=0.5, label='Hard')
        plt.legend()
        plt.ylabel('Grip Level')

        subplot(2, 2, 3)
        soft_grip_graph3 = testTyreLapTime(soft, 105, laps)
        medium_grip_graph3 = testTyreLapTime(medium, 105, laps)
        hard_grip_graph3 = testTyreLapTime(hard, 105, laps)
        plt.title('Degradation of all three compounds Lap Time = 105Kg (full load)')
        plt.plot(laps, soft_grip_graph3, '-x', markersize=4,
                 color='red', alpha=0.5, label='Soft')
        plt.plot(laps, medium_grip_graph3, '-x', markersize=4,
                 color='green', alpha=0.5, label='Medium')
        plt.plot(laps, hard_grip_graph3, '-x', markersize=4,
                 color='blue', alpha=0.5, label='Hard')
        plt.legend()
        plt.ylabel('Lap Time')

        subplot(2, 2, 4)
        soft_grip_graph4 = testTyreLapTime(soft, 60, laps)
        medium_grip_graph4 = testTyreLapTime(medium, 60, laps)
        hard_grip_graph4 = testTyreLapTime(hard, 60, laps)
        plt.title('Degradation of all three compounds Lap Time = 60Kg')
        plt.plot(laps, soft_grip_graph4, '-x', markersize=4,
                 color='red', alpha=0.5, label='Soft')
        plt.plot(laps, medium_grip_graph4, '-x', markersize=4,
                 color='green', alpha=0.5, label='Medium')
        plt.plot(laps, hard_grip_graph4, '-x', markersize=4,
                 color='blue', alpha=0.5, label='Hard')
        plt.legend()
        plt.ylabel('Lap Time')
        plt.xlabel('Lap Number')
        plt.show()

    elif graph_number == 2:
        subplot(1, 1, 1)
        sample_graph = testSample(medium, 105, laps)
        plt.title('Sample Strategy')
        plt.plot(laps, sample_graph, '-x', markersize=4,
                 color='red', alpha=0.5, label='Laptimes')
        plt.legend()
        plt.ylabel('Lap Time')
        plt.xlabel('Lap Number')

        plt.show()


# ................................................... Printing Graphs...................................................
# .....................................................................................................................
# '1' for First 4 graphs and '2' for 'Lap Number' graph
printGraphs(1)
