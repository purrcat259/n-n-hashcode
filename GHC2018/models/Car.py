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
        self.assigned_ride.complete()
        # Get rid of the completed one
        self.assigned_route.ordered_rides.pop()
        # get the next one if one exists
        if len(self.assigned_route.ordered_rides) > 0:
            self.assigned_ride = self.assigned_route.ordered_rides[0]

    def complete_route(self):
        self.assigned_route = None

    def assigned_route_completed(self):
        return len(self.assigned_route.ordered_rides) == 0

    def move_towards_destination(self):
        target_row, target_col = self.assigned_ride.row_end, self.assigned_ride.col_end
        if target_row > self.row:
            self.move_down()
        elif target_row < self.row:
            self.move_up()
        elif target_col > self.col:
            self.move_right()
        else:
            self.move_left()

    def move_up(self):
        # print('Car {} moving UP'.format(self.car_id))
        self.row -= 1

    def move_down(self):
        # print('Car {} moving DOWN'.format(self.car_id))
        self.row += 1

    def move_right(self):
        # print('Car {} moving RIGHT'.format(self.car_id))
        self.col += 1

    def move_left(self):
        # print('Car {} moving LEFT'.format(self.car_id))
        self.row -= 1
