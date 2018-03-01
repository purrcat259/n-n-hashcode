import math


def calculate_distance(row_start, row_end, col_start, col_end):
    return abs(row_start - row_end) + abs(col_start - col_end)


class Ride:
    def __init__(self, ride_id, row_start, col_start, row_end, col_end, earliest_start, latest_finish):
        self.ride_id = ride_id
        self.earliest_start = earliest_start
        self.col_end = col_end
        self.row_end = row_end
        self.latest_finish = latest_finish
        self.col_start = col_start
        self.row_start = row_start
        self.assigned_car = None  # -1 means unassigned
        self.max_duration = self.latest_finish - self.earliest_start
        self.distance = calculate_distance(self.row_start, self.row_end, self.col_start, self.col_end)



