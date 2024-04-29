import pygame
pygame.init()
WIN = pygame.display.set_mode((700,500))
pygame.display.set_caption("game5")
SF = pygame.font.SysFont("kranky", 50)
class Paddle:
    COLOR = (0, 0, 0)
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win): pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up: self.y -= self.VEL
        else: self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
class Ball:
    MAX_VEL = 5
    COLOR1 = (0, 0, 0)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR1, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
def draw(win, paddles, ball, left_score, right_score):
    win.fill((255, 255, 230))

    left_score_text = SF.render(f"{left_score}", 1, (255, 192, 203))
    right_score_text = SF.render(f"{right_score}", 1, (255, 192, 203))
    win.blit(left_score_text, (175 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (525 - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, 500, 25):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, (0, 0, 0), (345, i, 10, 25))

    ball.draw(win)
    pygame.display.update()
def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= 500: ball.y_vel *= -1
    elif ball.y - ball.radius <= 0: ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
def movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= 500: left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0: right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= 500: right_paddle.move(up=False)
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10,200,20,100)
    right_paddle = Paddle(670,200,20,100)
    ball = Ball(350,250,7)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(60)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        movement(keys, left_paddle, right_paddle)

        ball.move()
        collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > 700:
            left_score += 1
            ball.reset()

        if left_score >= 10:
            text = SF.render("LW", 1, (255, 0, 0))
            WIN.blit(text, (350 - text.get_width() //2, 250 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        if right_score >= 10:
            text = SF.render("RW", 1, (255, 0, 0))
            WIN.blit(text, (350 - text.get_width() //2, 250 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()
if __name__ == '__main__': main()