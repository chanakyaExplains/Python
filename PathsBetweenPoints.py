#pip install pygame

import pygame
import math
from collections import defaultdict
from itertools import combinations


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


def generate_edges(n):
    return list(combinations(range(1, n + 1), 2))

def find_paths(graph, current_node, visited_edges, current_path, all_paths):
    all_paths.append(list(current_path))
    
    for neighbor in graph[current_node]:
        edge = (min(current_node, neighbor), max(current_node, neighbor))
        
        if edge not in visited_edges:
            visited_edges.add(edge)
            current_path.append(neighbor)
            find_paths(graph, neighbor, visited_edges, current_path, all_paths)
            current_path.pop()
            visited_edges.remove(edge)

def get_all_paths(graph, n):
    all_paths = []
    
    for start_node in range(1, n + 1):
        visited_edges = set()
        find_paths(graph, start_node, visited_edges, [start_node], all_paths)
    
    return all_paths

def convert_path_to_edges(path):
    edges = []
    for i in range(len(path) - 1):
        edge = (min(path[i], path[i + 1]), max(path[i], path[i + 1]))
        edges.append(edge)
    return edges

def draw_points(n,CENTER_X,CENTER_Y,RADIUS,screen,font):
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = CENTER_X + RADIUS * math.cos(angle)
        y = CENTER_Y + RADIUS * math.sin(angle)
        points.append((x, y))
        pygame.draw.circle(screen, BLUE, (int(x), int(y)), 10)
    
        label = font.render(str(i + 1), True, WHITE)
        screen.blit(label, (x - 10, y - 10))
    return points

def draw_path(path, points,screen):
    for i in range(len(path) - 1):
        start_point = points[path[i] - 1]
        end_point = points[path[i + 1] - 1]
        pygame.draw.line(screen, RED, start_point, end_point, 3)

def draw_buttons(screen,font,next_button_rect,prev_button_rect):
    pygame.draw.rect(screen, GREEN, next_button_rect)
    pygame.draw.rect(screen, GREEN, prev_button_rect)
    next_label = font.render("Next", True, BLACK)
    prev_label = font.render("Prev", True, BLACK)
    screen.blit(next_label, (next_button_rect.x + 10, next_button_rect.y + 10))
    screen.blit(prev_label, (prev_button_rect.x + 10, prev_button_rect.y + 10))

def draw_dropdown(selected_length, lengths,screen,length_dropdown_rect,font):
    pygame.draw.rect(screen, GREEN, length_dropdown_rect)
    dropdown_label = font.render(f"Length: {lengths[selected_length] if lengths else 'N/A'}", True, BLACK)
    screen.blit(dropdown_label, (length_dropdown_rect.x + 10, length_dropdown_rect.y + 10))

def draw_path_number(current, total,screen,font,CENTER_X):
    path_label = font.render(f"Path {current + 1} of {total}", True, WHITE)
    screen.blit(path_label, (CENTER_X - path_label.get_width() // 2, 50))

def main():

    n = 5 
    edges = generate_edges(n)


    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)


    all_paths = get_all_paths(graph, n)


    paths_by_length = defaultdict(list)
    edge_paths_set = set()

    for path in all_paths:
        path_length = len(path) - 1
        edges_in_path = convert_path_to_edges(path)
        sorted_edges = tuple(sorted(edges_in_path)) 

        if sorted_edges not in edge_paths_set: 
            edge_paths_set.add(sorted_edges) 
            paths_by_length[path_length].append(path) 

    lengths = sorted(paths_by_length.keys())
    current_path_index = 0
    selected_length = 0
    total_paths = 0 


    pygame.init()

    WIDTH, HEIGHT = 800,600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Render Paths')

    CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
    RADIUS = 200

    font = pygame.font.SysFont(None, 36)

    next_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT)
    prev_button_rect = pygame.Rect(50, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT)
    length_dropdown_rect = pygame.Rect(300, HEIGHT - 80, 200, BUTTON_HEIGHT)


    running = True

    while running:
        screen.fill(BLACK)

    
        points = draw_points(n,CENTER_X,CENTER_Y,RADIUS,screen,font)

    
        if lengths:
            current_length_paths = paths_by_length[lengths[selected_length]]
            total_paths = len(current_length_paths) 

            if total_paths > 0:
                draw_path(current_length_paths[current_path_index], points,screen)
                draw_path_number(current_path_index, total_paths,screen,font,CENTER_X)

    
        draw_buttons(screen,font,next_button_rect,prev_button_rect)
        draw_dropdown(selected_length, lengths,screen,length_dropdown_rect,font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
            
                if next_button_rect.collidepoint(event.pos):
                    if total_paths > 0:
                        current_path_index = (current_path_index + 1) % total_paths
            
                elif prev_button_rect.collidepoint(event.pos):
                    if total_paths > 0:
                        current_path_index = (current_path_index - 1) % total_paths
            
                elif length_dropdown_rect.collidepoint(event.pos):
                    selected_length = (selected_length + 1) % len(lengths)
                    current_path_index = 0 

        pygame.display.flip()

    pygame.quit()

main()
