import pygame

pygame.init()


class StatusWindow:
    def __init__(self, x_pos, y_pos, image, player, font=16, color="white"):
        self.player = player
        self.font = pygame.font.SysFont("cambria", font)
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.color = color
        info = list(player.get_info())
        self.nick = self.font.render(info[0], True, color)
        self.funds = self.font.render(info[1], True, color)
        self.status = self.font.render(info[2], True, color)
        self.nick_rect = self.nick.get_rect(center=(self.x_pos, self.y_pos - 20))
        self.funds_rect = self.funds.get_rect(center=(self.x_pos, self.y_pos))
        self.status_rect = self.status.get_rect(center=(self.x_pos, self.y_pos + 20))

    def update_status(self, screen, player, is_dealer=False):
        self.player = player
        info = list(self.player.get_info())
        if is_dealer:
            info[0] = info[0] + " - D"
        self.nick = self.font.render(info[0], True, self.color)
        self.funds = self.font.render(info[1], True, self.color)
        self.status = self.font.render(info[2], True, self.color)
        screen.blit(self.image, self.rect)
        screen.blit(self.nick, self.nick_rect)
        screen.blit(self.funds, self.funds_rect)
        screen.blit(self.status, self.status_rect)
