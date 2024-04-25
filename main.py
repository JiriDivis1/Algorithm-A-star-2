from graph import *
from character import *

#Inicializace pygame
pygame.init()

graph = Graph(NOT_USABLE_NODES)

start_node_indexes = graph.get_node_indexes("ab")
start_node_position = graph.get_nodes()[start_node_indexes[0]][start_node_indexes[1]].get_node_center_pos()
start_node_position = graph.convert_node_point_to_area_point(start_node_position[0], start_node_position[1])
character = Character(RED_CIRCLE, start_node_position[0], start_node_position[1])

def main():
    global running, graph

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 = levé tlačítko na myši
                click_position = pygame.mouse.get_pos()
                if character.is_clicked(click_position):
                    print("klikl jsi na hráče")
                    continue
                click_position = graph.convert_area_point_to_node_point(click_position[0], click_position[1])
                # Zjistíme id uzlu, na který jsme klikli
                click_node = None
                for i in range(count_of_rows):
                    for j in range(count_of_cols):
                        click_node = graph.get_nodes()[i][j]
                        if click_node.is_clicked(click_position):
                            dest_node = graph.get_nodes()[i][j]
                            dest_node_id = dest_node.get_node_id()

                            # Klikli jsme na nepoužitelný uzel
                            if not dest_node.get_is_usable():
                                print("Sem nelze jít, jedná se o překážku")
                            else:
                                # Zjistíme na kterém čtverci se nacházíme
                                source_position = character.get_positions()
                                source_node = None
                                dest_positions = []

                                for i in range(count_of_rows):
                                    for j in range(count_of_cols):
                                        source_node = graph.get_nodes()[i][j]

                                        if source_node.is_clicked(graph.convert_area_point_to_node_point(source_position[0], source_position[1])):
                                            source_node_id = source_node.get_node_id()

                                            if source_node_id == dest_node_id:
                                                click_position = graph.convert_node_point_to_area_point(click_position[0], click_position[1])
                                                if source_position[0] <= click_position[0]:
                                                    character.set_direct_x(SPEED_OF_PEOPLES)
                                                else:
                                                    character.set_direct_x(-1 * SPEED_OF_PEOPLES)

                                                if source_position[1] <= click_position[1]:
                                                    character.set_direct_y(SPEED_OF_PEOPLES)
                                                else:
                                                    character.set_direct_y(-1 * SPEED_OF_PEOPLES)

                                                dest_positions.append(click_position)
                                                character.set_dest_positions(dest_positions)
                                                character.set_movement(True)
                                                break

                                            dest_nodes = graph.a_star_algorithm(source_node_id, dest_node_id)
                                            #dest_nodes.pop(0)  # Jelikož na prvním místě je pozice aktuálního uzlu
                                            dest_nodes.pop(
                                                len(dest_nodes) - 1)  # Pozice posledního uzlu vyměníme za místo kliknutí

                                            #Odstranění chybných uzlů
                                            dest_nodes = graph.dest_nodes_filter(dest_nodes)

                                            for dest_node in dest_nodes:
                                                node_indexes = graph.get_node_indexes(dest_node)
                                                node = graph.get_nodes()[node_indexes[0]][node_indexes[1]]
                                                node_point = graph.convert_node_point_to_area_point(node.get_node_center_pos()[0], node.get_node_center_pos()[1])
                                                dest_positions.append(node_point)

                                            dest_positions.append(graph.convert_node_point_to_area_point(click_position[0], click_position[1]))

                                            character.set_dest_positions(dest_positions)
                                            character.set_movement(True)

                                            first_dest = dest_positions[0]

                                            # Určíme, zda se hráč má posouvat nahoru, ...
                                            if source_position[0] <= first_dest[0]:
                                                character.set_direct_x(SPEED_OF_PEOPLES)
                                            # ... nebo dolů
                                            else:
                                                character.set_direct_x(-1 * SPEED_OF_PEOPLES)

                                            # Určíme, zda se hráč má posouvat doprava, ...
                                            if source_position[1] <= first_dest[1]:
                                                character.set_direct_y(SPEED_OF_PEOPLES)
                                            # ... nebo doleva
                                            else:
                                                character.set_direct_y(-1 * SPEED_OF_PEOPLES)

                                            break
                                            
                                    # Pohyb byl započat
                                    if source_node and source_node.is_clicked(source_position):
                                        break

                    # Pohyb byl dokončen
                    if click_node and click_node.is_clicked(click_position):
                        break

        SCREEN.fill(YELLOW)

        #Vykreslení podlahy
        SCREEN.blit(FLOOR, FLOOR.get_rect())

        """
        pygame.draw.rect(SCREEN, BLACK, [FLOOR_MEDIAN-100, TOP_FLOOR, 200, 200], 3)
        pygame.draw.rect(SCREEN, BLACK, rectangle, 3)
        pygame.draw.polygon(SCREEN, BLACK,[(fun(rectangle.topleft[0], rectangle.topleft[1])), (fun(rectangle.topright[0], rectangle.topright[1])), (fun(rectangle.bottomright[0], rectangle.bottomright[1])), (fun(rectangle.bottomleft[0], rectangle.bottomleft[1]))], 3)
        """
        #Vykreslení čtverců ...
        for i in range(count_of_rows):
            for j in range(count_of_cols):
                act_node = graph.get_nodes()[i][j]

                if act_node.get_is_usable():
                    act_node.draw_area(TRANSPARENT)
                else:
                    act_node.draw_area(GRAY)
        
        # ... a hráče
        character.draw()
        character.move()


        pygame.display.update()

    pygame.quit()

main()