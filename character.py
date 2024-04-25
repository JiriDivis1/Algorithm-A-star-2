from model import *


# Postava ve hře, v tomto případě červený kruh
class Character():
    def __init__(self, image, x_center, y_center):
        self.image = image
        self.x_center = x_center
        self.y_center = y_center
        self.rect = self.image.get_rect(center=(self.x_center, self.y_center))
        self.mask = pygame.mask.from_surface(self.image)
        self.dest_positions = []  # Pole pozicí (x, y), na které se má postava přesunout
        self.direct_x = 1
        self.direct_y = 1
        self.movement = False  # True, pokud se postava pohybuje

    def get_image(self):
        return self.image

    def get_x_center(self):
        return self.x_center

    def set_x_center(self, x_center):
        self.x_center = x_center
        return self

    def get_y_center(self):
        return self.y_center

    def set_y_center(self, y_center):
        self.y_center = y_center
        return self

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect
        return self

    def get_positions(self):
        return (self.get_rect().centerx, self.get_rect().centery)

    def get_mask(self):
        return self.mask

    def get_dest_positions(self):
        return self.dest_positions

    def set_dest_positions(self, dest_positions):
        self.dest_positions = dest_positions
        return self

    def get_direct_x(self):
        return self.direct_x

    def set_direct_x(self, direct_x):
        self.direct_x = direct_x
        return self

    def get_direct_y(self):
        return self.direct_y

    def set_direct_y(self, direct_y):
        self.direct_y = direct_y
        return self

    def get_movement(self):
        return self.movement

    def set_movement(self, movement):
        self.movement = movement
        return self

    # Vykleslí postavu na obrazovku
    def draw(self):
        SCREEN.blit(self.get_image(), self.get_rect())

    # Vrátí true, pokud bylo na kliknuto na postavu
    def is_clicked(self, position):
        pos_in_mask = position[0] - self.get_rect().x, position[1] - self.get_rect().y
        touching = self.get_rect().collidepoint(*position) and self.get_mask().get_at(pos_in_mask)
        return touching

    """ Funkce pro vykonávání pohybu postavy
    """
    def move(self):
        # Je aktivován pohyb
        if self.get_movement():
            dest_positions = self.get_dest_positions()
            act_dest_position = dest_positions[0]
            # Funkce move_x a move_y vrátí True, jakmile je pohyb dokončen
            movement_x = self.move_x(act_dest_position[0])
            movement_y = self.move_y(act_dest_position[1])

            if movement_x and movement_y:
                dest_positions.pop(0)
                if dest_positions == []:
                    self.set_movement(False)
                    return None

                first_dest = dest_positions[0]
                source_position = self.get_positions()

                if source_position[0] <= first_dest[0]:
                    self.set_direct_x(SPEED_OF_PEOPLES)
                else:
                    self.set_direct_x(-1 * SPEED_OF_PEOPLES)

                if source_position[1] <= first_dest[1]:
                    self.set_direct_y(SPEED_OF_PEOPLES)
                else:
                    self.set_direct_y(-1 * SPEED_OF_PEOPLES)

            if dest_positions == []:
                self.set_movement(False)

    """
    Provádí pohyb ke čtverci, který je v dest_positions na nultém indexu
    pokud jsme se do toho čtverce dostali, vrátí 1, jinak vrátí nulu
    """

    def move_x(self, final_position):
        source_position = self.get_rect().centerx
        direct_x = self.get_direct_x()
        # Půjdeme doprava
        if direct_x > 0:
            if source_position < final_position:
                self.get_rect().centerx += direct_x
                return 0
            # Jsme v cíli
            else:
                self.get_rect().centerx = final_position
                return 1
        # Půjdeme doleva
        else:
            if source_position > final_position:
                self.get_rect().centerx += direct_x
                return 0
            else:
                self.get_rect().centerx = final_position
                return 1

    """
    Provádí pohyb ke čtverci, který je v dest_positions na nultém indexu
    pokud jsme se do toho čtverce dostali, vrátí 1, jinak vrátí nula
    """
    def move_y(self, final_position):
        source_position = self.get_rect().centery
        direct_y = self.get_direct_y()
        # Půjdeme doprava
        if direct_y > 0:
            if source_position < final_position:
                self.get_rect().centery += direct_y
                return 0
            # Jsme v cíli
            else:
                self.get_rect().centery = final_position
                return 1
        # Půjdeme doleva
        else:
            if source_position > final_position:
                self.get_rect().centery += direct_y
                return 0
            else:
                self.get_rect().centery = final_position
                return 1