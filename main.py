XP = SpriteKind.create()

char_level = 1
xp_bar = statusbars.create(120, 4, StatusBarKind.magic)
xp_bar.bottom = 110
xp_bar.max = 10
xp_bar.value = 0
lta: number = 0
xp_to_add = 0
xp_bar.set_flag(SpriteFlag.INVISIBLE, True)
gstate = "battle"

#xp_to_add = game.ask_for_number("HOW MUCH")
game.show_long_text("Locked in an endless conflict, our hero has been fighting back the armies of the dark lord for some time now. Her only solace? each one defeated makes her ever stronger. Unfortunately this newfound power comes at a cost, she can only absorb it by being defeated by the same enemies she fights!", DialogLayout.FULL)
text_sprite = textsprite.create(str(xp_to_add))
text_sprite.set_icon(assets.image("EXP"))
text_sprite.left = 0
text_sprite.top = 0
text_sprite.set_outline(1, 6)

def rotate(xp: Sprite):
    if randint(0,1) == 1:
        for i in range(0, randint(0, 120)):
            transformSprites.change_rotation(xp, 3)
    else:
        for i in range(0, randint(0, 120)):
            transformSprites.change_rotation(xp, -3)


def go_to_xp():
        global lta
        for pip in sprites.all_of_kind(XP):
            global lta
            transformSprites.rotate_sprite(pip, 90)
            story.sprite_move_to_location(pip, xp_bar.x, xp_bar.y, 500)
            sprites.destroy(pip, effects.rings, 50)
            xp_bar.value +=1
            if xp_bar.value == xp_bar.max:
                lta +=1
                console.log(lta)
                xp_bar.value = 0
                xp_bar.max += 20
                effects.bubbles.start_screen_effect(500)

def level():
    global xp_to_add, gstate, h1a, h1h, h1atk, h1def, lta, p1mp, batk, bdef, ba, bh
    n = 0
    xp_bar.set_flag(SpriteFlag.INVISIBLE, False)
    while n < xp_to_add:


        xp = sprites.create(assets.image("EXP"), XP)
        xp.scale = 0.6
        story.sprite_move_to_location(xp, randint(20,140), randint(20,60), 300)
        def startrotate():
            rotate(xp)
        timer.background(startrotate)
        n += 1
        text_sprite.set_text(str(xp_to_add - n))

    go_to_xp()
    xp_to_add = 0
    console.log(lta)
    for i in range (0,lta):
        h1a -= 10
        h1h += 25
        h1atk += 10
        h1def += 5
        p1mp += 20
    sprites.set_data_number(hero, "agi", h1a)
    sprites.set_data_number(hero, "atk", h1atk)
    sprites.set_data_number(hero, "def", h1def)
    sprites.set_data_number(hero, "hp", h1h)
    sprites.set_data_number(hero, "mp", p1mp)
    console.log("agi" + sprites.read_data_number(hero, "agi") + " ATK: " + sprites.read_data_number(hero, "atk") + " DEF: " + sprites.read_data_number(hero, "def") + " HP: " + sprites.read_data_number(hero, "hp"))
    for bar in statusbars.all_of_kind(1):
        sprites.destroy(bar)
    for bars in statusbars.all_of_kind(2):
        sprites.destroy(bars)
    for bar2 in statusbars.all_of_kind(4):
        sprites.destroy(bar2)
    sprites.set_data_number(boss, "atk", batk)
    sprites.set_data_number(boss, "def", bdef)
    sprites.set_data_number(boss, "agi", ba)
    sprites.set_data_number(boss, "hp", bh)
    setup_bars(hero)
    setup_bars(boss)
    lta = 0
    gstate = "battle"
    info.set_score(0)
    xp_bar.set_flag(SpriteFlag.INVISIBLE, True)
#level()



Actor = SpriteKind.create()
Party = SpriteKind.create()
hero = sprites.create(assets.image("h1"), Actor)
hero.set_position(101, 66)
boss_sprites = [assets.image("e1"), assets.image("e2")]
boss = sprites.create(boss_sprites[randint(0,1)], Actor)
boss.set_position(29, 76)
scene.set_background_image(assets.image("bg"))



bmenuopen = False
my_menu: miniMenu.MenuSprite = None
h1a = 100
ba = 170
bh = 100
h1h = 125
batk = 25
h1atk = 50
bdef = 10
h1def = 10
p1mp = 20

sprites.set_data_boolean(hero, "acting", False)
sprites.set_data_boolean(boss, "acting", False)
sprites.set_data_number(hero, "agi", h1a)
sprites.set_data_number(boss, "agi", ba)
sprites.set_data_string(hero, "nam", "Hero")
sprites.set_data_number(hero, "hp", h1h)
sprites.set_data_number(boss, "hp", bh)
sprites.set_data_number(hero, "atk", h1atk)
sprites.set_data_number(boss, "atk", batk)
sprites.set_data_number(hero, "def", h1def)
sprites.set_data_number(boss, "def", bdef)
sprites.set_data_number(hero, "mp", p1mp)



def setup_bars(char: Sprite):
    agi_bar = statusbars.create(20, 4, 2)
    agi_bar.attach_to_sprite(char,2)
    agi_bar.max = sprites.read_data_number(char, "agi")
    agi_bar.value = 0
    if sprites.read_data_number(char, "mp") >0:
        mp_bar = statusbars.create(20, 4, 4)
        mp_bar.set_color(6, 12)
        mp_bar.attach_to_sprite(char, 4)
        mp_bar.max = sprites.read_data_number(char, "mp")
        mp_bar.value = sprites.read_data_number(char, "mp")
    health_bar = statusbars.create(20,4,1)
    health_bar.attach_to_sprite(char, 6)
    health_bar.max = sprites.read_data_number(char, "hp")
    health_bar.value = health_bar.max


for char in sprites.all_of_kind(Actor):
    setup_bars(char)
hero.set_kind(Party)




def bar_prog(char: Sprite):
    global bmenuopen
    if sprites.read_data_boolean(char, "acting") == True:
        return
    if statusbars.get_status_bar_attached_to(2, char).value == statusbars.get_status_bar_attached_to(2, char).max-1 and bmenuopen and char.kind() == Party:
            return
    else:
        statusbars.get_status_bar_attached_to(2, char).value += 1
    if statusbars.get_status_bar_attached_to(2, char).value == statusbars.get_status_bar_attached_to(2, char).max and bmenuopen and char.kind() == Party:
        return
    if statusbars.get_status_bar_attached_to(2, char).value == statusbars.get_status_bar_attached_to(2, char).max and char.kind() == Party:
        bmenuopen = True
        pmenu(char)

    elif statusbars.get_status_bar_attached_to(2, char).value == statusbars.get_status_bar_attached_to(2, char).max and char.kind() == Actor:
        statusbars.get_status_bar_attached_to(2, char).value = 0
        sprites.set_data_boolean(char, "acting", True)
        def resenatt():
            enemy_att(char)
        timer.background(resenatt)


def pmenu(char: Sprite):
    global bmenuopen
    my_menu = miniMenu.create_menu(miniMenu.create_menu_item("Attack"),miniMenu.create_menu_item("Defend"), miniMenu.create_menu_item("Special"))
    my_menu.set_title(sprites.read_data_string(char, "nam"))

    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.ROWS, 2)
    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.COLUMNS, 2)
    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.WIDTH, 120)
    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.HEIGHT, 40)
    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.BACKGROUND_COLOR, 1)
    my_menu.y = 100
    my_menu.x = 80
    my_menu.set_menu_style_property(miniMenu.MenuStyleProperty.USE_AS_TEMPLATE, 1)
    def on_button_pressed(selection, selectedIndex):
        global bmenuopen

        statusbars.get_status_bar_attached_to(2, char).value = 0
        my_menu.close()
        if selectedIndex == 0:
            bmenuopen = False
            sprites.set_data_boolean(char, "acting", True)
            def resolveatt():
                p_attack(char)
            timer.background(resolveatt)
        elif selectedIndex == 1:
            bmenuopen = False
            return
        elif selectedIndex == 2:
            sprites.set_data_boolean(char, "acting", True)
            if sprites.read_data_number(char, "agi") == h1a:
                
                def resh1sp():
                    if statusbars.get_status_bar_attached_to(4, char).value >= 10:
                        h1_specials(char)
                        

                    else:
                        story.sprite_say_text(statusbars.get_status_bar_attached_to(1, char), "Out of MP!")
                        pmenu(char)
                timer.background(resh1sp)
    my_menu.on_button_pressed(controller.A, on_button_pressed)

def p_attack(char: Sprite):

    story.sprite_move_to_location(char, char.x-20, char.y, 100)
    pause(500)
    story.sprite_move_to_location(char, char.x+20, char.y, 100)
    sprites.set_data_boolean(char, "acting", False)
    fxspri = sprites.create(assets.image("blank"))
    fxspri.set_position(boss.x, boss.y)
    fxspri.z = 100
    animation.run_image_animation(fxspri,assets.animation("attsp"), 50, False)
    pause(150)
    dam_taken = sprites.read_data_number(char, "atk") - sprites.read_data_number(boss, "def") +1
    statusbars.get_status_bar_attached_to(1, boss).value -= dam_taken
    def takedam():
            damtext(dam_taken, boss)
    timer.background(takedam)
    fxspri.destroy()

def h1_specials(char: Sprite):
    global bmenuopen
    my_menu = miniMenu.create_menu(miniMenu.create_menu_item("Fire"),miniMenu.create_menu_item("Big Hit"),)
    my_menu.set_title(sprites.read_data_string(char, "nam") + " Specials")
    my_menu.y = 100
    my_menu.x = 80
    def on_button_pressed(selection, selectedIndex):
        global bmenuopen
        my_menu.close()
        bmenuopen = False
        if selectedIndex == 0:
            def ressp1():
                if statusbars.get_status_bar_attached_to( 4, char).value >= 20:
                    h1_fire(char)
                    statusbars.get_status_bar_attached_to(4, char).value -= 20
                else:
                    story.sprite_say_text(statusbars.get_status_bar_attached_to(1, char), "Not enough MP!")
                    pmenu(char)
            timer.background(ressp1)
        else:
            def ressp2():
                if statusbars.get_status_bar_attached_to(4, char).value >= 10:
                    h1_bh(char)
                    statusbars.get_status_bar_attached_to(4, char).value -= 10
                else:
                    story.sprite_say_text(statusbars.get_status_bar_attached_to(1, char), "Not enough MP!")
                    pmenu(char)
            timer.background(ressp2)
    my_menu.on_button_pressed(controller.A, on_button_pressed)


def h1_fire(char: Sprite):
    story.sprite_move_to_location(char, char.x-20, char.y, 100)
    pause(500)
    story.sprite_move_to_location(char, char.x+20, char.y, 100)
    sprites.set_data_boolean(char, "acting", False)
    fxspri = sprites.create(assets.image("blank"))
    fxspri.set_position(boss.x, boss.y)
    fxspri.z = 100
    animation.run_image_animation(fxspri,assets.animation("fire"), 50, False)
    pause(200)
    dam_taken = sprites.read_data_number(char, "atk") + 20 - sprites.read_data_number(boss, "def")
    statusbars.get_status_bar_attached_to(1, boss).value -=  dam_taken
    console.log(dam_taken) 
    def takedam():
        damtext(dam_taken, boss)
    timer.background(takedam)
    fxspri.destroy()

def h1_bh(char: Sprite):
    story.sprite_move_to_location(char, char.x-20, char.y, 100)
    pause(500)
    story.sprite_move_to_location(char, char.x+20, char.y, 100)
    sprites.set_data_boolean(char, "acting", False)
    fxspri = sprites.create(assets.image("blank"))
    fxspri.set_position(boss.x, boss.y)
    fxspri.z = 100
    animation.run_image_animation(fxspri,assets.animation("big"), 50, False)
    pause(250)
    dam_taken = sprites.read_data_number(char, "atk") + 10 - sprites.read_data_number(boss, "def") 
    statusbars.get_status_bar_attached_to(1, boss).value -= dam_taken
    def takedam():
            damtext(dam_taken, boss)
    timer.background(takedam)
    fxspri.destroy()


def enemy_att(char: Sprite):
    story.sprite_move_to_location(char, char.x+20, char.y, 100)
    pause(500)
    story.sprite_move_to_location(char, char.x-20, char.y, 100)
    sprites.set_data_boolean(char, "acting", False)
    fxspri = sprites.create(assets.image("blank"))
    target = sprites.all_of_kind(Party)[0]
    fxspri.set_position(target.x, target.y)
    fxspri.z = 100
    animation.run_image_animation(fxspri,assets.animation("attsp"), 50, False)
    pause(150)
    dam_taken = sprites.read_data_number(char, "atk") - sprites.read_data_number(hero, "def")
    statusbars.get_status_bar_attached_to(1, hero).value -= dam_taken
    console.log("player damage taken: " + dam_taken)
    def takedam():
            damtext(dam_taken, hero)
    timer.background(takedam)
    fxspri.destroy()

def tick():
    global gstate
    if gstate == "battle":
        for member in sprites.all_of_kind(Party):
            bar_prog(member)
        bar_prog(boss)
game.on_update(tick)

def on_zero(status):
    global gstate, xp_to_add
    if statusbars.get_status_bar_attached_to(1, boss).value <= 0:
        boss.start_effect(effects.disintegrate, 500)
        statusbars.get_status_bar_attached_to(1, boss).value = statusbars.get_status_bar_attached_to(1, boss).max
        if sprites.read_data_number(boss, "agi") > 5:
            sprites.set_data_number(boss, "agi", sprites.read_data_number(boss, "agi")-15)
        sprites.set_data_number(boss, "atk", sprites.read_data_number(boss, "atk")+5)
        sprites.set_data_number(boss, "def", sprites.read_data_number(boss, "def")+5)
        sprites.set_data_number(boss, "hp", sprites.read_data_number(boss, "hp")+25)
        xp_to_add += randint(8,12)
        console.log("def: " + sprites.read_data_number(boss, "def") + " atk: " + sprites.read_data_number(boss, "atk") + " agi: " + sprites.read_data_number(boss, "agi"))
        text_sprite.set_text(str(xp_to_add))
        sprites.destroy(statusbars.get_status_bar_attached_to(2, boss))
        sprites.destroy(statusbars.get_status_bar_attached_to(1, boss))
        setup_bars(boss)
        info.change_score_by(1)
        boss.set_image(boss_sprites[randint(0,1)])
    elif statusbars.get_status_bar_attached_to(1, hero).value <= 0:
        gstate = "level"
        level()
statusbars.on_zero(StatusBarKind.health, on_zero)

def damtext(taken: number, char: Sprite):
    damnumber = textsprite.create(str(taken))
    damnumber.x = char.x
    damnumber.y = char.y
    damnumber.vy = -50
    damnumber.ay = 100
    damnumber.vx = randint(-20,20)
    damnumber.set_outline(1, 2)
    damnumber.set_flag(SpriteFlag.AUTO_DESTROY, True)