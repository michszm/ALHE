from utils import two_points_distance
from utils import nrst_pt_on_seg
from random import sample

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

    def mutate(self):
        new_segment = self.add_any_new_segment()
        new_segment_point = new_segment.points.copy().pop()
        # WIP
        # cycle_segments = self.find_cycle(new_segment_point)
        cycle_segments = None
        cycle_segments.remove(new_segment)
        segment_to_remove = sample(cycle_segments, 1).pop()
        self.segments.remove(segment_to_remove)
        if segment_to_remove.conn_to_powerstation:
            for coord in segment_to_remove.powers_coord:
                self.connect_power_plant(coord)

    def add_new_segment(self, line_segment):
        self.segments.append(line_segment)

    def add_any_new_segment(self):
        adj_list = self.to_adj_list()
        all_points = set(adj_list.keys())
        unchecked_points = all_points.copy()
        insert_point = None
        point_outsiders = None
        new_segment = None
        while unchecked_points:
            insert_point = sample(unchecked_points, 1).pop()
            unchecked_points.remove(insert_point)
            point_neighbors = adj_list[insert_point]
            point_outsiders = (all_points - point_neighbors)
            point_outsiders.remove(insert_point)
            if point_outsiders:
                break
        if point_outsiders:
            new_neighbor = sample(point_outsiders, 1).pop()
            new_segment = LineSegment(insert_point, new_neighbor)
            self.add_new_segment(new_segment)
        else:
            pass

        return new_segment

    def to_adj_list(self):
        adj_list = {}
        for seg in self.segments:
            points = seg.points.copy()
            point1 = points.pop()
            point2 = points.pop()
            if point1 not in adj_list:
                adj_list[point1] = set()
            if point2 not in adj_list:
                adj_list[point2] = set()
            adj_list[point1].add(point2)
            adj_list[point2].add(point1)
        return adj_list

    def connect_power_plant(self, powers_coord):
        min_dist = float("inf")
        min_dist_point = None
        min_dist_segment = None
        for seg in self.segments:
            points = seg.points.copy()
            point1 = points.pop()
            point2 = points.pop()
            pt, dist = nrst_pt_on_seg(powers_coord + (0,),
                                      point1 + (0,),
                                      point2 + (0,))
            if dist < min_dist:
                min_dist = dist
                min_dist_point = (pt[0], pt[1])
                min_dist_segment = seg
        if min_dist_point is not None:
            powers_seg = LineSegment(min_dist_point, powers_coord)
            min_dist_segment.conn_to_powerstation = True
            min_dist_segment.powers_line_segment.append(powers_seg)
            min_dist_segment.powers_line_segment_len.append(min_dist)
            min_dist_segment.powers_coord.append(powers_coord)
        else:
            pass


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
