import sys
import matplotlib.pyplot as plt
import numpy as np
from pylab import *


class Tyres:

    def __init__(self, current_grip, initial_deg, switch_point, switch_deg):
        '''Tyres Constructor \n\n Soft: 2.0, 0.03, 1.8, 1.25 \n\n Medium: 1.5, 0.02, 1.2, 1.25 \n\n Hard: 1.0, 0.01, 0.75, 1.25'''

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

    def addLap(self, current_fuel, grip_loss_factor, fuel_tank):
        '''Simulates the wear of the tyre after another lap has been completed'''

        fuel = current_fuel  # Deg due fuel effect
        fuelFull = fuel_tank
        grip_factor = grip_loss_factor  # Deg due car effect on tyres
        fuelEffect = self.fuel_effect(fuel, fuel_tank)

        # Fallen of the Cliff
        if self.current_grip < 0.3:
            return 0

        # High Phase - Grip is qual or less to switch_point (specific for each tyre)
        elif self.current_grip <= self.switch_point:
            # Grip reduced by initial deg scaled by fuel effect
            self.current_deg = self.current_deg * self.switch_deg * fuelEffect
            self.current_grip -= ((self.current_deg *
                                   fuelEffect) * grip_factor)
            return self.current_grip

        # Lienar Phase - Grip bigger than switch_point (specific for each tyre)
        else:
            # Grip is reduced in a linear way
            self.current_grip -= ((self.current_deg *
                                   fuelEffect) * grip_factor)

            return self.current_grip

    def calculateLapTime(self, fuel, lap_time_factor):
        '''Calculates and returns the laptime based on the current fuel level and state of the tyre.'''
        lap_time = 90

        fuel_current = fuel

        # Increasing LapTime if grip is at Fallen of the Cliff
        if self.current_grip < 0.3:
            lap_time = (lap_time + 2) * lap_time_factor

        # Decreasing the Laptime if grip is at High or Standard Phase
        elif self.current_grip >= 0.3:
            lap_time -= self.current_grip * lap_time_factor

        # (2-(2*(fuel_current/105))) Converts the current fuel into 105 = 0 or 0 = 2 and any value porportional between it
        lap_time -= (2-((2*fuel_current)/105))
        print(str(lap_time + (2-((2*fuel_current)/105))))
        return (lap_time)

    def reset(self):
        '''Resets the tyre to its initial state'''
        self.current_grip = self.initial_grip   # Restoring grip
        self.current_deg = self.initial_deg     # Removind compound effect from deg

    def fuel_effect(self, current_fuel, full_fuel):
        '''To calculate the fuel effect you take the current fuel on
        board and divide it by six times the total fuel at the start of the race. you will
        then add 0.83 to this number. The reason for this is that the fuel will make up
        1/6th of the total mass of the car at the start of the race (i.e. 5/6 = 0.83)
        '''
        tank_full = full_fuel  # Max value for fuel tank
        fuel = current_fuel  # Current value for fuel tank
        return (current_fuel / (full_fuel*6)) + 0.83  # Returning Fuel effec


class Car:
    def __init__(self, initial_tyre, pitstop, pit_tyres, total_laps, grip_loss_factor, lap_time_factor):
        '''Car Constructor'''

        self.initial_tyre_ = initial_tyre  # Initial set of tyres
        self.pitstop = pitstop  # Quantity of pitstops per simulation
        self.pit_tyres = pit_tyres  # Tyres changed in PitStop
        self.grip_loss_factor = grip_loss_factor    # Impact from car on tyre
        self.lap_time_factor = lap_time_factor  # How fast the car is
        self.total_laps = total_laps  # Total quantity of laps

    def isValidStrategy(self):
        '''Checks if a series of condititions are True'''

    def simulateRace(self):
        '''Simulates a race using this strategy to calculate an overall racetime'''

    def energy(self):
        '''Return the overall racetime of the strategy'''

    def chooseRandomTyre(self):
        '''Return random tyre'''

    def changeCompound(self):
        '''If only one PitStop, will chose a differen compound. If multiple PitStops simulation, will choose a random Tyre'''

    def changeLap(self):
        '''Chooses one of the pit in laps at random and flips a coin to determine if we should increment or decrement that lap'''

    def move(self):
        '''Determine whether to change a tyre compound or a lap number using the helper functions above.'''


laps = range(60)  # Creating Laps List, to use on graph as parameter.
pitstop_time = 24  # PitStop time to change tyre compounds
fuel_consumption = 1.72  # Fuel per lap

# Graph 1
# Adding the initial value for Soft Tyres

def testTyeGripDef(tyre, starting_fuel, laps):
    # List used to store the grip_deg per lap
    grip_deg_list = []

    fuel = starting_fuel
    fuel_tank = starting_fuel
    for x in laps:

        # Calculating grip deg
        grip_deg_list.append(tyre.addLap(fuel, 1, fuel_tank))

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
    fuel_tank = starting_fuel
    for x in laps:

        # Calculating grip deg
        tyre.addLap(fuel, 1, fuel_tank)
        laptime_list.append(tyre.calculateLapTime(fuel, 1))
        fuel -= fuel_consumption  # Reducing fuel per lap

        print("Lap: " + str(laps[x]) + "     Fuel: " + str("%.2f" %
                                                           fuel) + "     Lap Time: " + str("%.2f" % laptime_list[x]) + "     Grip: " + str("%.4f" % tyre.current_grip))

    # Reset initial_grid for each tyre after laps
    tyre.reset()
    print(laptime_list)
    return laptime_list


# Tyres Compounds
soft = Tyres(2.0, 0.03, 1.8, 1.25)
medium = Tyres(1.5, 0.02, 1.2, 1.25)
hard = Tyres(1.0, 0.01, 0.75, 1.25)

# mercedes = Car(soft, 15, hard, 60, 1, 1)

# soft_grip_graph1 = testTyeGripDef(soft, 105, laps)
# medium_grip_graph1 = testTyeGripDef(medium, 105, laps)
# hard_grip_graph1 = testTyeGripDef(hard, 105, laps)
# plt.title('Lap Times for Strategy')
# plt.plot(laps, soft_grip_graph1, '-x', markersize=4,
#          color='red', alpha=0.5, label='Soft')
# plt.plot(laps, medium_grip_graph1, '-x', markersize=4,
#          color='green', alpha=0.5, label='Medium')
# plt.plot(laps, hard_grip_graph1, '-x', markersize=4,
#          color='blue', alpha=0.5, label='Hard')
# plt.legend()
# plt.ylabel('Lap Time')
# plt.xlabel('Lap Number')
# plt.show()



# Generating the Graphs 1,2,3,4

subplot(2, 2, 1)
soft_grip_graph1 = testTyeGripDef(soft, 105, laps)
medium_grip_graph1 = testTyeGripDef(medium, 105, laps)
hard_grip_graph1 = testTyeGripDef(hard, 105, laps)
plt.title('Degradation of all three compounds grip = 105Kg')
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
plt.title('Degradation of all three compounds Lap Time = 105Kg')
plt.plot(laps, soft_grip_graph3, '-x', markersize=4,
        color='red', alpha=0.5, label='Soft')
plt.plot(laps, medium_grip_graph3, '-x', markersize=4,
        color='green', alpha=0.5, label='Medium')
plt.plot(laps, hard_grip_graph3, '-x', markersize=4,
        color='blue', alpha=0.5, label='Hard')
plt.legend()
plt.ylabel('Lap Time')
plt.xlabel('Lap Number')

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
