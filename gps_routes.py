"""Create routes between cities on a map."""
import sys
import argparse
# Your implementation of City, Map, bfs, and main go here.

class City:
    """A class that holds the data representing a City.
    
    Attributes:
        name (str): inputted name of the city
        neighbors (dict): Starts off as an empty string that we will populate 
            with the add_neighbor() method later. The keys of this dictionary will 
            be other City objects that are connected to this instance of City. The 
            values of those keys are tuples where the first item is the distance 
            between the cities(int), and the interstate(str) that connects them.
    """
    def __init__(self, name):
        """Define __init__() to set the variables to the corresponding value.
        
        Args:
            self: a reference to the class
            name (str): inputted name of the city
        
        Side effects:
            Modifies the value of name and neighbors
        """
        # set the name argument to an attribute
        self.name = name
        # set the neighbors attribute to an empty dictionary
        self.neighbors = {}

    def __repr__(self):
        """Define __repr__() to return name.
        
        Args: 
            self: a reference to the class
            
        Returns:
            name (str): return the name attribute of the instance
        """
        return self.name

    def add_neighbor(self, neighbor, distance, interstate):
        """Define add_neighbor() that creates the key/value pairs for the 
        neighbor City.
        
        Args:
            self: a reference to the class
            neighbor(City): the City object that will be connected to the instance
            distance(str): the distance between the two cities
            interstate(str): the interstate number that connects the two cities 
        
        Side effects:
            Modifies the neighbors attribute
        """
        # checking to see if the neighbor is present within the city
        if type(neighbor) is City and neighbor not in self.neighbors:
            # create the key/value pair using the tuple with the distance and interstate
            self.neighbors[neighbor] = (distance, interstate)
            neighbor.neighbors[self] = (distance, interstate)

class Map:
    """A class that stores the map data as a form of Graph where each node in 
    the Graph is a city, and the edges are represented by the relationships that 
    the cities have to each other.
    
    Attributes:
        cities: a list of all of the unique city objects that make up the Graph 
            structure.
    """
    def __init__(self, relationships):
        """Define __init__() method that will work to find the corresponding values
        using the City object to later connect each city together.
        
        Args:
            self: a reference to the class
            relationships (dict): A dictionary where the keys are individual cities
            and the values are a list of tuples
        
        Side effects:
            Modifies the value of the cities attribute. Will also use methods from
            the City class to update the list
        """
        # set the cities attribute to an empty list 
        self.cities = {}
        # using .items() to access the key in the relationships dictionary
        for cities_name, relationship_info in relationships.items():
            # create a city object with the name of that city
            corresponding_city = self.__repr__(cities_name) 
            # using the tuple with the three elements corresponding to the relationships
            for neighbor_str, distance, interstate in relationship_info:
                # create a neighbor string 
                key_city = self.__repr__(neighbor_str) 
                # using the add_neighbor() method of the city object, connect each city
                corresponding_city.add_neighbor(key_city, distance, interstate)
                

    def __repr__(self, name):
        """Define __repr__ to return the string representation of the cities 
        attribute.
        
        Agrs:
            self: a reference to the class
            name (str): inputted name of the city
          
        Returns:
            city: object that contains the cities attribute
          
        Side effects:
            Modifies the name and cities attribute
        """
        # if the name is found in the cities attribute
        if name in self.cities:
            # create a city object with that name and append it to cities attribute
            return self.cities[name]
        # find the corresponding City by its name
        corresponding_city = City(name)
        # ensure the name from the cities attribute is equal to city
        self.cities[name] = corresponding_city
        # return the string represention of the cities attribute
        return corresponding_city
    
    
def bfs(Graph, Start, Goal):
    """Define bfs() that will find the shortest paths between two nodes in a 
    graph structure.
    
    Args:
        Graph (Map): a map object representing the graph that we will be traversing
        Start (str): the start city in a roadtrip
        Goal (str): the destination city in a roadtrip
    
    Returns:
        list of strings (cities) we will vist on the shortest path
    """
    # creates a variable to ensure we are starting at the start location
    starting_place = Graph[Start]
    # create an empty list  
    explored = set()
    # create a list within a list where the inner list contains the start city
    queue = [[starting_place]]
    # while the queue is not empty
    while queue:
        # pop the first element from the queue
        saved_path = queue.pop(0)
        # identify the last node from the saved_path
        last_node = saved_path[-1]
        # if the last_not is not currently present in explored
        if last_node not in explored:
            # find the node whose name matches the current value of the node
            # .keys() ensures that this is a dictionary
            neighbors = last_node.neighbors.keys()
            # for each item within neighbors
            for neighbor in neighbors:
                # convert the saved_path to a variable named new_path
                new_path = list(saved_path)
                # append the neighbor item to the new_path
                new_path.append(neighbor)
                # append the new_path to the queue
                queue.append(new_path)
                # if the string representation of neighbor is the same value as goal
                if neighbor.name == Goal:
                    # return a list containing the string represention in the new_path using list comprehension
                    return [city.name for city in new_path]
            # append the node to explored
            explored.add(last_node)
    # if no path is found print a message then return None
    print("No path was found between the starting city and the goal")
    return None
    
def main(start, destination, connections):
    """Define main() to create the Map object with the connections data that is 
    being passed in. It will then use bfs() to find the path between a start 
    City and a destination City. It will parse the returned value and instruct 
    the user on where they should drive given a start node and an end node.
    
    Args: 
        start(str): the start city in a roadtrip
        destination(str): the destination city in a roadtrip
        Graph(dict): a dictionary representing an adjecency list of cities and 
            the cities to which they connect
    
    Returns:
        a string that contains all of the same contents that we have printed out
        to the console
    """
    # create a map object using connections attribute
    map_directions = Map(connections)
    # using bfs(), get the cities and the start and destination city and call it instructions
    instructions = bfs(map_directions.cities, start, destination)
    # declare an empty string
    empty_result = ""
    # for each of the cities elements in the instructions
    for city_element, city in enumerate(instructions):
        # if the current element is the first element
        if city_element == 0:
            # print a message and add it to the empty string
            print(f"Starting at {city}")
            empty_result += f"Starting at {city}\n"
        # if the current element is anything before the last element
        if city_element < len(instructions) - 1:
            # identify the following city in the list
            following_city = instructions[city_element + 1]
            # using the map object find the city's name who is the same and the neighbors to this city 
            for neighbor, (distance, interstate) in map_directions.__repr__(city).neighbors.items():
                # use an if statement to locate the next city and make sure the dictionary's keys are strings
                if str(neighbor) == following_city:
                    # print a message with the information and add it to the empty string
                    print(f"Drive {distance} miles on {interstate} towards {following_city}, then")
                    empty_result += f"Drive {distance} miles on {interstate} towards {following_city}, then\n" 
        # if the current element is the last element          
        if city_element == len(instructions) - 1:
            # print the last message and add it to the string
            print(f"You will arrive at your destination")
            empty_result += f"You will arrive at your destination"
    return(empty_result)

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis,", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 283, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "80"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 183, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburg": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 304, "76"), ("New York", 391, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburg", 107, "76")], #COMEBACK
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence,", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 101, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)