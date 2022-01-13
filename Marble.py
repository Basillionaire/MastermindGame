import turtle
from Point import Point
from mastermind_game import COLORS
from turtle import Screen, Turtle
from mastermind_game import make_secret_code, count_bulls_and_cows

MARBLE_RADIUS = 15
GUESS_RADIUS = 3

CHECK_BUTTON = 'checkbutton.gif'
FILE_ERROR = 'file_error.gif'
LEADERBOARD_Error = 'leaderboard_error.gif'
LOSE = 'Lose.gif'
QUIT = 'quit.gif'
QUIT_MESSAGE = 'quitmsg.gif'
WINNER = 'winner.gif'
X_BUTTON = 'xbutton.gif'

WINNER_FILE = 'leaderboard.txt'


class GameRunner:
    def __init__(self, position, color, size = MARBLE_RADIUS):
        self.pen = self.new_pen()
        self.player = ''
        self.color = color
        self.position = position
        self.pen.hideturtle()
        self.size = size
        self.pen.speed(0)  # set to fastest drawing
        self.round_starting_position = Point(-300,200)
        self.guess_input_starting_position = Point(-300,-300)
        self.play_area = []
        self.input_row = []
        self.image_items = []
        self.successful_guess_row = []
        self.active_row = 0
        self.score = 0
        self.secret_code = make_secret_code()

    def new_pen(self): 
        return turtle.Turtle()

    def make_screen(self):
        screen = turtle.Screen()
        screen.setup(900,800)

    def draw_square(self, x, y, width, length, color='black'):   
        turtle.pensize(5)
        turtle.penup()
        turtle.sety(y)
        turtle.setx(x)
        turtle.pendown()
        turtle.color(color)
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(length)
        turtle.right(90)
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(length)
        turtle.right(90)

    def draw_circle(self, color='white', size=MARBLE_RADIUS):
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)
        self.pen.down()
        self.pen.fillcolor(color)
        self.pen.begin_fill()
        self.pen.circle(size)
        self.pen.end_fill()

    def draw_empty_circle(self, size):
        self.draw_circle(size=size)

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def draw_empty_guess_cirlces(self):
        initial_x, initial_y = self.position.x, self.position.y
        self.position.y += 15

        guess_positions = []

        def draw_set_of_2_circles(guess_positions):
            for _ in range(2):
                guess_positions.append(CircleData(x=self.position.x, y=self.position.y, color='white'))
                self.draw_empty_circle(size=GUESS_RADIUS)
                self.position.y -= 10
            return guess_positions

        guess_positions = draw_set_of_2_circles(guess_positions)

        self.position.y += 20
        self.position.x += 10

        guess_positions = draw_set_of_2_circles(guess_positions)

        return guess_positions
        
    def draw_4_empty_circles(self):
        row_of_circles = []
        for _ in range(4):
            row_of_circles.append(CircleData(x=self.position.x, y=self.position.y, color='white'))
            self.draw_empty_circle(MARBLE_RADIUS)
            self.position.x += 60

        empty_cow_bulls = self.draw_empty_guess_cirlces()
        for circ in row_of_circles:
            print(circ.x, circ.y)
        return row_of_circles, empty_cow_bulls

    def draw_10_sets_of_4_circles(self):
        self.position = self.round_starting_position
        for _ in range(10):
            row_of_circles, empty_cow_bulls = self.draw_4_empty_circles()
            self.play_area.append(row_of_circles)
            self.successful_guess_row.append(empty_cow_bulls)
            self.position.x -= 250
            self.position.y -= 40

    def draw_input_circles(self):
        self.position = self.guess_input_starting_position
        for color in COLORS:
            self.input_row.append(CircleData(x=self.position.x, y=self.position.y, color=color))
            self.draw_circle(color=color, size=MARBLE_RADIUS)
            
            self.position.x += 40

    def show_winners(self):
        scores = self.read_scores()
        turtle.setpos(300, 0)
        #self.pen.goto(self.position.x, self.position.y)

        final_string = ''
        for player_and_score in scores:
            if player_and_score.strip() == '':
                continue
            player, score = player_and_score.strip().split(',')
            
            string = '{} : {}\n'.format(player, score)
            final_string += string
            self.pen.goto(self.position.x, self.position.y)
        turtle.write(final_string,  font=("Arial", 15, "normal"), align='Right')
        

    def declare_user(self):
        self.player = turtle.textinput("MasterMind", "Your name:")
        self.show_winners()

    def write_score(self):
        score_string = '{},{}\n'.format(self.player, self.score)
        lines = self.read_scores()
        output_lines = []
        with open(WINNER_FILE, 'w+') as file:
            does_player_exist = False
            for line in lines:
                if line.strip() == '':
                    continue
                recorded_player, recorded_score = line.split(',')
                if self.player == recorded_player and self.score > int(recorded_score):
                    output_lines.append(score_string)
                    does_player_exist = True
                else:
                    output_lines.append(line + "\n")
            if not does_player_exist:
                output_lines += score_string
            
            file.truncate(0)
            file.writelines(output_lines)
            

    def read_scores(self):
        try:
            with open(WINNER_FILE, 'r+') as file:
                lines = file.readlines()
        except Exception:
            with open(WINNER_FILE, 'w+') as file:
                lines = []

        return lines

    def handle_clicks_on_input_circles(self, x, y):
        for input_circle in self.input_row:
            if input_circle.is_click_in_range(x, y):
                if input_circle.color == 'white':
                    break
                active_row = self.play_area[self.active_row]
                for index in range(len(active_row)):
                    if active_row[index].color == 'white':
                        self.position.x = active_row[index].x
                        self.position.y = active_row[index].y
                        self.draw_circle(input_circle.color)
                        self.play_area[self.active_row][index].color = input_circle.color
                        self.position.x = input_circle.x
                        self.position.y = input_circle.y
                        input_circle.color = 'white'
                        self.draw_circle()
                        print(self.play_area[self.active_row][index].color)
                        break
                    else:
                        continue

        self.handle_clicks_on_buttons(x, y)

    def handle_clicks_on_buttons(self, x, y):
        for image in self.image_items:
            print(x,y)
            if image.is_in_click_range(x, y):
                if image.image == CHECK_BUTTON:
                    self.submit_checkbox()
                elif image.image == X_BUTTON:
                    self.reset_input_and_current_row()
                elif image.image == QUIT:
                    self.quit_action()

    def reset_input_and_current_row(self):
        self.reset_input_circles()
        self.reset_active_row()

    def reset_input_circles(self):
        for index in range(len(self.input_row)):
            if self.input_row[index].color == 'white':
                self.input_row[index].color = COLORS[index]
                self.set_position(self.input_row[index].x, self.input_row[index].y)
                self.draw_circle(COLORS[index])
                
    def reset_active_row(self):
        for item in self.play_area[self.active_row]:
            if item.color != 'white':
                item.color = 'white'
                self.set_position(item.x, item.y)
                self.draw_circle(item.color)
                    
    def submit_checkbox(self):
        guesses = [circle.color for circle in self.play_area[self.active_row]]
        
        bulls, cows = count_bulls_and_cows(self.secret_code, guesses)
        if bulls > 0 or cows > 0:
            tracker = 0
            for bull in range(bulls):
                active_guess_row = self.successful_guess_row[self.active_row]
                circle = active_guess_row[tracker]
                self.position.x = circle.x
                self.position.y = circle.y
                self.draw_circle('black', GUESS_RADIUS)
                tracker += 1
            for cow in range(cows):
                active_guess_row = self.successful_guess_row[self.active_row]
                circle = active_guess_row[tracker]
                self.position.x = circle.x
                self.position.y = circle.y
                self.draw_circle('red', GUESS_RADIUS)
                tracker += 1
        self.active_row += 1
        self.score = self.active_row
        self.reset_input_circles()
        if bulls == 4 or self.active_row > 9:
            self.end_game(bulls)

    def quit_action(self):
        self.score = 11
        self.write_score()
        turtle.bye()

    def stamp_image(self, image, width, height, x, y):
        screen = Screen()
        screen.register_shape(image)

        turtle = Turtle(shape=image)
        turtle.penup()

        turtle.goto(x, y)
        turtle.stamp()
        turtle.shape('classic')
        turtle.penup()
        

        x1 = x - width/2
        y1 = y + height/2

        x2 = x1 + width
        y2 = y1 - height

        image = ImageData(x1=x1, y1=y1, x2=x2, y2=y2, width=width, height=height, image=image)
        self.image_items.append(image)
        return turtle.stamp()
        

    def quit(self):
        return self.stamp_image(QUIT, 100, 56, 200, -350)

    def checkbox(self):
        return self.stamp_image(CHECK_BUTTON, 60, 60, -300, -350)

    def reset_button(self):
        return self.stamp_image(X_BUTTON, 60, 60,  -230, -350)

    def end_game(self, bulls):
        self.write_score()
        if bulls == 4:
            return self.stamp_image(WINNER, 1000,1000, 0, 0)
        else:
            return self.stamp_image(LOSER, 1000,1000, 0, 0)

    def render_images(self):
        self.quit()
        self.checkbox()
        self.reset_button()


class CircleData:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def is_click_in_range(self, x, y):
        x1 = self.x + MARBLE_RADIUS
        x2 = self.x - MARBLE_RADIUS
        y1 = self.y + MARBLE_RADIUS + MARBLE_RADIUS
        y2 = self.y - MARBLE_RADIUS + MARBLE_RADIUS
        is_in_x_range =  x > x2 and x < x1

        is_in_y_range = y > y2 and y < y1
        return is_in_x_range and is_in_y_range


class ImageData:
    def __init__(self, x1, y1, x2, y2, width, height, image):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height
        self.image = image

    def is_in_click_range(self, x, y):
        
        is_in_x_range =  x > self.x1 and x < self.x2

        is_in_y_range = y > self.y2 and y < self.y1
        return is_in_x_range and is_in_y_range
