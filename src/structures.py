class NetworkTree:

    goal_func = 0
    segments = []

    def __init__(self):
        self.segments = []

    def count_goal_func(self):
        print "Count goal_func"

    def addNewSegment(self, lineSegment):
        self.segments.append(lineSegment)

class LineSegment:

    conn_to_powerstation = False
    powers_line_segment_len = 0
    powers_coord = ()

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2


    # x1, y1
    # x2, y2
    # px, py - powerstation locations