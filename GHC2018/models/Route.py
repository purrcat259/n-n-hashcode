class Route:
    def __init__(self, ordered_rides):
        self.ordered_rides = ordered_rides
        self.assigned = False
        self.next_routes = []

    def get_route_ride_ids(self):
        return [ride.ride_id for ride in self.ordered_rides]
