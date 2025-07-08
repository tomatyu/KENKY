import pygame
import sys

# 初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ピンポンゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# パドル設定
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5

# ボール設定
BALL_SIZE = 20
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# フォント設定
font = pygame.font.SysFont(None, 48)

# プレイヤーのスコア
score_left = 0
score_right = 0

# パドルの初期位置
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# ボールの初期位置
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # スコア表示
    score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力取得
    keys = pygame.key.get_pressed()

    # 左パドル操作 (W, Sキー)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # 右パドル操作 (↑, ↓キー)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # ボール移動
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 上下の壁に当たったら跳ね返る
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # パドルに当たったら跳ね返る
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1

    # 左端にボールが行ったら右のプレイヤーの得点
    if ball.left <= 0:
        score_right += 1
        # ボールを中央に戻す
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    # 右端にボールが行ったら左のプレイヤーの得点
    if ball.right >= WIDTH:
        score_left += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    draw()
    clock.tick(60)
