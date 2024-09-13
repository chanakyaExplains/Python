import pygame
import pygame_gui
import math

import pygame_gui.ui_manager

pygame.init()
pygame.display.set_caption("Pygame 3D Renderer")

info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)

manager = pygame_gui.UIManager((screenWidth, screenHeight))

clock = pygame.time.Clock()

BackgroundColor = (255, 255, 255)
RenderColor = (0, 0, 0)

sliderWidth = screenWidth * 0.2
sliderHeight = 40
sliderOffset = screenWidth * 0.8

xAxisRotationSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((sliderOffset, 50), (sliderWidth, sliderHeight)),
    start_value=0,
    value_range=(-50.0, 50.0),
    manager=manager
)

xAxisRotationLabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((sliderOffset, 90), (sliderWidth, 30)),
    text="Rotate X: 0.0",
    manager=manager
)

xAxisReset = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((sliderOffset, 100), (70, 30)),
    text="Reset",
    manager=manager
)

yAxisRotationSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((sliderOffset, 150), (sliderWidth, sliderHeight)),
    start_value=0,
    value_range=(-50.0, 50.0),
    manager=manager
)

yAxisRotationLabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((sliderOffset, 190), (sliderWidth, 30)),
    text="Rotate Y: 0.0",
    manager=manager
)

yAxisReset = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((sliderOffset, 200), (70, 30)),
    text="Reset",
    manager=manager
)

zAxisRotationSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((sliderOffset, 250), (sliderWidth, sliderHeight)),
    start_value=0,
    value_range=(-50.0, 50.0),
    manager=manager
)

zAxisRotationLabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((sliderOffset, 290), (sliderWidth, 30)),
    text="Rotate Z: 0.0",
    manager=manager
)

zAxisReset = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((sliderOffset, 300), (70, 30)),
    text="Reset",
    manager=manager
)

projectionAngleSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((sliderOffset, 350), (sliderWidth, sliderHeight)),
    start_value=0, 
    value_range=(0, 180),
    manager=manager
)

projectionAngleDisplay = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((sliderOffset, 390), (sliderWidth, 30)),
    text="Theta: 0°",
    manager=manager
)

scaleSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((sliderOffset, 450), (sliderWidth, sliderHeight)),
    start_value=1.0, 
    value_range=(0.1, 5.0),
    manager=manager
)

scaleLabel = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((sliderOffset, 490), (sliderWidth, 30)),
    text="Scale: 1.0",
    manager=manager
)

toggleEdges = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((sliderOffset, 550), (100, 50)),
    text="Toggle edges",
    manager=manager
)

togglePoints = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((sliderOffset+150, 550), (100, 50)),
    text="Toggle sides",
    manager=manager
)

def rotate(Points3D, xRotation, yRotation, zRotation):

    sinX = math.sin(xRotation)
    sinY = math.sin(yRotation)
    sinZ = math.sin(zRotation)

    cosX = math.cos(xRotation)
    cosY = math.cos(yRotation)
    cosZ = math.cos(zRotation)
    
    rotatedPoints = []
    
    for x, y, z in Points3D:
    
        y1 = y * cosX - z * sinX
        z1 = y * sinX + z * cosX
    
        x1 = x * cosY + z1 * sinY
        z2 = -x * sinY + z1 * cosY
    
        x2 = x1 * cosZ - y1 * sinZ
        y2 = x1 * sinZ + y1 * cosZ

        rotatedPoints.append((x2, y2, z2))
    
    return rotatedPoints

def obliqueprojection(Points3D, projectionAngle=0):
    projectionAngleRad = math.radians(projectionAngle)
    Points2D = []
    for x, y, z in Points3D:
        xProjected = x + z * math.cos(projectionAngleRad)
        yProjected = y + z * math.sin(projectionAngleRad)
        Points2D.append((xProjected, yProjected))
    return Points2D


Object3DPoints = [
   (1, 1, 1), (-1, 1, 1), (1, -1, 1), (-1, -1, 1),(1, 1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1),(0, 1.618, 0.618), (0, -1.618, 0.618), (0, 1.618, -0.618), (0, -1.618, -0.618),(0.618, 0, 1.618), (-0.618, 0, 1.618), (0.618, 0, -1.618), (-0.618, 0, -1.618),(1.618, 0.618, 0), (-1.618, 0.618, 0), (1.618, -0.618, 0), (-1.618, -0.618, 0) 
]

Object3DEdges = [(0, 8), (0, 12), (0, 16), (1, 8), (1, 13), (1, 17), (2, 9), (2, 12), (2, 18), (3, 9), (3, 13), (3, 19), (4, 10), (4, 14), (4, 16), (5, 10), (5, 15), (5, 17), (6, 11), (6, 14), (6, 18), (7, 11), (7, 15), (7, 19), (8, 0), (8, 1), (8, 10), (9, 2), (9, 3), (9, 11), (10, 4), (10, 5), (10, 8), (11, 6), (11, 7), (11, 9), (12, 0), (12, 2), (12, 13), (13, 1), (13, 3), (13, 12), (14, 4), (14, 6), (14, 15), (15, 5), (15, 7), (15, 14), (16, 0), (16, 4), (16, 18), (17, 1), (17, 5), (17, 19), (18, 2), (18, 6), (18, 16), (19, 3), (19, 7), (19, 17)]

rotationAngleX = 0
rotationAngleY = 0
rotationAngleZ = 0
rotationSpeedX = 0 
rotationSpeedY = 0 
rotationSpeedZ = 0 
projectionAngle = 0 
scaleFactor = 1.0 
renderEdges = True
renderPoints = True

running = True
while running:
    timedelta = clock.tick(60) / 1000.0
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == xAxisRotationSlider:
                    rotationSpeedX = event.value
                    xAxisRotationLabel.set_text(f"Rotate X: {int(rotationSpeedX)}")
                elif event.ui_element == yAxisRotationSlider:
                    rotationSpeedY = event.value
                    yAxisRotationLabel.set_text(f"Rotate Y: {int(rotationSpeedY)}")
                elif event.ui_element == zAxisRotationSlider:
                    rotationSpeedZ = event.value
                    zAxisRotationLabel.set_text(f"Rotate Z: {int(rotationSpeedZ)}")
                elif event.ui_element == projectionAngleSlider:
                    projectionAngle = event.value
                    projectionAngleDisplay.set_text(f"Theta: {int(projectionAngle)}°")
                elif event.ui_element == scaleSlider:
                    scaleFactor = event.value
                    scaleLabel.set_text(f"Scale: {round(scaleFactor,1)}")
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == toggleEdges:
                    renderEdges = not renderEdges
                elif event.ui_element == togglePoints:
                    renderPoints = not renderPoints
                elif event.ui_element == xAxisReset:
                    rotationSpeedX = 0
                    xAxisRotationLabel.set_text(f"Rotate X: {int(rotationSpeedX)}")
                    xAxisRotationSlider.set_current_value(0)
                elif event.ui_element == yAxisReset:
                    rotationSpeedY = 0
                    yAxisRotationLabel.set_text(f"Rotate Y: {int(rotationSpeedY)}")
                    yAxisRotationSlider.set_current_value(0)
                elif event.ui_element == zAxisReset:
                    rotationSpeedZ = 0
                    zAxisRotationLabel.set_text(f"Rotate Z: {int(rotationSpeedZ)}")
                    zAxisRotationSlider.set_current_value(0)

    
        manager.process_events(event)


    manager.update(timedelta)


    screen.fill(BackgroundColor)
    

    rotationAngleX = (rotationAngleX + rotationSpeedX * timedelta) % 360
    rotationAngleY = (rotationAngleY + rotationSpeedY * timedelta) % 360
    rotationAngleZ = (rotationAngleZ + rotationSpeedZ * timedelta) % 360


    scaledObject3DPoints = [(x * scaleFactor, y * scaleFactor, z * scaleFactor) for x, y, z in Object3DPoints]
    

    rotatedObject3DPoints = rotate(scaledObject3DPoints, math.radians(rotationAngleX), math.radians(rotationAngleY), math.radians(rotationAngleZ))
    

    projected2DPoints = obliqueprojection(rotatedObject3DPoints, projectionAngle=projectionAngle)
    

    def toscreencoords(points2d, scale=100, offset=(screenWidth * 0.8 / 2, screenHeight / 2)):
        return [(int(x * scale + offset[0]), int(y * scale + offset[1])) for x, y in points2d]
    
    screenPoints = toscreencoords(projected2DPoints)
    
    if renderPoints:
        for point in screenPoints:
            pygame.draw.circle(screen, RenderColor,point,5.0)

    if renderEdges:
        for edge in Object3DEdges:
            startpoint = screenPoints[edge[0]]
            endpoint = screenPoints[edge[1]]
            pygame.draw.line(screen, RenderColor, startpoint, endpoint, 1)


    manager.draw_ui(screen)
    

    pygame.display.flip()

pygame.quit()
