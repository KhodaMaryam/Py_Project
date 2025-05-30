import os
import pygame
import numpy as np
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import time
import random
#import platform
#print(platform.python_version())
#################################################################################
class EGO_Car:
    def __init__(self, x, y, angle=90.0, length=4, max_steering=30, max_acceleration=5):
        self.position = Vector2(x, y)
        self.velocity = Vector2(8.31,0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 13.85 ###27.78 m/s =100 km/h minimum speed is 8.31 m/s =30 km/h,    13.85 m/s =50 km/h
        self.brake_deceleration = 5
        self.free_deceleration = 1
        self.acceleration = 0.0
        self.steering = 0.0
    def update(self,dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))#vehical velocity if it's in allowable range
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
################################################################################
class O_Car:
    def __init__(self,vel, x, y):
        self.position = Vector2(x, y)
        self.velocity=(0,vel)
    def update(self,dt):
        self.position += np.array(self.velocity) * dt
################################################################################


class Start:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((145, 700), pygame.RESIZABLE)
        width ,height = 145 ,700
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
# Loading image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "car.png")
        path_amu = os.path.join(current_dir, "amu.png")
        path1 = os.path.join(current_dir, "car1.png")
        path2 = os.path.join(current_dir, "car2.png")
        path3 = os.path.join(current_dir, "car3.png")
        path4 = os.path.join(current_dir, "car4.png")
        path5 = os.path.join(current_dir, "car5.png")

##### car_image
        Ecar_image = pygame.image.load(path)
        amu_image = pygame.image.load(path_amu)
        car_image1 = pygame.image.load(path1)
        car_image2 = pygame.image.load(path2)
        car_image3 = pygame.image.load(path3)
        car_image4 = pygame.image.load(path4)
        car_image5 = pygame.image.load(path5)
# Cars Location    ################ 1 km/h = .277 m/s
        RANDOM =6 + 2* random.random()
        Ecar = EGO_Car(RANDOM,64,angle=90.0)
        amu = O_Car(8.31,7,70)
        car3 = O_Car(8.31,7,57)
        car1=O_Car(8.31,3,89)### Top-Left car
        car2=O_Car(8.31,11.5,20)### Top-Right car
        car4=O_Car(8.31,3,57)### Top-Left car
        car5=O_Car(8.31,11.5,57)### bottom-Right car
        ppu = 10
        start_time = time.time()
        while not self.exit:
            dt = self.clock.get_time() / 1000
            
            # Event queue
            for event in pygame.event.get():
                pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                    self.exit = True

            # User input for ambulance
####################################################################

             # User input for host car
####################################################################         

            if pressed[pygame.K_UP]:
                if Ecar.velocity.x < 0:
                    Ecar.acceleration = Ecar.brake_deceleration
                else:
                    Ecar.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if Ecar.velocity.x > 0:
                    Ecar.acceleration = -1*Ecar.brake_deceleration
                else:
                    Ecar.acceleration -= 1 * dt
            else:
                if abs(Ecar.velocity.x) > dt * Ecar.free_deceleration:
                    Ecar.acceleration = -copysign(Ecar.free_deceleration, Ecar.velocity.x)
                else:
                    if dt != 0:
                        Ecar.acceleration = -Ecar.velocity.x / dt
            Ecar.acceleration = max(-Ecar.max_acceleration, min(Ecar.acceleration, Ecar.max_acceleration))
            if pressed[pygame.K_RIGHT]:
                Ecar.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                Ecar.steering += 30 * dt
            else:
                Ecar.steering = 0
            Ecar.steering = max(-Ecar.max_steering, min(Ecar.steering, Ecar.max_steering))
################################################################################################
           # Logic
            Ecar.update(dt)
            amu.update(-dt)
            car1.update(-dt)
            car2.update(-dt)
            car3.update(-dt)
            car4.update(-dt)
            car5.update(-dt)
            
            Ecar.position_disp = np.array((Ecar.position[0], Ecar.position[1]))
            amu.position_disp = np.array((amu.position[0], amu.position[1]))
            car1.position_disp = np.array((car1.position[0], car1.position[1]))
            car2.position_disp = np.array((car2.position[0], car2.position[1]))
            car3.position_disp = np.array((car3.position[0], car3.position[1]))
            car4.position_disp = np.array((car4.position[0], car4.position[1]))
            car5.position_disp = np.array((car5.position[0], car5.position[1]))
            #print(Ecar.position_disp[1])
            #print(Ecar.velocity.x)
########################################## Data writing ###########################################
#P_amu-P_ego,P_amu-P_car1,P_amu-P_car2,P_amu-P_car3,P_amu-P_ego,P_amu-P_car1,P_amu-P_car2,P_amu-P_car3,V_amu-V_ego,V_amu-V_car1,V_amu,V_car2,V_amu-V_car3,Ego_acc	    
            if amu.position_disp[1]> 1:
            	outFile = open('/home/m/daily podcast/Paper/Code/Simulator/Right','a')
            	outFile.write(str(amu.position_disp[1]- Ecar.position_disp[1]))#long dist ego
            	outFile.write(",") 
            	#outFile.write(str(amu.position_disp[1]-car1.position_disp[1]))#long dist amu & car1
            	#outFile.write(",") 
            	#outFile.write(str(amu.position_disp[1]-car2.position_disp[1]))#long dist amu & car2
            	#outFile.write(",")
            	#outFile.write(str(amu.position_disp[1]-car3.position_disp[1]))#long dist amu & car3
            	#outFile.write(",")
            	outFile.write(str(amu.position_disp[0]- Ecar.position_disp[0]))#lat  dist amu & ego
            	outFile.write(",") 
            	#outFile.write(str(amu.position_disp[0]-car1.position_disp[0]))#lat  dist amu & car1
            	#outFile.write(",") 
            	#outFile.write(str(amu.position_disp[0]-car2.position_disp[0]))#lat  dist amu & car2
            	#outFile.write(",")
            	#outFile.write(str(amu.position_disp[0]-car3.position_disp[0]))#lat  dist amu & car3
            	#outFile.write(",")  
            	outFile.write(str(Ecar.velocity.x)) ##long vel  ego
            	outFile.write(",")
            	#outFile.write(str(Ecar.velocity.y)) ##lat  vel  ego
            	#outFile.write(",")
            	#outFile.write(str(amu.velocity[1]-car1.velocity[1]))##long vel amu & car1
            	#outFile.write(",")
            	#outFile.write(str(amu.velocity[1]-car2.velocity[1]))##long vel amu & car2
            	#outFile.write(",")
            	#outFile.write(str(amu.velocity[1]-car3.velocity[1]))##long vel amu & car3
            	outFile.write(str(Ecar.acceleration))#
            	outFile.write("\n") 
            else:print("--- %s seconds ---" % (time.time() - start_time))
            if (amu.position_disp[1]<1) or ((-4<(Ecar.position_disp[1]-amu.position_disp[1])<4)and(-2<(Ecar.position_disp[0]-amu.position_disp[0])<2)) or ((-4<(Ecar.position_disp[1]-car3.position_disp[1])<4)and(-2<(Ecar.position_disp[0]-car3.position_disp[0])<2)) or ((-4<Ecar.position_disp[1]-car2.position_disp[1]<4)and(-2<Ecar.position_disp[0]-car2.position_disp[0]<2)) or ((-4<Ecar.position_disp[1]-car1.position_disp[1]<4)and(-2<Ecar.position_disp[0]-car1.position_disp[0]<2)) or ((-4<(Ecar.position_disp[1]-car4.position_disp[1])<4)and(-2<(Ecar.position_disp[0]-car4.position_disp[0])<2))or ((-4<(Ecar.position_disp[1]-car5.position_disp[1])<4)and(-2<(Ecar.position_disp[0]-car5.position_disp[0])<2)) or ((Ecar.position_disp[0]>14.5) or (Ecar.position_disp[0]<0)) :
                if (amu.position_disp[1]<1):
                    print("End of The round")
                else:
                    print("Crash")
                break




            # Drawing
            self.screen.fill((150, 150, 150))
            pygame.draw.rect(self.screen,(255, 255, 255) , [8  , 0, 6, 1000])##[left, top, width, height]
            pygame.draw.rect(self.screen,(255, 255, 255) , [131, 0, 6, 1000])
            lane_positions_1 = [[49, 1000-i*80, 6, 50] for i in range(1000)]
            lane_positions_2 = [[90, 1000-i*80, 6, 50] for i in range(1000)]
            for p in lane_positions_1:
                p_disp = p
                pygame.draw.rect(self.screen,(255, 255, 255), p_disp)
            for H in lane_positions_2:
                p_disp = H
                pygame.draw.rect(self.screen,(255, 255, 255), p_disp)     
      

            rotated  = pygame.transform.rotate(Ecar_image, Ecar.angle)
            rotated_amu  = amu_image
            rotated1 = car_image1
            rotated2 = car_image2 
            rotated3 = car_image3
            rotated4 = car_image4 
            rotated5 = car_image5

 
            rect = rotated.get_rect()
            rect_amu = rotated_amu.get_rect()
            rect1 = rotated1.get_rect()
            rect2 = rotated2.get_rect()
            rect3 = rotated3.get_rect()
            rect4 = rotated4.get_rect()
            rect5 = rotated5.get_rect()
            
            self.screen.blit(rotated, Ecar.position_disp * ppu - (rect.width / 2, rect.height / 2))
            self.screen.blit(rotated_amu, amu.position_disp * ppu - (rect_amu.width / 2, rect_amu.height / 2))
            self.screen.blit(rotated1, car1.position_disp * ppu - (rect1.width / 2, rect1.height / 2))
            self.screen.blit(rotated2, car2.position_disp * ppu- (rect2.width / 2, rect2.height / 2))
            self.screen.blit(rotated3, car3.position_disp * ppu  - (rect3.width / 2, rect3.height / 2))
            self.screen.blit(rotated4, car4.position_disp * ppu- (rect4.width / 2, rect4.height / 2))
            self.screen.blit(rotated5, car5.position_disp * ppu  - (rect5.width / 2, rect5.height / 2))
#            pygame.display.flip()
            pygame.display.update()

            self.clock.tick(self.ticks)
        pygame.quit()


################################################################################
if __name__ == '__main__':
    game = Start()
    game.run()
