import threading
import pygame
import pygame_gui
import numpy as np

# Importing my own stuff
import Vessel_Class as vc
import Projectile_Class as pc


class Game ():
    """This class should handle the GUI and all the real-time aspects!"""

    engine_running = False
    gui_running = True
    clock = pygame.time.Clock()

    gui_framerate = 60.0
    engine_framerate = 120.0

    window_height = 1200
    window_width = 800

    objects = {}
    next_id = 0

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Explodotech')
        self.window_surface = pygame.display.set_mode((self.window_height, self.window_width))
        self.background = pygame.Surface((self.window_height, self.window_width))
        self.background.fill(pygame.Color('#000000'))

        self.manager = pygame_gui.UIManager((self.window_height, self.window_width))

        ### Define GUI Elements here
        self.lbl_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.window_width/2, 20), (200,50)), text = "Explodotech", manager = self.manager)

        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.window_height-150, self.window_width-100),
                            (100, 50)), text='Quit', manager=self.manager,
                            tool_tip_text = "Quit the game")

        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,50),(100,50)),
                                                        text='Start', manager = self.manager)

        self.btn_run_test = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,150),(100,50)),
                                                        text='Run Test', manager = self.manager)

        ### Create the engine thread
        self.engine_thread = threading.Thread(target = self.engine_loop, args = [], daemon=True)

        #self.engine_thread.start()


    def start_polling(self):
        """Starts the main loop"""
        self.engine_running = True

    def stop_polling(self):
        """Stops the main loop"""
        self.engine_running = False

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

                self.manager.process_events(event)

            self.manager.update(dT)

            self.window_surface.blit(self.background, (0, 0))

            # Draw all the elements onto the screen
            for ID in self.objects:
                #print("Drawing object")
                obj = self.objects.get(ID)
                pygame.draw.circle(surface = self.window_surface, color = "white", center = obj.pos, radius = 10, width = 2)

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

    def engine_loop(self):
        """Doing all the game calculations in the background"""
        print("Engine loop started...")
        while self.engine_running:
            t = self.clock.tick_busy_loop(60)/1000
            for ID in self.objects:
                obj = self.objects.get(ID)
                obj.update(t)

    ### Define GUI events here

    def quit_button_event(self):
        """Shut down the GUI"""
        print("Quit-button pressed!")
        self.gui_running = False
        self.engine_running = False

    def start_button_event(self):
        """Start the game"""
        print("Start-button pressed!")
        self.engine_running = True
        self.engine_thread.start()

    def btn_run_test_event(self):
        """Spawn two vessels to see if thinsg work"""
        print("Run Test pressed!")
        self.objects[self.next_id] = vc.Vessel(ident = self.next_id, pos = np.array([500.0,500.0]), name =  "Rocinante")
        self.objects[self.next_id].velocity = np.array([0.0,0.0])
        self.next_id += 1
        self.objects[self.next_id] = vc.Vessel(ident = self.next_id, pos = np.array([200.0,300.0]), name =  "Hamurabi")
        self.next_id += 1
        self.objects[self.next_id] = pc.Projectile(ident = self.next_id, target = self.objects[0], origin = self.objects[1], totalSpeed = 20.0)