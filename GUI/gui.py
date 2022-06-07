import pygame
import os
import sys
import operator
from backend.GameStatus import GameStatus
from backend.PlayerStatus import PlayerStatus
from sympy.solvers import solve
from sympy import Symbol
from GUI.button import Button
from backend.PlayerAction import PlayerAction

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (135, 206, 250)
CARD = (3, 5)


class Gui:
    FPS = 60
    CARD_IMAGE_REDUCTION_VALUE = 10
    pygame.init()

    def __init__(self, width, height, client):
        self.buttons = []
        self.width = width
        self.height = height
        self.placement_of_deck = (self.width // 4.7, self.height // 2.9)
        self.card_size = (self.height // self.CARD_IMAGE_REDUCTION_VALUE, self.width // self.CARD_IMAGE_REDUCTION_VALUE)
        self.button_size = (self.width // 5, self.height // 10)
        self.status_field_size = (self.width // 8, self.height // 6)
        self.cards_overlapping = (self.card_size[0] // 4, self.card_size[1] // 5)
        self.players_coordinates = dict()
        self.farthest_card = (0, 0)
        self.space_between_cards = (self.width // 20, 0)
        self.window = pygame.display.set_mode((width, height))
        self.client = client
        self.dirty_rect = []
        pygame.display.set_caption('Poker Game')

    def add_pot(self):
        pot = None
        if 0 < self.client.game.pot <= 4:
            pot = pygame.image.load(os.path.join('images', 'Chips', '4.png'))
        if 4 < self.client.game.pot <= 12:
            pot = pygame.image.load(os.path.join('images', 'Chips', '12.png'))
        if 12 < self.client.game.pot <= 24:
            pot = pygame.image.load(os.path.join('images', 'Chips', '24.png'))
        if 24 < self.client.game.pot <= 36:
            pot = pygame.image.load(os.path.join('images', 'Chips', '36.png'))
        if 36 < self.client.game.pot <= 48:
            pot = pygame.image.load(os.path.join('images', 'Chips', '48.png'))
        if 48 < self.client.game.pot <= 60:
            pot = pygame.image.load(os.path.join('images', 'Chips', '60.png'))
        if 60 < self.client.game.pot:
            pot = pygame.image.load(os.path.join('images', 'Chips', '72.png')).convert()

        if pot is not None:
            pot_placement = (self.width // 2.3, self.height // 20)
            pot_image_size = self.card_size
            pot = pygame.transform.scale(pot, pot_image_size)
            self.window.blit(pot, pot_placement)

    def add_buttons(self):
        pad = pygame.transform.scale(pygame.image.load(os.path.join('images', 'Buttons', 'button.png')),
                                     self.button_size)
        call_b = Button(self.width // 10, 19 * self.height // 20, pad, PlayerAction.CALL)
        self.buttons.append(call_b)

        fold_b = Button(3 * self.width // 10, 19 * self.height // 20, pad, PlayerAction.FOLD)
        self.buttons.append(fold_b)

        check_b = Button(5 * self.width // 10, 19 * self.height // 20, pad, PlayerAction.CHECK)
        self.buttons.append(check_b)

        raise_b = Button(7 * self.width // 10, 19 * self.height // 20, pad, PlayerAction.RAISE)
        self.buttons.append(raise_b)

        all_in_b = Button(9 * self.width // 10, 19 * self.height // 20, pad, PlayerAction.ALL_IN)
        self.buttons.append(all_in_b)

        for button in self.buttons:
            self.dirty_rect.append(button.text_rect)
            self.dirty_rect.append(button.rect)

    def redraw_window(self):
        self.window.fill(WHITE)
        self.add_table()
        self.add_deck()
        if self.client.game is None:
            pygame.display.update()
            return

        if len(self.players_coordinates) > 0:
            self.draw_hole_cards()
            self.show_statuses()

        for card in self.client.game.community_cards:
            self.add_card(card)
        self.add_pot()

        pygame.display.update()

    def add_table(self, table='BLUE'):
        if table == 'BLUE':
            table_layout = pygame.image.load(os.path.join('images', 'Tables', 'table1.png')).convert()
        elif table == 'RED':
            table_layout = pygame.image.load(os.path.join('images', 'Tables', 'table2.png')).convert()
        table_layout = pygame.transform.scale(table_layout, (self.width, self.height))
        self.window.blit(table_layout, (0, 0))

    def get_scaled_reverse(self, reverse):
        if reverse == 'RED':
            deck = pygame.image.load(os.path.join('images', 'Reverses', '4.png')).convert()
        elif reverse == 'BLUE':
            deck = pygame.image.load(os.path.join('images', 'Reverses', '1.png')).convert()
        deck = pygame.transform.scale(deck, self.card_size)
        return deck

    def add_deck(self, reverse='RED'):
        deck = self.get_scaled_reverse(reverse)
        self.window.blit(deck, self.placement_of_deck)
        self.farthest_card = (self.placement_of_deck[0] + self.card_size[0], self.placement_of_deck[1])

    def find_next_point_on_ellipse(self, a, b, point, distance_between_points):
        x = Symbol('x')
        y = Symbol('y')
        coordinates_for_ellipse = (point[0] - self.width / 2, -point[1] + self.height / 2)
        solution_x = solve(distance_between_points + coordinates_for_ellipse[0] - x, x)
        solution_x = solution_x[0]
        if solution_x > a:
            return
        solution_y = solve(solution_x ** 2 / a ** 2 + y ** 2 / b ** 2 - 1, y)
        if solution_y[0] <= 0:
            solution_y = solution_y[0]
        else:
            solution_y = solution_y[1]

        return solution_x + self.width / 2, -solution_y + 2 * self.height / 6

    def adjust_card_coordinates(self, position):
        return (position[0] + self.cards_overlapping[0],
                position[1] + self.cards_overlapping[1])

    def calc_cards_coordinates(self):
        a, b = (7 * self.width // 8) / 2, (4 * self.height // 6) / 2  # to not be too close to the edges of the board
        distance_between_players = 2 * a / (self.client.game.players.number_of_players - 1)
        start_position = ((self.width - 2 * a) / 2,
                          2 * self.height / 6)

        for player in self.client.game.players.list:
            self.players_coordinates[player.name] = start_position
            start_position = self.find_next_point_on_ellipse(a, b, start_position, distance_between_players)

    def draw_hole_cards(self, reverse='RED'):
        for player in self.client.game.players.list:
            if player.name == self.client.player_id or \
                    (self.client.game.status >= GameStatus.SHOWDOWN and player.status is not PlayerStatus.OUT):
                card = pygame.image.load(player.hole_cards[0].get_path_to_image()).convert()
                card = pygame.transform.scale(card, self.card_size)
            else:
                card = self.get_scaled_reverse(reverse)

            pos_first_card = self.players_coordinates[player.name]
            self.window.blit(card, pos_first_card)

            if player.name == self.client.player_id or \
                    (self.client.game.status >= GameStatus.SHOWDOWN and player.status is not PlayerStatus.OUT):
                card = pygame.image.load(player.hole_cards[1].get_path_to_image()).convert()
                card = pygame.transform.scale(card, self.card_size)
            else:
                card = self.get_scaled_reverse(reverse)

            pos_second_card = self.adjust_card_coordinates(pos_first_card)
            self.window.blit(card, pos_second_card)

    def show_statuses(self):
        font = pygame.font.Font("freesansbold.ttf", int(0.1 * self.card_size[1]))
        info = font.render(self.client.game.status.name + " "
                                                          "Current player: " + self.client.game.players.current_player.name + " " +
                           " In pot = " + str(self.client.game.pot) + " " +
                           " On the table = " + str(self.client.game.on_the_table) + " " +
                           " Current raise = " + str(self.client.game.current_raise),
                           True,
                           WHITE)
        self.window.blit(info, (0, 0))
        for player in self.client.game.players.list:
            information = list(player.get_info())
            for info in information:
                i = len(information) - information.index(info)

                if player == self.client.game.players.current_player:
                    info = font.render(info, True, BLUE)
                else:
                    info = font.render(info, True, RED)

                coordinates_of_player = self.players_coordinates[player.name][0], \
                                        (1 - i * 0.1) * self.players_coordinates[player.name][1]
                self.window.blit(info, coordinates_of_player)

    def add_card(self, card, card_placement=None):
        if card is None:
            return
        card = pygame.image.load(card.get_path_to_image()).convert()
        card = pygame.transform.scale(card, self.card_size)
        if card_placement is None:
            card_placement = tuple(map(operator.add, self.farthest_card, self.space_between_cards))
            self.farthest_card = (card_placement[0] + self.card_size[0], card_placement[1])
        self.window.blit(card, card_placement)

    def run(self):
        run = True
        self.redraw_window()
        self.add_buttons()
        while run:
            while self.client.game is None:
                pygame.time.delay(500)
            if len(self.players_coordinates) == 0:
                self.calc_cards_coordinates()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.client.game.players.current_player.name == self.client.player_id\
                        and self.client.game.status >= GameStatus.PREFLOP:
                    for button in self.buttons:
                        if button.checkForInput():
                            self.client.send(button.action)

            for button in self.buttons:
                button.changeColor()
                button.update_button(self.window)

            pygame.display.update(self.dirty_rect)

            if self.client.to_update:
                self.redraw_window()
                self.client.to_update = False

        pygame.quit()
        sys.exit()
