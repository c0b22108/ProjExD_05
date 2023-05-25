import sys
import random
import pygame as pg

WIDTH = 1024
HEIGHT = 1024
CAMERA_POS = (WIDTH // 2, HEIGHT - 200)

nonplayer_rect_lst = []

class Player(pg.sprite.Sprite):
    
    size = (64, 64)
    
    move_dict = {
        pg.K_LEFT: (-1, 0),
        pg.K_a: (-1, 0),
        pg.K_RIGHT: (1, 0),
        pg.K_d: (1, 0),
        pg.K_UP: (0, -1),
        pg.K_SPACE: (0, -1)
        
    }
    
    

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pg.Surface(__class__.size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        # self.gravity_vel = 5
        # self.jump_power = 256
        # self.is_ground = False
        self.box_timer = 0
        self.curve_timer = 0
        self.my_timer = 0
        self.vel_explode = [0,0]
        
        
        #Kodai marge
        self.gravity_acc = 1
        self.walk_acc = 2
        self.walk_vel_max = 20
        self.jump_init_vel = 20
        self.is_ground = False
        self.acc = [0, 0]
        self.vel = [0, 0]

    def update(self, key_lst: dict):
        self.my_timer += 1
        self.update_box(key_lst)
        self.update_bomb(key_lst)
        self.update_throw_predict(key_lst)
        self.update_explode_blast()
        
        
        self.acc = [0, 0]
        for d in __class__.move_dict:
            if key_lst[d]:
                self.acc[0] += self.walk_acc * self.move_dict[d][0]
                if self.is_ground:
                    self.vel[1] = self.jump_init_vel * self.move_dict[d][1]
                    if self.vel[1] < 0:
                        self.is_ground = False

        if not self.is_ground:
            self.acc[1] += self.gravity_acc

        self.vel[0] += self.acc[0]
        if self.vel[0] < -self.walk_vel_max:
            self.vel[0] = -self.walk_vel_max
        elif self.vel[0] > self.walk_vel_max:
            self.vel[0] = self.walk_vel_max
        self.vel[1] += self.acc[1]
        """
        for d in __class__.move_dict:
            if key_lst[d]:
                self.rect.x += self.move_dict[d][0] * 3
                if self.is_ground:
                    self.rect.y += self.move_dict[d][1] * self.jump_power
                    if self.move_dict[d][1] < 0:
                        self.is_ground = False

        if not self.is_ground:
            self.rect.y += self.gravity_vel
"""
    
    def update_box(self,key_lst: dict):
        """
        Press mouse Left
        box throw 
        """        
        
        #次に投げれるようになるまでのフレーム数
        if self.my_timer - self.box_timer < 30:
            return
        
        
        pg.event.get()
        if pg.mouse.get_pressed()[0]:
            self.box_timer = self.my_timer
            throw_arg = [0,0]
            mouse_pos = list(pg.mouse.get_pos())
            player_pos = list(self.rect.center)
            throw_arg[0] = (mouse_pos[0] - player_pos[0])/15
            throw_arg[1] = (mouse_pos[1] - player_pos[1])/15
            #print(throw_arg)
            Box((self.rect.centerx,self.rect.centery - 10),tuple(throw_arg),power=2.0)
            
            
            
    def update_bomb(self,key_lst: dict):
        """
        Press mouse Riglt
        bomb throw 
        """        
        
        #次に投げれるようになるまでのフレーム数
        if self.my_timer - self.box_timer < 30:
            return
        
        
        pg.event.get()
        if pg.mouse.get_pressed()[2]:
            self.box_timer = self.my_timer
            throw_arg = [0,0]
            mouse_pos = list(pg.mouse.get_pos())
            player_pos = list(self.rect.center)
            throw_arg[0] = (mouse_pos[0] - player_pos[0])/15
            throw_arg[1] = (mouse_pos[1] - player_pos[1])/15
            #print(throw_arg)
            Bomb(self.rect.center,tuple(throw_arg),power=2.0)
            
    def update_throw_predict(self,key_lst: dict):
        """
        Press Shift
        draw throw curve 
        """        
        
        #次に投げれるようになるまでのフレーム数
        if self.my_timer - self.curve_timer < 10:
            return
        
        
        pg.event.get()
        #CTRLで予測線
        if key_lst[pg.K_RCTRL]:
            self.curve_timer = self.my_timer
            throw_arg = [0,0]
            mouse_pos = list(pg.mouse.get_pos())
            player_pos = list(self.rect.center)
            throw_arg[0] = (mouse_pos[0] - player_pos[0])/15
            throw_arg[1] = (mouse_pos[1] - player_pos[1])/15
            #print(throw_arg)
            Throw_predict(self.rect.center,tuple(throw_arg),power=2.0)
            #Bomb(self.rect.center,tuple(throw_arg),power=2.0)
            
    def update_explode_blast(self):
        self.vel[0] += self.vel_explode[0]
        self.vel[1] += self.vel_explode[1]
        if self.is_ground:
            self.vel_explode = [0,0]
        #else:
            #if self.vel_explode != [0,0]:
                #self.vel_explode[1] += 1
                #print(self.vel_explode)
    
    def set_vel_explode(self,vx,vy):
        self.vel_explode = [vx,vy]
    
    def set_vel(self, vx: float, vy: float):
        self.vel[0] = vx
        self.vel[1] = vy
        
class Block(pg.sprite.Sprite):
    size =  (50, 50)

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pg.Surface(__class__.size)
        self.image.fill((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.center = pos
     
     
            
class Box(pg.sprite.Sprite):
    """
    playerがなげるBoxClassです
    """
    boxes = pg.sprite.Group()
    def __init__(self, pos: tuple[int, int],vel:tuple[float,float],power:float=5):
        global nonplayer_rect_lst
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.gravity_val = 1
        self.life = 0
        self.is_ground = False
        self.vel = list(vel)
        self.acc = [0,0]
        self.acc = [0,self.gravity_val]
        __class__.boxes.add(self)
        nonplayer_rect_lst.append(self.rect)
        

    def update(self):
        
        self.life += 1
        if self.life > 6000:
            self.kill()
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        
        
        
        if self.is_ground:
            self.vel[1] = 0
            self.vel[0] = 0
        
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        
    def set_vel(self,vx,vy):
        self.vel[1] = vy
        self.vel[0] = vx
    
    def is_moving(self):
        #[0,0]でないならFalse
        return not self.vel == [0,0]
    
        

class Bomb(pg.sprite.Sprite):
    """
    playerがなげるBombClassです
    """
    bombs = pg.sprite.Group()
    def __init__(self, pos: tuple[int, int],vel:tuple[float,float],power:float=5):
        global nonplayer_rect_lst
        super().__init__()
        self.image = pg.Surface((30, 30))
        self.image.fill((255, 128, 0))
        self.rect = self.image.get_rect()
        #self.image.set_alpha(128)
        self.rect.center = pos
        self.gravity_val = 1
        self.life = 0
        self.is_ground = False
        self.vel = list(vel)
        self.acc = [0,0]
        self.acc = [0,self.gravity_val]
        __class__.bombs.add(self)
        nonplayer_rect_lst.append(self.rect)

    def update(self):
        life_max = 180
        self.life += 1
        
        #自動で消えるまでの時間
        if self.life >= life_max:
            Explode(self.rect.center)
            self.kill()
            
        #爆発までの時間を色で表現
        #self.image.fill((int((255 - 255*self.life/life_max +2 )), max(0,128 - self.life),0 ))
        #print(int(255*self.life/life_max))
        self.image.fill((255 - 128*int((self.life/life_max/120)), 128 * (1 - self.life/life_max), 255 * (self.life/life_max)**2))
        
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        
        
        
        if self.is_ground:
            self.vel[1] = 0
            self.vel[0] = 0
        
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        
    def set_vel(self,vx,vy):
        self.vel[1] = vy
        self.vel[0] = vx
        
class Explode(pg.sprite.Sprite):
    """
    Bombが爆発した時に呼び出されるExplodeClassです
    """
    explodes = pg.sprite.Group()
    def __init__(self, pos: tuple[int, int],power:float=7):
        global nonplayer_rect_lst
        super().__init__()
        rad = power * 16
        self.image = pg.Surface((rad, rad))
        self.image.fill((200, 0, 0))
        pg.draw.circle(self.image, (200, 0, 0), (rad, rad), rad)
        self.image.set_colorkey((255, 255, 255))
        self.image.set_alpha(128)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.life = 0
        __class__.explodes.add(self)
        nonplayer_rect_lst.append(self.rect)

    def update(self):
        self.life += 1
        #自動で消えるまでの時間
        if self.life > 12:
            self.kill()
          

class Throw_predict(pg.sprite.Sprite):
    """
    playerがなげるものの予測線Classです
    """
    predicts = pg.sprite.Group()
    def __init__(self, pos: tuple[int, int],vel:tuple[float,float],power:float=5):
        global nonplayer_rect_lst
        super().__init__()
        self.image = pg.Surface((15, 15))
        self.image.fill((255, 200, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.gravity_val = 1
        self.life = 0
        self.vel = list(vel)
        self.acc = [0,0]
        self.acc = [0,self.gravity_val]
        __class__.predicts.add(self)
        nonplayer_rect_lst.append(self.rect)

    def update(self):
        
        self.life += 1
        #自動で消えるまでの時間
        if self.life > 180:
            self.kill()
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        
    def set_vel(self,vx,vy):
        self.vel[1] = vy
        self.vel[0] = vx
        
def main():
    pg.display.set_caption("proto")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.Surface((WIDTH, HEIGHT))
    bg_img.fill((0, 0, 0))

    global nonplayer_rect_lst
    nonplayer_rect_lst.append(bg_img.get_rect())

    player = Player(CAMERA_POS)
    
    blocks = pg.sprite.Group()
    for i in range(-WIDTH, WIDTH):
        blocks.add(Block((i * Block.size[0], HEIGHT)))
    for i in range(10):
        for j in range(10):
            blocks.add(Block((i * 2000, HEIGHT - j * Block.size[1])))
            blocks.add(Block((i * 2000 + Block.size[0], HEIGHT - j * Block.size[1])))
    for b in blocks:
        nonplayer_rect_lst.append(b.rect)
    
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        
        
        if random.random() > 0.001:
            print(nonplayer_rect_lst[0].center)
        # #Boxをnonplayerlstにいれる
        # for i in Box.boxes:
        #     if  not i in nonplayer_rect_lst:
        #         nonplayer_rect_lst.append(i.rect)
        # #Bombをnonplayerlstにいれる
        # for i in Bomb.bombs:
        #     if  not i in nonplayer_rect_lst:
        #         nonplayer_rect_lst.append(i.rect)
        # #Explodeをnonplayerlstにいれる
        # for i in Explode.explodes:
        #     if  not i in nonplayer_rect_lst:
        #         nonplayer_rect_lst.append(i.rect)
        # #Throwをnonplayerlstにいれる
        # for i in Throw_predict.predicts:
        #     if  not i in nonplayer_rect_lst:
        #         nonplayer_rect_lst.append(i.rect)
        
        

        key_lst = pg.key.get_pressed()

        player.update(key_lst)
        
                    
        #Box
        Box.boxes.update()
        #Bomb
        Bomb.bombs.update()
        #Explode
        Explode.explodes.update()
        #predict
        Throw_predict.predicts.update()

        # player.is_ground = False
        
        
        
        # スクロール
        for r in nonplayer_rect_lst:
            r.x -= player.vel[0]
            if not player.is_ground:
                r.y -= player.vel[1]

        
        #毎フレーム落下するとして初期化
        for i in Box.boxes:
            i.is_ground = False
        
        #Boxの接地判定
        collide_lst = pg.sprite.groupcollide(Box.boxes, blocks, False,False)
        #print(collide_lst)
        for i in collide_lst:
            i.is_ground = True
            
        
        #Bombの接地判定
        collide_lst = pg.sprite.groupcollide(Bomb.bombs, blocks, False,False)
        for i in collide_lst:
            i.is_ground = True
        
        #Box同士の衝突判定
        collide_lst = pg.sprite.groupcollide(Box.boxes, Box.boxes, False,False)
    
        for obj,collide_lst_2 in collide_lst.items():
            if len(collide_lst_2) > 1:
                for obj2 in collide_lst_2:
                    if not obj is obj2:
                        if obj.rect.centery < obj2.rect.top :
                            obj.is_ground = True
                            break
                        else:
                            obj2.is_ground = False
                        #obj.is_ground = False
        
    
        #BoxにPlayerが乗るための接地判定
        for b in pg.sprite.spritecollide(player, Box.boxes, False):
            # x方向
            if player.rect.bottom > b.rect.centery:
                if player.vel[0] < 0:
                    for r in nonplayer_rect_lst:
                        r.x += player.vel[0]
                    player.vel[0] = 0
                elif player.vel[0] > 0:
                    for r in nonplayer_rect_lst:
                        r.x += player.vel[0]
                    player.vel[0] = 0
            # y方向
            if b.rect.left <= player.rect.centerx <= b.rect.right:
                for r in nonplayer_rect_lst:
                    r.y += player.vel[1]
                if player.vel[1] > 0:
                    player.is_ground = True
                player.vel[1] = 0
                player.vel[0] *= 0.8
        
        """if len(collide_lst) > 0:
            for b in collide_lst:
                if b.life > 60:
                    if player.rect.top < b.rect.bottom:
                        player.rect.top = b.rect.bottom
                    if player.rect.bottom > b.rect.top:
                        player.rect.bottom = b.rect.top
                        player.is_ground = True"""
        #BombとBoxのCollide
        collide_lst = pg.sprite.groupcollide(Bomb.bombs, Box.boxes, False,False)
        for bomb in collide_lst:
            bomb.set_vel(0,0)
            bomb.is_ground = True
        #Bombによって召喚されたExplodeとBoxのCollide
        collide_lst = pg.sprite.groupcollide(Explode.explodes, Box.boxes, False,True)
        
        #ExplodeとPlayerの当たり判定　あたると吹っ飛ぶ
        collide_lst = pg.sprite.spritecollide(player,Explode.explodes, False,False)
        for explode in collide_lst:
            
            throw_arg = [0,0]
            explode_pos = list(explode.rect.center)
            player_pos = list(player.rect.center)
            power_border = 4
            throw_arg[0] = -(explode_pos[0] - player_pos[0])/power_border + 0.001
            throw_arg[1] = -(explode_pos[1] - player_pos[1])/power_border + 0.001
            print(throw_arg)
            player.vel[0] += throw_arg[0]
            player.vel[1] += throw_arg[1]
    
        #予測線の接地判定
        collide_lst = pg.sprite.groupcollide(Throw_predict.predicts, blocks, True,False)
        
        # Playerとブロックの衝突判定
        collide_lst = pg.sprite.spritecollide(player, blocks, False)
        if len(collide_lst) == 0:
            player.is_ground = False
        else:
            for b in collide_lst:
                # x方向
                if player.rect.bottom > b.rect.centery:
                    if player.vel[0] < 0:
                        for r in nonplayer_rect_lst:
                            r.x += player.vel[0]
                        player.vel[0] = 0
                    elif player.vel[0] > 0:
                        for r in nonplayer_rect_lst:
                            r.x += player.vel[0]
                        player.vel[0] = 0
                # y方向
                if b.rect.left <= player.rect.centerx <= b.rect.right:
                    for r in nonplayer_rect_lst:
                        r.y += player.vel[1]
                    if player.vel[1] > 0:
                        player.is_ground = True
                    player.vel[1] = 0
                    player.vel[0] *= 0.8

        screen.blit(bg_img, (0, 0))
        blocks.draw(screen)
        Box.boxes.draw(screen)
        Bomb.bombs.draw((screen))
        Explode.explodes.draw((screen))
        Throw_predict.predicts.draw((screen))
        screen.blit(player.image, player.rect)
        pg.display.update()

        tmr += 1
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    
