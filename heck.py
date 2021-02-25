import random

class Intersection:

    def __init__(self, ownId):
        self.id = ownId
        self.streets_in = []
        self.streets_out = []

class LightSchedule:

    def __init__(self, intersection_id):
        self.intersection_id = intersection_id
        self.street_names = []
        self.durations = []
        self.last_time = 0

    def add_street(self, street_name, duration):
        self.street_names.append(street_name)
        self.durations.append(duration)

    def add_street_at(self, street_name, time):
        self.street_names.append(street_name)
        if len(self.street_names) > 1:
            self.durations[-1] = time - self.last_time
            self.last_time = time
        self.durations.append(0) # temporary zero

    def has_data(self):
        return len(self.street_names) > 0

    def finalize(self, final_time):
        if len(self.durations) > 0 and self.durations[-1] == 0:
            self.durations[-1] = final_time - self.last_time
            self.last_time = final_time
        
        new_street_names = []
        new_durations = []
        
        for i, street_name in enumerate(self.street_names):
            if len(new_street_names) == 0 or new_street_names[-1] != street_name:
                new_street_names.append(street_name)

            for j in range(len(new_street_names) - 1, -1, -1):
                new_street_name = new_street_names[j]
                if street_name == new_street_name:
                    while len(new_durations) < j + 1:
                        new_durations.append(0)
                    new_durations[j] += self.durations[i]
                    break

        self.street_names = new_street_names
        self.durations = new_durations
    
    def __str__(self):
        return "{}\n{}\n{}".format(
            self.intersection_id,
            len(self.street_names),
            "\n".join([f"{street_name} {duration}" for street_name, duration in zip(self.street_names, self.durations)]))

class Street:

    def __init__(self, name, duration, intersection1_id, intersection2_id):
        self.name = name
        self.duration = duration
        self.intersection1_id = intersection1_id
        self.intersection2_id = intersection2_id
        self.popularity = 0

class Car:

    def __init__(self, ownId, route):
        self.id = ownId
        
        # first item of the list is the last street travelled along
        self.route = route

    def move(self):
        self.route.pop(0)

    def get_current_intersection(self, streets, intersections):
        street = streets[self.route[0]]
        return intersections[street.intersection2_id]

    def get_current_street(self, streets):
        #print("-=-=-=-=-=-=-=-=-=-=-=-=-")
        #print(self.id)
        #print(streets)
        #print(self.route)
        if len(self.route) == 0:
            return None
        return streets[self.route[0]]

def solve_file(path):
    file = open(path, "r")
    lines = file.read().split("\n")
    file.close()

    header = lines[0].split()

    simulation_duration = int(header[0])
    number_of_intersections = int(header[1])
    number_of_streets = int(header[2])
    number_of_cars = int(header[3])
    destination_points = int(header[4])

    print(f"Simulation duration: {simulation_duration}")
    print(f"# of intersections: {number_of_intersections}")
    print(f"# of streets: {number_of_streets}")
    print(f"# of cars: {number_of_cars}")
    print(f"Points for reaching destination: {destination_points}")

    intersections = []
    streets = {}
    cars = []
    light_schedules = {}

    # generate the crap

    # intersections
    for i in range(number_of_intersections):
        intersections.append(Intersection(i))

    # streets
    for line in lines[1:1+number_of_streets]:
        values = line.split()
        intersection1_id = int(values[0])
        intersection2_id = int(values[1])
        name = values[2]
        duration = int(values[3])
        streets[name] = Street(name, duration, intersection1_id, intersection2_id)

    # car routes
    for i, line in enumerate(lines[1+number_of_streets:]):
        if line.strip() == "": # ooh la laa
            continue
        values = line.split()
        route = values[1:]
        cars.append(Car(i, route))

    # aggregate street names onto intersection object
    for street_id, street in streets.items():
        for intersection in intersections:
            if intersection.id == street.intersection2_id:
                intersection.streets_in.append(street)
            elif intersection.id == street.intersection2_id:
                intersection.streets_out.append(street)

    #calculate street popularity
    for car in cars:
        for street_name in car.route:
            streets[street_name].popularity += 1

    # do the solution
    for intersection in intersections:
        if intersection.id not in light_schedules:
            light_schedules[intersection.id] = LightSchedule(intersection.id)
        schedule = light_schedules[intersection.id]

        streets_in = [s for s in intersection.streets_in if s.popularity > 0]
        if len(streets_in) == 0:
            continue

        popularities = [s.popularity for s in streets_in]
        hcf = 1
        for n in range(int(max(popularities) ** 0.5), 1, -1):
            if sum([p % n for p in popularities]) == 0:
                hcf = n
                break
        
        for street in streets_in:
            #schedule.add_street(street.name, street.popularity // hcf)
            # random time!!!!!!!!!!!!
            schedule.add_street(street.name, random.randint(1,6))

    # finalization only needs to be done if using add_street_at!!!! so don't!!!!!!
    #print("finalizing...")
    for schedule in light_schedules.values():
        # schedule.finalize(simulation_duration)
        pass

    file = open(path + ".solution.txt", "w")
    file.write(f"{len([ls for ls in light_schedules.values() if ls.has_data()])}\n" + "\n".join([str(ls) for ls in light_schedules.values() if ls.has_data()]))
    file.close()

for letter in ["a", "b", "c", "d", "e", "f"]:
    print(f"\nSolving '{letter}'!")
    solve_file(f"{letter}.txt");

