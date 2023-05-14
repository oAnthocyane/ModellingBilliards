import pygame


class Simulation:
    def __init__(self, coords, radius, coords_loose, radius_loose, color_loose=(0, 0, 0),
                 color_first_ball=(255, 0, 0), color_second_ball=(0, 255, 0)):
        self.coords = coords
        self.radius = radius
        self.colors = [color_first_ball, color_second_ball]
        self.coords_loose = coords_loose
        self.radius_loose = radius_loose
        self.color_loose = color_loose

    def show_with_pygame(self, width=640, height=480):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Balls")

        # отрисовываем каждый шаг по очереди
        for i in range(len(self.coords[0])):
            # очищаем экран
            screen.fill((0, 0, 0))
            pygame.draw.circle(screen, self.color_loose, self.coords_loose, self.radius_loose)
            # рисуем каждый шарик
            for j in range(len(self.coords)):
                pygame.draw.circle(screen, self.colors[j], (self.coords[j][i][0], self.coords[j][i][1]), self.radius)
            pygame.display.update()

            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


