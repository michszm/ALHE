from utils import two_pts_dist, nrst_pt_on_seg_plane
from random import sample

class NetworkTree:

    def __init__(self):
        self.goal_func = 0
        self.segments = []
        self.plant_to_seg = {}

    def count_goal_func(self, cost_traction, cost_power_lines):
        self.goal_func = 0
        for seg in self.segments:
            self.goal_func += seg.length() * cost_traction

            if seg.conn_to_powerstation:
                for power_seg_len in seg.powers_line_segment_len:
                    self.goal_func += power_seg_len * cost_power_lines

        self.goal_func = 1.0 / self.goal_func
        return self.goal_func

    def mutate(self):
        new_segment = self.add_any_new_segment()
        new_segment_point = new_segment.points.copy().pop()
        cycle_segments = self.find_cycle(new_segment_point)
        cycle_segments.remove(new_segment)
        segment_to_remove = sample(cycle_segments, 1).pop()
        self.segments.remove(segment_to_remove)

        if segment_to_remove.conn_to_powerstation:
            for coord in segment_to_remove.powers_coord:
                self.connect_power_plant(coord)

        new_seg_points = new_segment.get_points()
        new_seg_a = new_seg_points.pop()
        new_seg_b = new_seg_points.pop()
        for plant in self.plant_to_seg:
            nrst_pt, dist = nrst_pt_on_seg_plane(plant, new_seg_a, new_seg_b)
            curr_segment = self.plant_to_seg[plant]
            if dist < curr_segment.dst_to_plant(plant):
                self.unlink_plant_from_seg(curr_segment, plant)
                self.link_plant_to_seg(new_segment, plant, nrst_pt)

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

    def find_cycle(self, start_point):
        adj_list = self.to_adj_list()
        queue = [start_point]
        visited = set()
        visited.add(start_point)
        parents = dict()
        parents[start_point] = None
        cycle = None
        while queue and not cycle:
            parent = queue.pop()
            for child in adj_list[parent]:
                if child in visited and child != parents[parent]:
                    cycle = list()
                    cycle.append(self.find_seg_with_coords(parent,  child))
                    last_child = child
                    child = parent
                    parent = parents[parent]
                    while parent is not last_child:
                        cycle.append(self.find_seg_with_coords(parent, child))
                        child = parent
                        if not parents[parent]:
                            break
                        parent = parents[parent]
                    if parent is not last_child:
                        child = parent
                        parent = last_child
                        cycle.append(self.find_seg_with_coords(parent, child))
                        break
                elif child not in visited:
                    visited.add(child)
                    parents[child] = parent
                    queue.append(child)

        return cycle

    def connect_power_plant(self, powers_coord):
        min_dist = float("inf")
        min_dist_point = None
        min_dist_segment = None
        for seg in self.segments:
            points = seg.get_points()
            point1 = points.pop()
            point2 = points.pop()
            pt, dist = nrst_pt_on_seg_plane(powers_coord, point1, point2)
            if dist < min_dist:
                min_dist = dist
                min_dist_point = pt
                min_dist_segment = seg
        if min_dist_point is not None:
            self.link_plant_to_seg(min_dist_segment, powers_coord, min_dist_point)
        else:
            pass

    def find_seg_with_coords(self, a, b):
        segment = LineSegment(a, b)
        segment_index = self.segments.index(segment)
        found_segment = self.segments[segment_index]
        return found_segment

    def pick_rand_segment(self):
        rand_seg = sample(self.segments,1)
        return rand_seg

    def link_plant_to_seg(self, seg, plant, link_pt):
        if link_pt:
            conn_seg = LineSegment(plant, link_pt)
            seg.link_plant(plant, conn_seg, two_pts_dist(plant + (0,), link_pt + (0,)))
        else:
            seg_points= seg.get_points()
            seg_a = seg_points.pop()
            seg_b = seg_points.pop()
            nrst_pt, dist = nrst_pt_on_seg_plane(plant, seg_a, seg_b)
            conn_seg = LineSegment(plant, nrst_pt)
            seg.link_plant(plant, conn_seg, dist)
        self.plant_to_seg[plant] = seg

    def unlink_plant_from_seg(self, seg, plant):
        seg.unlink_plant(plant)
        self.plant_to_seg.pop(plant)

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

    def __hash__(self):
        points = self.points.copy()
        return hash(tuple((points.pop(), points.pop())))

    def dst_to_plant(self, plant):
        if plant in self.powers_coord:
            plant_index = self.powers_coord.index(plant)
            return self.powers_line_segment_len[plant_index]
        else:
            return None

    def link_plant(self, plant, conn_seg, conn_dst):
        if not self.powers_coord:
            self.conn_to_powerstation = True
        self.powers_coord.append(plant)
        self.powers_line_segment.append(conn_seg)
        self.powers_line_segment_len.append(conn_dst)

    def unlink_plant(self, plant):
        if plant in self.powers_coord:
            plant_index = self.powers_coord.index(plant)
            self.powers_coord.pop(plant_index)
            self.powers_line_segment_len.pop(plant_index)
            self.powers_line_segment.pop(plant_index)
            if not self.powers_coord:
                self.conn_to_powerstation = False

    def length(self):
        points = self.points.copy()
        return two_pts_dist(points.pop() + (0,), points.pop() + (0,))

    def get_points(self):
        points_copy = self.points.copy()
        return points_copy

