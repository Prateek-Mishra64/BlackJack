import arcade
import arcade.gui


class MyGame(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.background_color = arcade.color.AMAZON
        self.background = arcade.load_texture("/home/himesh/Documents/Blackjack/Resources/Menu.jpg")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        normal = arcade.load_texture("Resources/play_normal.png")
        hover = arcade.load_texture("Resources/play_hover.png")
        press = arcade.load_texture("Resources/play_pressed.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, self.width ,self.height),
        )

def main():
    window = MyGame(1200,869,title="My Arcade Game")
    arcade.run()

if __name__ == "__main__":
    main()

