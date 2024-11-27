# dependancies :   run in command prompt 'pip install pygame'

import pygame
import math


pygame.init()


windowInformation = pygame.display.Info()
width, height = windowInformation.current_w, windowInformation.current_h


screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Tangents to Circle")


center = (width // 2, height // 2)
radius = 150
Point = [width // 3, height // 3]


tangentLength = math.sqrt(width * width + height * height)


def getTangentLines(Point, center, radius, tangentLength):
    x1, y1 = Point
    xc, yc = center
    dx = x1 - xc
    dy = y1 - yc
    distance = math.sqrt(dx**2 + dy**2)

    angle = math.atan2(dy, dx)

    relativeAngleOffset = math.asin(radius / distance)

    angle1 = angle - relativeAngleOffset
    angle2 = angle + relativeAngleOffset

    tangent1direction = (math.cos(angle1), math.sin(angle1))
    tangent2direction = (math.cos(angle2), math.sin(angle2))

    tangent1End = (
        x1 - tangent1direction[0] * tangentLength,
        y1 - tangent1direction[1] * tangentLength,
    )
    tangent2End = (
        x1 - tangent2direction[0] * tangentLength,
        y1 - tangent2direction[1] * tangentLength,
    )

    return tangent1End, tangent2End


def draw_slider(x, y, width, height, value, minValue, maxValue):
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))

    handleX = x + (value - minValue) / (maxValue - minValue) * width
    pygame.draw.circle(
        screen, (0, 0, 255), (int(handleX), y + height // 2), height // 2
    )


running = True
isdragging = False
isdraggingSlider = False
sliderx, slidery, sliderWidth, sliderHeight = (
    width // 4,
    height - 100,
    width // 2,
    20,
)
minRadius, maxRadius = 5, 300

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouseX, mouseY = pygame.mouse.get_pos()

                if (
                    abs(mouseX - Point[0]) < 10
                    and abs(mouseY - Point[1]) < 10
                ):
                    isdragging = True

                if (
                    sliderx <= mouseX <= sliderx + sliderWidth
                    and slidery <= mouseY <= slidery + sliderHeight
                ):
                    isdraggingSlider = True

        if event.type == pygame.MOUSEMOTION:
            if isdragging:
                Point[0], Point[1] = pygame.mouse.get_pos()
            if isdraggingSlider:
                mouseX, _ = pygame.mouse.get_pos()

                newRadius = minRadius + (mouseX - sliderx) / sliderWidth * (
                    maxRadius - minRadius
                )
                radius = max(min(newRadius, maxRadius), minRadius)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                isdragging = False
                isdraggingSlider = False

    distanceToCenter = math.sqrt(
        (Point[0] - center[0]) ** 2 + (Point[1] - center[1]) ** 2
    )

    if distanceToCenter > radius:

        tangent1End, tangent2End = getTangentLines(
            Point, center, radius, tangentLength
        )

        pygame.draw.line(screen, (0, 255, 0), Point, tangent1End, 2)
        pygame.draw.line(screen, (0, 255, 0), Point, tangent2End, 2)

    pygame.draw.circle(screen, (0, 0, 255), center, radius, 2)

    pygame.draw.circle(screen, (255, 0, 0), Point, 8)

    draw_slider(
        sliderx, slidery, sliderWidth, sliderHeight, radius, minRadius, maxRadius
    )

    pygame.display.flip()


pygame.quit()
