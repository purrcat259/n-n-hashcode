class Car:
    def __init__(self, car_id, row=0, col=0):
        self.car_id = car_id
        self.row = row
        self.col = col
        self.assigned_ride = None
        self.assigned_route = None

    def assign_ride(self, ride):
        self.assigned_ride = ride

    def assign_route(self, route):
        self.assigned_route = route
        for ride in route.ordered_rides:
            ride.assigned_car = self.car_id
        self.assign_ride(route.ordered_rides[0])

    def is_at_destination(self):
        return self.row == self.assigned_ride.row_end and self.col == self.assigned_ride.col_end

    def complete_ride(self):
        self.assigned_ride = None

    def complete_route(self):
        self.assigned_route = None

    def move_towards_destination(self):
        # TODO
        pass
