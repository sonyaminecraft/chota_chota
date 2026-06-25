import random
import tkinter as tk

# Настройки экрана
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 15
INITIAL_FALL_SPEED = 4


class AdvancedSpaceGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Space Garbage Collector Pro")
        self.root.resizable(False, False)

        # Главный холст
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#050510")
        self.canvas.pack()

        # Игровые переменные
        self.score = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.game_over = False

        # Генерируем красивое звездное небо на заднем фоне
        self.stars = []
        self.create_stars()

        # Интерфейс счета
        self.score_text = self.canvas.create_text(
            70,
            30,
            text=f"SCORE: {self.score}",
            fill="#00ffff",
            font=("Courier New", 18, "bold"),
        )

        # Создаём игрока (Супермен)
        self.create_player()

        # Космический мусор — радиоактивная светящаяся сфера
        self.garbage = self.canvas.create_oval(
            0,
            0,
            35,
            35,
            fill="#ff0055",
            outline="#ffcc00",
            width=3,
            tags="garbage",
        )
        self.respawn_garbage()

        # Зажимаем клавиши для плавного управления во все стороны (WASD + Стрелки)
        self.keys = {
            "w": False,
            "s": False,
            "a": False,
            "d": False,
            "Up": False,
            "Down": False,
            "Left": False,
            "Right": False,
        }

        # Биндим нажатия и отпускания клавиш
        self.root.bind("<KeyPress>", self.press_key)
        self.root.bind("<KeyRelease>", self.release_key)

        # Переменные для хранения надписей Game Over
        self.game_over_texts = []

        # Погнали!
        self.update_game()

    def create_player(self):
        """Создает корабль в виде Супермена (человечек с плащом)."""
        # Тело Супермена
        self.player = self.canvas.create_polygon(
            # Голова (круглая)
            WIDTH // 2 - 10, HEIGHT - 75,
            WIDTH // 2 - 15, HEIGHT - 70,
            WIDTH // 2 - 15, HEIGHT - 55,
            WIDTH // 2 - 10, HEIGHT - 50,
            WIDTH // 2 - 5, HEIGHT - 48,
            WIDTH // 2, HEIGHT - 47,  # Макушка
            WIDTH // 2 + 5, HEIGHT - 48,
            WIDTH // 2 + 10, HEIGHT - 50,
            WIDTH // 2 + 15, HEIGHT - 55,
            WIDTH // 2 + 15, HEIGHT - 70,
            WIDTH // 2 + 10, HEIGHT - 75,
            fill="#ffcc00",  # Жёлтые волосы
            outline="#ff8800",
            width=1,
        )
        
        # Лицо (кожа)
        self.face = self.canvas.create_polygon(
            WIDTH // 2 - 7, HEIGHT - 72,
            WIDTH // 2 - 10, HEIGHT - 65,
            WIDTH // 2 - 10, HEIGHT - 58,
            WIDTH // 2 - 5, HEIGHT - 53,
            WIDTH // 2, HEIGHT - 51,
            WIDTH // 2 + 5, HEIGHT - 53,
            WIDTH // 2 + 10, HEIGHT - 58,
            WIDTH // 2 + 10, HEIGHT - 65,
            WIDTH // 2 + 7, HEIGHT - 72,
            fill="#f5cba7",
            outline="#e8b48c",
            width=1,
        )
        
        # Тело (синий костюм)
        self.body = self.canvas.create_polygon(
            WIDTH // 2 - 18, HEIGHT - 55,
            WIDTH // 2 - 20, HEIGHT - 40,
            WIDTH // 2 - 18, HEIGHT - 25,
            WIDTH // 2 - 12, HEIGHT - 15,
            WIDTH // 2, HEIGHT - 10,
            WIDTH // 2 + 12, HEIGHT - 15,
            WIDTH // 2 + 18, HEIGHT - 25,
            WIDTH // 2 + 20, HEIGHT - 40,
            WIDTH // 2 + 18, HEIGHT - 55,
            fill="#1a3d7c",
            outline="#0d2b5e",
            width=2,
        )
        
        # Логотип S на груди (красный ромб с S)
        self.logo = self.canvas.create_polygon(
            WIDTH // 2, HEIGHT - 48,
            WIDTH // 2 - 8, HEIGHT - 38,
            WIDTH // 2 - 6, HEIGHT - 28,
            WIDTH // 2, HEIGHT - 22,
            WIDTH // 2 + 6, HEIGHT - 28,
            WIDTH // 2 + 8, HEIGHT - 38,
            fill="#cc0000",
            outline="#ff0000",
            width=1,
        )
        
        # Буква S на логотипе (просто линия)
        self.s_logo = self.canvas.create_text(
            WIDTH // 2, HEIGHT - 36,
            text="S",
            fill="#ffffff",
            font=("Arial", 10, "bold")
        )
        
        # Руки (вытянуты вперёд, как при полёте)
        # Левая рука
        self.left_arm = self.canvas.create_polygon(
            WIDTH // 2 - 20, HEIGHT - 48,
            WIDTH // 2 - 35, HEIGHT - 55,
            WIDTH // 2 - 30, HEIGHT - 50,
            WIDTH // 2 - 18, HEIGHT - 40,
            fill="#f5cba7",
            outline="#e8b48c",
            width=1,
        )
        
        # Правая рука
        self.right_arm = self.canvas.create_polygon(
            WIDTH // 2 + 20, HEIGHT - 48,
            WIDTH // 2 + 35, HEIGHT - 55,
            WIDTH // 2 + 30, HEIGHT - 50,
            WIDTH // 2 + 18, HEIGHT - 40,
            fill="#f5cba7",
            outline="#e8b48c",
            width=1,
        )
        
        # Красный плащ (развевается назад)
        self.cape = self.canvas.create_polygon(
            WIDTH // 2 - 15, HEIGHT - 15,
            WIDTH // 2 - 30, HEIGHT - 5,
            WIDTH // 2 - 25, HEIGHT + 5,
            WIDTH // 2 - 10, HEIGHT - 5,
            WIDTH // 2, HEIGHT - 8,
            WIDTH // 2 + 10, HEIGHT - 5,
            WIDTH // 2 + 25, HEIGHT + 5,
            WIDTH // 2 + 30, HEIGHT - 5,
            WIDTH // 2 + 15, HEIGHT - 15,
            fill="#cc0000",
            outline="#ff0000",
            width=2,
        )
        
        # Ноги (ботинки)
        # Левая нога
        self.left_leg = self.canvas.create_polygon(
            WIDTH // 2 - 12, HEIGHT - 10,
            WIDTH // 2 - 15, HEIGHT,
            WIDTH // 2 - 8, HEIGHT + 2,
            WIDTH // 2 - 5, HEIGHT - 5,
            fill="#1a3d7c",
            outline="#0d2b5e",
            width=1,
        )
        
        # Правая нога
        self.right_leg = self.canvas.create_polygon(
            WIDTH // 2 + 12, HEIGHT - 10,
            WIDTH // 2 + 15, HEIGHT,
            WIDTH // 2 + 8, HEIGHT + 2,
            WIDTH // 2 + 5, HEIGHT - 5,
            fill="#1a3d7c",
            outline="#0d2b5e",
            width=1,
        )
        
        # Группируем все части в один список для удобства перемещения
        self.player_parts = [
            self.player, self.face, self.body, self.logo, self.s_logo,
            self.left_arm, self.right_arm, self.cape, self.left_leg, self.right_leg
        ]

    def create_stars(self):
        """Создает 60 звезд случайного размера и яркости."""
        for _ in range(60):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.choice([1, 2, 3])
            color = random.choice(["#ffffff", "#aaaaaa", "#5555ff", "#ffaa00"])
            star = self.canvas.create_oval(
                x, y, x + size, y + size, fill=color, outline=""
            )
            self.stars.append((star, random.choice([1, 1.5, 2])))

    def respawn_garbage(self):
        """Выкидывает новый мусор сверху."""
        x = random.randint(30, WIDTH - 60)
        self.canvas.moveto(self.garbage, x, -50)

    def press_key(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = True

    def release_key(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = False

    def process_movement(self):
        """Расчет движения корабля по 4 направлениям одновременно."""
        if self.game_over:
            return

        dx, dy = 0, 0
        if self.keys["w"] or self.keys["Up"]:
            dy = -PLAYER_SPEED
        if self.keys["s"] or self.keys["Down"]:
            dy = PLAYER_SPEED
        if self.keys["a"] or self.keys["Left"]:
            dx = -PLAYER_SPEED
        if self.keys["d"] or self.keys["Right"]:
            dx = PLAYER_SPEED

        # Проверяем границы для всех частей Супермена
        p_box = self.canvas.bbox(self.player)
        if p_box:
            if (dx < 0 and p_box[0] <= 10) or (dx > 0 and p_box[2] >= WIDTH - 10):
                dx = 0
            if (dy < 0 and p_box[1] <= 10) or (dy > 0 and p_box[3] >= HEIGHT - 10):
                dy = 0

            # Двигаем все части Супермена
            for part in self.player_parts:
                self.canvas.move(part, dx, dy)

    def animate_stars(self):
        """Движение звезд вниз, создающее иллюзию полета вперед."""
        for star, speed in self.stars:
            self.canvas.move(star, 0, speed)
            s_box = self.canvas.bbox(star)
            if s_box and s_box[1] > HEIGHT:
                self.canvas.moveto(star, random.randint(0, WIDTH), -5)

    def check_collision(self):
        """Проверка, поймал ли корабль летящий кусок мусора."""
        p_box = self.canvas.bbox(self.player)
        g_box = self.canvas.bbox(self.garbage)

        if p_box and g_box:
            if not (
                p_box[2] < g_box[0]
                or p_box[0] > g_box[2]
                or p_box[3] < g_box[1]
                or p_box[1] > g_box[3]
            ):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score}")
                self.fall_speed += 0.3
                self.respawn_garbage()

    def restart_game(self):
        """Перезапускает игру."""
        # Удаляем старые надписи Game Over
        for text in self.game_over_texts:
            self.canvas.delete(text)
        self.game_over_texts = []
        
        # Сбрасываем переменные
        self.game_over = False
        self.score = 0
        self.fall_speed = INITIAL_FALL_SPEED
        
        # Обновляем счёт
        self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score}")
        
        # Возвращаем Супермена на стартовую позицию
        for part in self.player_parts:
            self.canvas.move(part, -(self.canvas.coords(part)[0] - WIDTH//2), 
                             -(self.canvas.coords(part)[1] - (HEIGHT - 60)))
        
        # Создаём новый мусор
        self.respawn_garbage()
        
        # Убираем кнопку рестарта, если она есть
        if hasattr(self, 'restart_button'):
            self.canvas.delete(self.restart_button)

    def show_game_over(self):
        """Показывает экран Game Over с кнопкой рестарта."""
        # Текст Game Over
        game_over_text = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 30,
            text="GAME OVER",
            fill="#ff0055",
            font=("Courier New", 50, "bold"),
        )
        self.game_over_texts.append(game_over_text)
        
        subtitle = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 30,
            text="You let the space debris escape!",
            fill="#ffffff",
            font=("Courier New", 16),
        )
        self.game_over_texts.append(subtitle)
        
        # Счёт на экране Game Over
        score_text = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 70,
            text=f"Final Score: {self.score}",
            fill="#00ffff",
            font=("Courier New", 20, "bold"),
        )
        self.game_over_texts.append(score_text)
        
        # Кнопка "Play Again" (красивая неоновая)
        self.restart_button = self.canvas.create_rectangle(
            WIDTH // 2 - 80,
            HEIGHT // 2 + 100,
            WIDTH // 2 + 80,
            HEIGHT // 2 + 140,
            fill="#00ffcc",
            outline="#ffffff",
            width=3,
            tags="restart_btn"
        )
        
        self.restart_text = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 120,
            text="↻ PLAY AGAIN",
            fill="#050510",
            font=("Courier New", 16, "bold"),
            tags="restart_btn"
        )
        
        self.game_over_texts.append(self.restart_button)
        self.game_over_texts.append(self.restart_text)
        
        # Привязываем клик по кнопке
        self.canvas.tag_bind("restart_btn", "<Button-1>", lambda e: self.restart_game())

    def update_game(self):
        """Основной такт игры (50 кадров в секунду)."""
        if not self.game_over:
            self.process_movement()
            self.animate_stars()
            
            self.canvas.move(self.garbage, 0, self.fall_speed)
            self.check_collision()
            
            g_box = self.canvas.bbox(self.garbage)
            if g_box and g_box[1] > HEIGHT:
                self.game_over = True
                self.show_game_over()
            
            self.root.after(20, self.update_game)
        else:
            # Продолжаем обновлять звёзды даже в Game Over
            self.animate_stars()
            self.root.after(20, self.update_game)


if __name__ == "__main__":
    window = tk.Tk()
    game = AdvancedSpaceGame(window)
    window.mainloop()