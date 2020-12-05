import pygame
import pygame_gui

### A set of methods to handle the radar screen - just to keep the Game class a little tidier!

class Radar_Screen:
    scope_size = (600, 600)
    position = (0, 0)
    zoom_factor = 1.0

    controls_position = (400, 150) # The position of the controls relative to the entire radar scope
    controls_size = (200, 200)

    def __init__(self, position, manager, font):
        self.position = position
        self.update_controls_position()

        self.radar_scope = pygame.Surface(self.scope_size)   # This is the surface we want to be drawing all of the tokens on
        self.myfont = font
        
        # Defining the GUI container - the manager needs to be passed from outside!
        self.manager = manager
        self.controls_panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect(self.controls_position, self.controls_size), starting_layer_height = 99,
                                                                manager=self.manager, element_id="radar_screen", visible=False)
        # Defining the control buttons
        self.btn_accelerate = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((70, 20),(50,50)), text="Burn",
                                                            manager = self.manager, container=self.controls_panel)
        self.btn_rotate_left = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((40, 80),(50,50)), text="Left",
                                                            manager = self.manager, container=self.controls_panel)
        self.btn_rotate_right = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((100, 80),(50,50)), text="Right",
                                                            manager = self.manager, container=self.controls_panel)

    def get_surface (self):
        return self.radar_scope

    def show_controls(self):
        self.controls_panel.show()

    def update_controls_position(self):
        x = self.position[0] + self.controls_position[0]
        y = self.position[1] + self.controls_position[1]

        self.controls_position = (x, y)


    def draw(self, dT, objects):
        """Pass in a list of objects you want to draw and draw them!"""
        # Blank the Radar Scope

        self.radar_scope.fill(pygame.Color('#1E323C'))

        # Draw all the elements onto the screen

        for ID in objects:
            obj = objects.get(ID)
            # Drawing ships
            if "ship" in obj.vessel_type:
                color = "white"

                center = (obj.pos)/self.zoom_factor
                line_end = (center + 2*obj.velocity)
                text_pos = ((center[0]+15), (center[1]-10))

                pygame.draw.circle(surface = self.radar_scope, color = color, center = center, radius = 10, width = 2)
                pygame.draw.line(surface = self.radar_scope, color = color, start_pos = center, end_pos = line_end, width = 2)
                textsurface = self.myfont.render(objects[ID].name, False, (100, 100, 100))
                self.radar_scope.blit(textsurface, text_pos)
            elif obj.vessel_type == "missile":
                color = "red"
                rel = (obj.pos-[5,5])/self.zoom_factor
                center = center = (obj.pos)/self.zoom_factor
                line_end = (center + 2*obj.velocity)
                size = (10/self.zoom_factor, 10/self.zoom_factor)
                pygame.draw.rect(surface = self.radar_scope, color = color, rect = pygame.Rect((rel,size), width = 2))
                pygame.draw.line(surface = self.radar_scope, color = color, start_pos = center, end_pos = line_end, width = 2)
