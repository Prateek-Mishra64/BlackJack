import arcade
from arcade.gui import (
    UIFlatButton,
    UILabel,
    UIManager,
    UIMessageBox,
    UIOnActionEvent,
    UITextureButton,
)

from logic import DealerAI, calculate_score, deal_card, deck, reset_deck


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background_texture = arcade.Sprite("Assets/Sprites/main menu.png")
        self.background_list = arcade.SpriteList()
        scale_x = self.window.width / self.background_texture.width
        scale_y = self.window.height / self.background_texture.height
        self.background_texture.scale = max(scale_x, scale_y)
        self.background_texture.center_x = self.window.width // 2
        self.background_texture.center_y = self.window.height // 2
        self.title = arcade.Sprite("Assets/Sprites/title.png")
        self.title.center_x = self.window.width // 2
        self.title.center_y = self.window.height // 2 + 100

        self.background_list.append(self.background_texture)
        self.background_list.append(self.title)

        self.play_button = self.make_button(
            340,
            470,
            200,
            75,
            self.show_message,
            arcade.load_texture("Assets/Sprites/play.png"),
            arcade.load_texture("Assets/Sprites/play_hovered.png"),
            arcade.load_texture("Assets/Sprites/play_clicked.png"),
        )
        self.ui_manager.add(self.play_button)

        self.rules_button = self.make_button(
            1450,
            460,
            200,
            75,
            self.show_rules,
            arcade.load_texture("Assets/Sprites/rules_idle.png"),
            arcade.load_texture("Assets/Sprites/rules_hover.png"),
            arcade.load_texture("Assets/Sprites/rules_clicked.png"),
        )
        self.ui_manager.add(self.rules_button)

        self.contact_button = self.make_button(
            320,
            160,
            180,
            75,
            self.show_contacts,
            arcade.load_texture("Assets/Sprites/contact_idle.png"),
            arcade.load_texture("Assets/Sprites/contact_hover.png"),
            arcade.load_texture("Assets/Sprites/contact_clicked.png"),
        )
        self.ui_manager.add(self.contact_button)

        self.quit_button = self.make_button(
            1450,
            130,
            200,
            75,
            lambda e: arcade.exit(),
            arcade.load_texture("Assets/Sprites/quit_idle.png"),
            arcade.load_texture("Assets/Sprites/quit_hover.png"),
            arcade.load_texture("Assets/Sprites/quit_clicked.png"),
        )
        self.ui_manager.add(self.quit_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            # Remove the box from the UI
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

    def make_button(
        self,
        x,
        y,
        width,
        height,
        callback,
        texture,
        texture_hovered,
        texture_pressed,
    ):
        button = UITextureButton(
            width=width,
            height=height,
            x=x,
            y=y,
            texture=texture,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT,),
        )
        button.on_click = callback
        return button

    def show_message(self, event):
        self.ui_manager.add(self.messagebox)

    def show_rules(self, event):
        self.window.show_view(RulesView())

    def show_contacts(self, event):
        self.window.show_view(ContactUs())

    def on_ui_event(self, event):
        if event.source == self.messagebox:
            if event.button.text == "Beginner":
                self.ui_manager.remove(self.messagebox)
                self.show_beginner(self)
            elif event.button.text == "Experienced":
                self.ui_manager.remove(self.messagebox)
                self.show_experienced(self)
            elif event.button.text == "Expert":
                self.ui_manager.remove(self.messagebox)
                self.show_expert(self)

    def show_beginner(self, event):
        self.window.show_view(EasyMode())

    def show_experienced(self, event):
        self.window.show_view(ModerateMode())

    def show_expert(self, event):
        self.window.show_view(HardMode())

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.ui_manager.draw()


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        self.rules_label = UILabel(
            x=50,
            y=700,
            text="The Rules are simple: You and the dealer each get 2 cards. Dealer shows one card. Try to beat dealer without going over 21.",
            font_size=20,
            text_color=arcade.color.TEAL,
            width=1800,
            multiline=True,
        )
        self.ui_manager.add(self.rules_label)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.back_to_menu
        self.ui_manager.add(back_button)

    def back_to_menu(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class ContactUs(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        self.contact_us = UILabel(
            x=500,
            y=700,
            text="Prateek and Himesh",
            font_size=40,
            text_color=arcade.color.ALIZARIN_CRIMSON,
            multiline=True,
            bold=True,
        )

        self.ui_manager.add(self.contact_us)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_contact
        self.ui_manager.add(back_button)

    def menu_contact(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


#################EASY MODE##################################################


class EasyMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background = arcade.Sprite("Assets/Sprites/table.png")

        self.dealer_sprites = arcade.SpriteList()
        self.player_sprites = arcade.SpriteList()
        self.resolt = arcade.SpriteList()
        reset_deck()

        self.easy_ui = arcade.SpriteList()
        scale_x = self.window.width / self.background.width
        scale_y = self.window.height / self.background.height
        self.background.scale = max(scale_x, scale_y)
        self.background.center_x = self.window.width // 2
        self.background.center_y = self.window.height // 2

        self.easy_ui.append(self.background)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_easy
        self.ui_manager.add(back_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

        self.ai = DealerAI("easy")

        hit_button = UITextureButton(
            x=self.window.width // 2 - 120,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/hit.png"),
        )
        hit_button.on_click = self.hit_action
        self.ui_manager.add(hit_button)

        stand_button = UITextureButton(
            x=self.window.width // 2 + 20,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/stand.png"),
        )
        stand_button.on_click = self.stand_action
        self.ui_manager.add(stand_button)

        self.player_hand = []
        self.dealer_hand = []

        self.draw_player_card()
        self.draw_player_card()

        self.draw_dealer_card()
        self.draw_dealer_card()

    def arrange_cards(self):
        spacing = 300
        start_x = 200
        y = 300
        for i, sprite in enumerate(self.player_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

        spacing = 300
        start_x = 200
        y = 800
        for i, sprite in enumerate(self.dealer_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

    def draw_player_card(self):
        suit, rank = deal_card()
        self.player_hand.append((suit, rank))
        card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.player_sprites.append(sprite)
        self.arrange_cards()

    def draw_dealer_card(self):
        suit, rank = deal_card()
        self.dealer_hand.append((suit, rank))

        if len(self.dealer_hand) == 1:
            card_path = "Assets/Sprites/card-back.png"
        else:
            card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.dealer_sprites.append(sprite)

        self.arrange_cards()

    def hit_action(self, event):
        score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)
        if dealer_score >= 21:
            result = arcade.Sprite("Assets/Sprites/win.png", scale=2)
            result.center_x = self.window.width // 2
            result.center_y = self.window.height // 2 + 300
            self.resolt.append(result)
        else:
            if score >= 21:
                result = arcade.Sprite("Assets/Sprites/lose.png", scale=2)
                result.center_x = self.window.width // 2
                result.center_y = self.window.height // 2 + 100
                self.resolt.append(result)

            elif score < 21:
                if score > dealer_score:
                    result = arcade.Sprite("Assets/Sprites/win.png")
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                elif score < dealer_score:
                    result = arcade.Sprite("Assets/Sprites/lose.png", scale=4)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                else:
                    result = arcade.Sprite("Assets/Sprites/tie.jpg", scale=5)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)

    def stand_action(self, event):
        self.draw_player_card()
        dealer_score = calculate_score(self.dealer_hand)
        player_score = calculate_score(self.player_hand)

        if player_score >= 21:
            result = arcade.Sprite("Assets/Sprites/lose.png")
            result.center_x = self.window.width // 2
            result.center_y = self.window.height // 2 + 300
            self.easy_ui.append(result)
            return

        while True:
            action = self.ai.choose_action(self.dealer_hand, self.player_hand)

            if action == 1:
                if len(deck) == 0:
                    break
                self.draw_dealer_card()
                dealer_score = calculate_score(self.dealer_hand)
                if dealer_score >= 21:
                    result = arcade.Sprite("Assets/Sprites/win.png")
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 300
                    self.easy_ui.append(result)
                    return
            else:
                break

            dealer_score = calculate_score(self.dealer_hand)
            player_score = calculate_score(self.player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            result_path = "Assets/Sprites/win.png"
        elif dealer_score > player_score:
            result_path = "Assets/Sprites/lose.png"
        else:
            result_path = "Assets/Sprites/tie.jpg"

        result = arcade.Sprite(result_path)
        result.center_x = self.window.width // 2
        result.center_y = self.window.height // 2 + 300
        self.easy_ui.append(result)

    def card_map(self, suit_number, rank_number):
        suit_name = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades"}
        suit = suit_name[suit_number]

        rank = str(rank_number)

        return f"Assets/Sprites/Cards/card-{suit}-{rank}.png"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_messagebox(None)

    def show_messagebox(self, event):
        self.ui_manager.add(self.messagebox)

    def menu_easy(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.easy_ui.draw(pixelated=12)
        self.player_sprites.draw()
        self.dealer_sprites.draw()
        self.ui_manager.draw()
        self.resolt.draw()


#################MODERATE MODE##################################################


class ModerateMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background = arcade.Sprite("Assets/Sprites/table.png")

        self.dealer_sprites = arcade.SpriteList()
        self.player_sprites = arcade.SpriteList()
        self.resolt = arcade.SpriteList()
        reset_deck()

        self.moderate_ui = arcade.SpriteList()
        scale_x = self.window.width / self.background.width
        scale_y = self.window.height / self.background.height
        self.background.scale = max(scale_x, scale_y)
        self.background.center_x = self.window.width // 2
        self.background.center_y = self.window.height // 2

        self.moderate_ui.append(self.background)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_easy
        self.ui_manager.add(back_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

        self.ai = DealerAI("medium")

        hit_button = UITextureButton(
            x=self.window.width // 2 - 120,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/hit.png"),
        )
        hit_button.on_click = self.hit_action
        self.ui_manager.add(hit_button)

        stand_button = UITextureButton(
            x=self.window.width // 2 + 20,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/stand.png"),
        )
        stand_button.on_click = self.stand_action
        self.ui_manager.add(stand_button)

        self.player_hand = []
        self.dealer_hand = []

        self.draw_player_card()
        self.draw_player_card()

        self.draw_dealer_card()
        self.draw_dealer_card()

    def arrange_cards(self):
        spacing = 300
        start_x = 200
        y = 300
        for i, sprite in enumerate(self.player_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

        spacing = 300
        start_x = 200
        y = 800
        for i, sprite in enumerate(self.dealer_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

    def draw_player_card(self):
        suit, rank = deal_card()
        self.player_hand.append((suit, rank))
        card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.player_sprites.append(sprite)
        self.arrange_cards()

    def draw_dealer_card(self):
        suit, rank = deal_card()
        self.dealer_hand.append((suit, rank))

        if len(self.dealer_hand) == 1:
            card_path = "Assets/Sprites/card-back.png"
        else:
            card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.dealer_sprites.append(sprite)

        self.arrange_cards()

    def hit_action(self, event):
        score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)
        if dealer_score >= 21:
            result = arcade.Sprite("Assets/Sprites/win.png", scale=2)
            result.center_x = self.window.width // 2
            result.center_y = self.window.height // 2 + 300
            self.resolt.append(result)
        else:
            if score >= 21:
                result = arcade.Sprite("Assets/Sprites/lose.png", scale=2)
                result.center_x = self.window.width // 2
                result.center_y = self.window.height // 2 + 100
                self.resolt.append(result)

            elif score < 21:
                if score > dealer_score:
                    result = arcade.Sprite("Assets/Sprites/win.png")
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                elif score < dealer_score:
                    result = arcade.Sprite("Assets/Sprites/lose.png", scale=4)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                else:
                    result = arcade.Sprite("Assets/Sprites/tie.jpg", scale=5)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)

    def stand_action(self, event):
        while True:
            dealer_score = calculate_score(self.dealer_hand)
            player_score = calculate_score(self.player_hand)
            action = self.ai.choose_action(self.dealer_hand, self.player_hand)

            if action == 1:
                self.draw_dealer_card()
                self.draw_player_card()
            else:
                break

        player_score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)

        result = arcade.Sprite("Assets/Sprites/Cards/Joker-alt.jpg", scale=2)

        if dealer_score > 21 or player_score > dealer_score:
            result_path = "Assets/Sprites/win.png"
        elif dealer_score > player_score:
            result_path = "Assets/Sprites/lose.png"
        else:
            result_path = "Assets/Sprites/tie.jpg"

        result.texture = arcade.load_texture(result_path)
        result.center_x = self.window.width // 2
        result.center_y = self.window.height // 2 + 300
        self.resolt.append(result)

    def card_map(self, suit_number, rank_number):
        suit_name = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades"}
        suit = suit_name[suit_number]

        rank = str(rank_number)

        return f"Assets/Sprites/Cards/card-{suit}-{rank}.png"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_messagebox(None)

    def show_messagebox(self, event):
        self.ui_manager.add(self.messagebox)

    def menu_easy(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.moderate_ui.draw(pixelated=12)
        self.player_sprites.draw()
        self.dealer_sprites.draw()
        self.ui_manager.draw()
        self.resolt.draw()


#################HARD MODE##################################################


class HardMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background = arcade.Sprite("Assets/Sprites/table.png")

        self.dealer_sprites = arcade.SpriteList()
        self.player_sprites = arcade.SpriteList()
        self.resolt = arcade.SpriteList()
        reset_deck()

        self.hard_ui = arcade.SpriteList()
        scale_x = self.window.width / self.background.width
        scale_y = self.window.height / self.background.height
        self.background.scale = max(scale_x, scale_y)
        self.background.center_x = self.window.width // 2
        self.background.center_y = self.window.height // 2

        self.hard_ui.append(self.background)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_easy
        self.ui_manager.add(back_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

        self.ai = DealerAI("hard")

        hit_button = UITextureButton(
            x=self.window.width // 2 - 120,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/hit.png"),
        )
        hit_button.on_click = self.hit_action
        self.ui_manager.add(hit_button)

        stand_button = UITextureButton(
            x=self.window.width // 2 + 20,
            y=self.window.height // 2,
            width=150,
            height=80,
            texture=arcade.load_texture("Assets/Sprites/stand.png"),
        )
        stand_button.on_click = self.stand_action
        self.ui_manager.add(stand_button)
        stand_button.on_click = self.stand_action
        self.ui_manager.add(stand_button)

        self.ai = DealerAI("hard")
        self.player_hand = []
        self.dealer_hand = []

        self.draw_player_card()
        self.draw_player_card()

        self.draw_dealer_card()
        self.draw_dealer_card()

    def arrange_cards(self):
        spacing = 300
        start_x = 200
        y = 300
        for i, sprite in enumerate(self.player_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

        spacing = 300
        start_x = 200
        y = 800
        for i, sprite in enumerate(self.dealer_sprites):
            sprite.center_x = start_x + spacing * i
            sprite.center_y = y

    def draw_player_card(self):
        suit, rank = deal_card()
        self.player_hand.append((suit, rank))
        card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.player_sprites.append(sprite)
        self.arrange_cards()

    def draw_dealer_card(self):
        suit, rank = deal_card()
        self.dealer_hand.append((suit, rank))

        if len(self.dealer_hand) == 1:
            card_path = "Assets/Sprites/card-back.png"
        else:
            card_path = self.card_map(suit, rank)

        sprite = arcade.Sprite(card_path, scale=3)
        self.dealer_sprites.append(sprite)

        self.arrange_cards()

    def hit_action(self, event):
        score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)
        if dealer_score >= 21:
            result = arcade.Sprite("Assets/Sprites/win.png", scale=2)
            result.center_x = self.window.width // 2
            result.center_y = self.window.height // 2 + 300
            self.resolt.append(result)
        else:
            if score >= 21:
                result = arcade.Sprite("Assets/Sprites/lose.png", scale=2)
                result.center_x = self.window.width // 2
                result.center_y = self.window.height // 2 + 100
                self.resolt.append(result)

            elif score < 21:
                if score > dealer_score:
                    result = arcade.Sprite("Assets/Sprites/win.png")
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                elif score < dealer_score:
                    result = arcade.Sprite("Assets/Sprites/lose.png", scale=4)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)
                else:
                    result = arcade.Sprite("Assets/Sprites/tie.jpg", scale=5)
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 100
                    self.resolt.append(result)

    def stand_action(self, event):
        dealer_score = calculate_score(self.dealer_hand)
        player_score = calculate_score(self.player_hand)

        if player_score >= 21:
            result = arcade.Sprite("Assets/Sprites/lose.png")
            result.center_x = self.window.width // 2
            result.center_y = self.window.height // 2 + 300
            self.hard_ui.append(result)
            return

        while True:
            action = self.ai.choose_action(self.dealer_hand, self.player_hand)

            if action == 1:
                if len(deck) == 0:
                    break
                self.draw_dealer_card()
                dealer_score = calculate_score(self.dealer_hand)
                if dealer_score >= 21:
                    result = arcade.Sprite("Assets/Sprites/win.png")
                    result.center_x = self.window.width // 2
                    result.center_y = self.window.height // 2 + 300
                    self.hard_ui.append(result)
                    return
            else:
                break

            dealer_score = calculate_score(self.dealer_hand)
            player_score = calculate_score(self.player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            result_path = "Assets/Sprites/win.png"
        elif dealer_score > player_score:
            result_path = "Assets/Sprites/lose.png"
        else:
            result_path = "Assets/Sprites/tie.jpg"

        result = arcade.Sprite(result_path)
        result.center_x = self.window.width // 2
        result.center_y = self.window.height // 2 + 300
        self.hard_ui.append(result)

    def card_map(self, suit_number, rank_number):
        suit_name = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades"}
        suit = suit_name[suit_number]

        rank = str(rank_number)

        return f"Assets/Sprites/Cards/card-{suit}-{rank}.png"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_messagebox(None)

    def show_messagebox(self, event):
        self.ui_manager.add(self.messagebox)

    def menu_easy(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.hard_ui.draw(pixelated=12)
        self.player_sprites.draw()
        self.dealer_sprites.draw()
        self.ui_manager.draw()
        self.resolt.draw()


window = arcade.Window(1920, 1200, "BlackJack", center_window=True, enable_polling=True)
menu_view = MainMenu()
window.show_view(menu_view)
arcade.run()
