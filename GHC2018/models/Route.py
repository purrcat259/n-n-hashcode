class Route:
    def __init__(self, ordered_rides):
        self.ordered_rides = ordered_rides
        self.assigned = False
        self.next_routes = []
