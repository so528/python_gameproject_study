import pygame
import random

pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Space Survival Game") # 게임 이름

# FPS
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("C:/Users/risey/OneDrive/바탕 화면/pygame_project/so_project/space.png")

# 우주선 이미지 불러오기
spaceship = pygame.image.load("C:/Users/risey/OneDrive/바탕 화면/pygame_project/so_project/ship.png")
spaceship_size = spaceship.get_rect().size
spaceship_width = int(spaceship_size[0] * 0.5)  # 크기 조절 (50%)
spaceship_height = int(spaceship_size[1] * 0.5)
spaceship = pygame.transform.scale(spaceship, (spaceship_width, spaceship_height))

# 초기 위치 설정
spaceship_x_pos = (screen_width / 2) - (spaceship_width / 2)
spaceship_y_pos = screen_height - spaceship_height

# 이동할 좌표
to_x = 0

# 이동 속도
spaceship_speed = 0.6

# 장애물 이미지 불러오기 및 크기 조절
obstacle = pygame.image.load("C:/Users/risey/OneDrive/바탕 화면/pygame_project/so_project/obstacle.png")
obstacle_width = int(obstacle.get_rect().size[0] * 0.5)
obstacle_height = int(obstacle.get_rect().size[1] * 0.5)
obstacle = pygame.transform.scale(obstacle, (obstacle_width, obstacle_height))

# 여러 장애물 관리
obstacle_speed = 5
num_obstacles = 5
obstacles = []

# 초기 장애물 위치 설정
for i in range(num_obstacles):
    x_pos = random.randint(0, screen_width - obstacle_width)
    y_pos = random.randint(-screen_height, 0)  # 화면 밖에서 생성
    obstacles.append([x_pos, y_pos])  # 각 장애물의 위치를 리스트로 관리

# 점수 변수 추가
score = 0
font = pygame.font.Font(None, 40)

# 이벤트 루프
running = True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= spaceship_speed
            elif event.key == pygame.K_RIGHT:
                to_x += spaceship_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 우주선 위치 업데이트
    spaceship_x_pos += to_x * dt

    # 경계값 처리
    if spaceship_x_pos < 0:
        spaceship_x_pos = 0
    elif spaceship_x_pos > screen_width - spaceship_width:
        spaceship_x_pos = screen_width - spaceship_width

    # 장애물 위치 업데이트 및 점수 증가
    for obstacle_pos in obstacles:
        obstacle_pos[1] += obstacle_speed  # 각 장애물의 y 위치를 업데이트
        # 화면을 벗어나면 다시 위에서 생성
        if obstacle_pos[1] > screen_height:
            obstacle_pos[1] = random.randint(-screen_height, 0)
            obstacle_pos[0] = random.randint(0, screen_width - obstacle_width)
            score += 10  # 장애물을 피했을 때 점수 증가

    # 충돌 처리
    spaceship_rect = spaceship.get_rect()
    spaceship_rect.left = spaceship_x_pos
    spaceship_rect.top = spaceship_y_pos

    # 화면 그리기
    screen.blit(background, (0, 0))
    screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))

    # 장애물 그리기 및 충돌 체크
    for obstacle_pos in obstacles:
        obstacle_rect = obstacle.get_rect(topleft=(obstacle_pos[0], obstacle_pos[1]))
        screen.blit(obstacle, obstacle_pos)  # 각 장애물 그리기

        if spaceship_rect.colliderect(obstacle_rect):  # 충돌 체크
            print("충돌했어요")
            running = False

    # 점수 표시
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

    pygame.display.update()

# 종료 전 대기
pygame.time.delay(2000)
pygame.quit()


