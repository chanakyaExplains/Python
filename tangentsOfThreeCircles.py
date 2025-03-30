# Dependencies : pygame and math libraries
# run 'pip install pygame' and 'pip install math' in the command prompt before attempting to run program

#radii of the circle are adjustable by grabbing the blue handles
#positions of the circles are adjustable by grabbing within the circles


import pygame
import math

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tangents of three circles")

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen_x_offset = screen_width/2
screen_y_offset = screen_height/2


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)


circles = [
    [-200, -200, 100],
    [0, -100, 50],
    [250, -200, 25]
]


def convert_coords(x, y):
    return (x + screen_x_offset, screen_y_offset - y)

def inverse_convert(x, y):
    return (x - screen_x_offset, screen_y_offset - y)

dragging_circle = None
resizing_circle = None

def is_point_in_circle(px, py, cx, cy, radius):
    return (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2

def find_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1

    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3

    determinant = a1 * b2 - a2 * b1

    if abs(determinant) < 1e-10:
        return None 

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)


def calculate_external_tangents(c1, c2):
    x1, y1, r1 = c1
    x2, y2, r2 = c2

    dx = x2 - x1
    dy = y2 - y1
    d = math.sqrt(dx**2 + dy**2)

    if d < abs(r1 - r2):
        return []


    angle_between_centers = math.atan2(dy, dx)
    angle_offset = math.acos((r1 - r2) / d)

    tangents = []
    for sign in [1, -1]:
        angle = angle_between_centers + sign * angle_offset
        x3 = x1 + r1 * math.cos(angle)
        y3 = y1 + r1 * math.sin(angle)
        x4 = x2 + r2 * math.cos(angle)
        y4 = y2 + r2 * math.sin(angle)

        tangent_dx = x4 - x3
        tangent_dy = y4 - y3
        x3_ext = x3 - 2000 * tangent_dx / d
        y3_ext = y3 - 2000 * tangent_dy / d
        x4_ext = x4 + 2000 * tangent_dx / d
        y4_ext = y4 + 2000 * tangent_dy / d

        tangents.append(((x3_ext, y3_ext), (x4_ext, y4_ext)))

    return tangents


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, (cx, cy, radius) in enumerate(circles):
                cx_screen, cy_screen = convert_coords(cx, cy)
                handle_x, handle_y = convert_coords(cx + radius, cy)
                
                if is_point_in_circle(mouse_x, mouse_y, handle_x, handle_y, 10):
                    resizing_circle = i
                elif is_point_in_circle(mouse_x, mouse_y, cx_screen, cy_screen, radius):
                    dragging_circle = i
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_circle = None
            resizing_circle = None
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if dragging_circle is not None:
                circles[dragging_circle][:2] = inverse_convert(mouse_x, mouse_y)
            elif resizing_circle is not None:
                cx, cy, _ = circles[resizing_circle]
                mouse_cx, mouse_cy = inverse_convert(mouse_x, mouse_y)
                new_radius = int(((mouse_cx - cx) ** 2 + (mouse_cy - cy) ** 2) ** 0.5)
                circles[resizing_circle][2] = max(5, new_radius)

    screen.fill(WHITE)

    for cx, cy, radius in circles:
        pygame.draw.circle(screen, RED, convert_coords(cx, cy), radius, 2)
        handle_pos = convert_coords(cx + radius, cy)
        pygame.draw.circle(screen, BLUE, handle_pos, 10)

    intersections = []

    for i in range(3):
        for j in range(i + 1, 3):
            tangents = calculate_external_tangents(circles[i], circles[j])
            
            if not tangents:
                continue

            for k in range(2):
                p1, p2 = tangents[k]
                pygame.draw.line(screen, GREEN, convert_coords(*p1), convert_coords(*p2), 1)

                p3, p4 = tangents[1 - k]
                intersection = find_intersection(p1, p2, p3, p4)
                if intersection:
                    pygame.draw.circle(screen, ORANGE, convert_coords(*intersection), 5)
                    intersections.append(intersection)

    pygame.display.flip()

pygame.quit()
