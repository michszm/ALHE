from utils import two_points_distance


class NetworkTree:

    goal_func = 0
    segments = []

    def __init__(self):
        self.segments = []

    def count_goal_func(self, cost_traction, cost_power_lines):
        for segment in self.segments:
            if segment.conn_to_powerstation:
                self.goal_func += segment.powers_line_segment_len * cost_power_lines
            else:
                self.goal_func += segment.length() * cost_traction
        self.goal_func = 1.0 / self.goal_func
        return self.goal_func

    def add_new_segment(self, line_segment):
        self.segments.append(line_segment)


class LineSegment:

    conn_to_powerstation = False
    powers_line_segment_len = 0
    powers_coord = ()

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def length(self):
        return two_points_distance(self.point1 + (0,), self.point2 + (0,))

    # x1, y1
    # x2, y2
    # px, py - powerstation locations
