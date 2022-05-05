import pygame
from backend.PlayerAction import PlayerAction

pygame.init()


def action_to_string(action):
    if action == PlayerAction.FOLD:
        return "FOLD"
    elif action == PlayerAction.CHECK:
        return "CHECK"
    elif action == PlayerAction.CALL:
        return "CALL"
    elif action == PlayerAction.RAISE:
        return "RAISE"
    elif action == PlayerAction.ALL_IN:
        return "ALL IN"


class Button:
    def __init__(self, x_pos, y_pos, image, action, font=40):
        self.action = action
        self.font = pygame.font.SysFont("cambria", font)
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = action_to_string(action)
        self.text = self.font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False

    def update_button(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self):
        is_action = False
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            is_action = True

        return is_action

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, "green")
        else:
            self.text = self.font.render(self.text_input, True, "white")
