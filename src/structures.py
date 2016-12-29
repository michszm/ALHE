from utils import two_points_distance


class NetworkTree:

    goal_func = 0

    def __init__(self):
        self.segments = []

    def count_goal_func(self, cost_traction, cost_power_lines):
        for seg in self.segments:
            if seg.conn_to_powerstation:
                for power_seg_len in seg.powers_line_segment_len:
                    self.goal_func += power_seg_len * cost_power_lines
            else:
                self.goal_func += seg.length() * cost_traction
        self.goal_func = 1.0 / self.goal_func
        return self.goal_func

    def add_new_segment(self, line_segment):
        self.segments.append(line_segment)


class LineSegment:

    def __init__(self, point1, point2):
        self.points = set()
        self.points.add(point1)
        self.points.add(point2)
        self.conn_to_powerstation = False
        self.powers_line_segment = []
        self.powers_line_segment_len = []
        self.powers_coord = []

    def __eq__(self, other):
        return self.points == other.points

    def length(self):
        points = self.points.copy()
        return two_points_distance(points.pop() + (0,), points.pop() + (0,))

    # x1, y1
    # x2, y2
    # px, py - powerstation locations
