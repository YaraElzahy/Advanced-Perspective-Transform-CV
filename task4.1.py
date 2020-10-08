# ______________________________________________    Author: Yara Elzahy    ____________________________________________#
# ______________________________________________     Date: 7/10/2020       ____________________________________________#
# ______________________________________________     Version: 2.0.0        ____________________________________________#
# ______________________________________________     Title: Task 4.2       ____________________________________________#
# _____________________________________________    ~  Description  ~      _____________________________________________#
# __________________This code transforms the perspective of video frames according to any 4 points ____________________#
# ________________________________    chosen by the user by 4 left clicks on the video    _____________________________#
import cv2
import numpy as np
import enum

pts = []
clonepts = []
destination = 0


# perspective transform state
class PERSPECTIVE(enum.Enum):
    WARPED = 1
    NOTWARPED = 0


# set initial state (not warped)
current_state = PERSPECTIVE.NOTWARPED


def rearrange_pts():
    global clonepts
    clonepts = sorted(pts)
    # compare y-coordinates of 2 points with least x-coordinates.
    # The one with the least x & y coordinates is the first point or upper left point (pts[0])
    # The one with the greater y-coordinate is the 3rd point or the lower left point (pts[1])
    if clonepts[0][1] < clonepts[1][1]:
        pts[0] = clonepts[0]
        pts[2] = clonepts[1]
    else:
        pts[2] = clonepts[0]
        pts[0] = clonepts[1]

    # compare y-coordinates of 2 points with highest x-coordinate values.
    # The one with the highest x & y coordinates is the last point or lower right point (pts[3])
    # The one with the lower y-coordinate is the 2nd point or the upper right point (pts[2])
    if clonepts[2][1] > clonepts[3][1]:
        pts[3] = clonepts[2]
        pts[1] = clonepts[3]
    else:
        pts[1] = clonepts[2]
        pts[3] = clonepts[3]

    #print(pts)


def click_event(event, x, y, flags, param):
    # check 3al event hwa anhy event fihom
    global pts, destination, xpts, ypts, clonepts
    if event == cv2.EVENT_LBUTTONDOWN:
        # place a red circle at every clicked position
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        pts.append((x, y))
        print(x, ',', y)
        if len(pts) == 4:
            destination = dynamic_perspective_transform()


def dynamic_perspective_transform():
    global current_state
    rows, cols = frame.shape[0], frame.shape[1]
    # Remember: width = number of columns, and height = number of rows.
    rearrange_pts()
    # store the 4 clicked points in the array pts1
    pts1 = np.float32([pts[0], pts[1], pts[2], pts[3]])

    # store the frame size in the array pts2
    pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [rows, cols]])

    # transform perspective of frame
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(frame, M, (rows, cols))

    # set current state to warped
    current_state = PERSPECTIVE.WARPED

    return dst


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    while True:
        # read frame
        _, frame = cap.read()

        # if the perspective has been transformed in the previous frame,
        # then transform the perspective of this frame too
        if current_state == PERSPECTIVE.WARPED:
            frame = dynamic_perspective_transform()

        # show frame
        cv2.imshow("image", frame)

        # call mouse event on left click
        cv2.setMouseCallback('image', click_event)

        # wait for keystroke
        k = cv2.waitKey(1) & 0xFF

        # if 'esc' or 'q' is pressed, exit and close window
        if (k == 27) or (k == ord('q')):
            break

        # if 'r' is pressed, reset
        if k == ord('r'):
            current_state = PERSPECTIVE.NOTWARPED
            pts = []

    cap.release()
    cv2.destroyAllWindows()
