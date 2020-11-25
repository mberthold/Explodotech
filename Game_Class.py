import threading
import pygame
import pygame_gui
import numpy as np
import json

# Importing my own stuff
import Vessel_Class as vc
import Projectile_Class as pc
import Ship_Class as sc


class Game ():
    """This class should handle the GUI and all the real-time aspects!"""

    engine_running = False
    gui_running = True
    clock = pygame.time.Clock()

    gui_framerate = 60.0
    engine_framerate = 120.0

    window_height = 800
    window_width = 1200

    radar_scope_position = (400, 150)
    radar_scope_zoom =2

    objects = {}
    next_id = 0

    background = None

    gui_layers = []

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Explodotech')
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier', 20)
        self.window_surface = pygame.display.set_mode((self.window_width,self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        self.initiate_radar_screen()
        

        try:
            self.background = pygame.image.load("Ressources/menu_bg.jpg")
            print("Setting Background image")
        except OSError as e:
            print (str(e))
            self.background = pygame.Surface((self.window_width,self.window_height))
            self.background.fill(pygame.Color('#000000'))
            print("Setting Background black")
        self.gui_layers.append((self.background, (0,0)))

        #self.manager = pygame_gui.UIManager((self.window_width, self.window_height))

        ### Define GUI Elements here
        self.lbl_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.window_width/2 - 100, 20), (200,50)), text = "Explodotech", manager = self.manager)

        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.window_width-150, self.window_height-100),
                            (100, 50)), text='Quit', manager=self.manager,
                            tool_tip_text = "Quit the game")

        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,50),(100,50)),
                                                        text='Start', manager = self.manager)

        # Scenatio selection
        self.drp_scenario_select = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect = pygame.Rect((50,300),(300,50)), manager = self.manager, 
                                                                                    options_list = self.load_scenarios(), starting_option = "Choose scenario")

        # We will keep this one around for now but actually we want to select a scenario and spawn the vessels from there
        self.btn_run_test = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,700),(100,50)),
                                                        text='Run Test', manager = self.manager)

        ### Create the engine thread
        self.engine_thread = threading.Thread(target = self.engine_loop, args = [], daemon=True)

        #self.engine_thread.start()

    def initiate_radar_screen(self):
        """Initiate all the elements found on the radar screen"""
        scope_size = (600, 600)
        self.radar_manager = pygame_gui.UIManager(scope_size)
        self.radar_scope = pygame.Surface(scope_size)   # This is the surface we want to be drawing all of the tokens on
        self.btn_accelerate = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((scope_size[0]-150, 200),(50,50)), text="Burn",
                                                            manager = self.radar_manager)


    def start_polling(self):
        """Starts the main loop"""
        self.engine_running = True

    def stop_polling(self):
        """Stops the main loop"""
        self.engine_running = False

    def load_scenarios(self):
        """ Load different scenario options from a (json?) file"""
        scenario_select_options = []
        with open("utility/scenarios.json") as json_file:
            self.scenario_list = json.load(json_file)["scenarios"]
        for scen in self.scenario_list:
            scenario_select_options.append(scen["name"])
        return scenario_select_options
        

    def gui_loop(self):
        """Managing all the GUI stuff"""

        print ("GUI-loop started!")

        while self.gui_running:
            
            dT = self.clock.tick(60)/1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.gui_running = False

                if event.type == pygame.USEREVENT:
                    # Checking for button presses!
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.quit_button:
                            self.quit_button_event()
                        if event.ui_element == self.start_button:
                            self.start_button_event()
                        if event.ui_element == self.btn_run_test:
                            self.btn_run_test_event()
                    # Checking for dropdown changes!
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.drp_scenario_select:
                            for scen in self.scenario_list:
                                if scen["name"] == event.text:
                                    for obj in scen["objects"]:
                                        if "ship" in obj["type"]:
                                            self.objects[self.next_id] = sc.Ship(ident = self.next_id, pos = np.array(obj["pos"]), name =  obj["name"])
                                            self.objects[self.next_id].velocity = np.array(obj["velocity"])
                                            self.next_id += 1
                                        if "missile" in obj["type"]:
                                            origin = self.objects[obj["origin_id"]]
                                            target = self.objects[obj["target_id"]]
                                            
                                            self.objects[self.next_id] = pc.Projectile(ident = self.next_id, target = target, origin = origin, totalSpeed = obj["totalSpeed"])
                                            self.next_id += 1

                self.manager.process_events(event)

            self.manager.update(dT)
            
            self.window_surface.blits(self.gui_layers)

            self.manager.draw_ui(self.window_surface)
            
            if self.engine_running:
                self.draw_radar_scope(dT)

            pygame.display.update()

    def draw_radar_scope(self, dT):

        # Blank the Radar Scope

        self.radar_scope.fill(pygame.Color('#1E323C'))


        # Draw all the elements onto the screen

        for ID in self.objects:
            obj = self.objects.get(ID)
            # Drawing ships
            if "ship" in obj.vessel_type:
                color = "white"

                center = (obj.pos)/self.radar_scope_zoom
                line_end = (center + 2*obj.velocity)
                text_pos = ((center[0]+15), (center[1]-10))

                pygame.draw.circle(surface = self.radar_scope, color = color, center = center, radius = 10, width = 2)
                pygame.draw.line(surface = self.radar_scope, color = color, start_pos = center, end_pos = line_end, width = 2)
                textsurface = self.myfont.render(self.objects[ID].name, False, (100, 100, 100))
                self.radar_scope.blit(textsurface, text_pos)
            elif obj.vessel_type == "missile":
                color = "red"
                rel = (obj.pos-[5,5])/self.radar_scope_zoom
                center = center = (obj.pos)/self.radar_scope_zoom
                line_end = (center + 2*obj.velocity)
                size = (10/self.radar_scope_zoom, 10/self.radar_scope_zoom)
                pygame.draw.rect(surface = self.radar_scope, color = color, rect = pygame.Rect((rel,size), width = 2))
                pygame.draw.line(surface = self.radar_scope, color = color, start_pos = center, end_pos = line_end, width = 2)

        self.radar_manager.update(dT)
        self.radar_manager.draw_ui(self.radar_scope)

    def engine_loop(self):
        """Doing all the game calculations in the background"""
        print("Engine loop started...")
        while self.engine_running:
            t = self.clock.tick_busy_loop(60)/1000
            graveyard = []
            for ID in self.objects:
                obj = self.objects.get(ID)
                obj.update(t)
                if not obj.isAlive:
                    graveyard.append(ID)
            for ID in graveyard:
                self.objects.pop(ID)

    ### Define GUI events here

    def quit_button_event(self):
        """Shut down the GUI"""
        print("Quit-button pressed!")
        self.gui_running = False
        self.engine_running = False

    def start_button_event(self):
        """Start the game"""
        if self.engine_running == False:
            print("Engine Starting")
            self.engine_running = True
            self.engine_thread.start()
            self.gui_layers.append((self.radar_scope, self.radar_scope_position))
        else:
            print("Engine Stopping")
            self.engine_running = False
            i = self.gui_layers.index((self.radar_scope, self.radar_scope_position))
            self.gui_layers.pop(i)
            # deleting all objetcs so we can start from a clean sheet
            self.objects = []
            self.next_id = 0
            #self.engine_thread.stop()

    def btn_run_test_event(self):
        """Spawn two vessels to see if things work"""
        print("Run Test pressed!")

        