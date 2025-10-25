import pygame, sys, pygame.mixer



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Sounds/fantasy-medieval-ambient-237371.mp3")
pygame.mixer.music.play(-1)
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("A Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)


font = pygame.font.Font("Fonts/MedievalSharp-Regular.ttf", 40)

def drawText(text, x, y, color):
    renderedtext = font.render(text, True, color)
    screen.blit(renderedtext, (x, y))

click_sound = pygame.mixer.Sound("Sounds/mixkit-typewriter-soft-click-1125.wav")

def drawButton(text, x, y, w, h, color, hover_color):
    global click
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)
    if rect.collidepoint(mouse_pos) and click:
        click_sound.play()
    return rect



def main():
    global click, state, playernamed
    availableChoices = ["Trainer", "Scholar"]
    state = "menu"
    last_state = None
    playerName = ""
    playernamed = False
    running = True
    weapon = ""
    gear = ""
    money = 5
    inventory = []


    storeitems = {
        "Battle Axe": {"price": 30, "type": "weapon", "damage": 15, "description": "A heavy axe that deals strong melee damage."},
        "Health Potion": {"price": 5, "type": "consumable", "heal": 20, "description": "Restores 20 HP when used."},
        "Chainmail": {"price": 50, "type": "armor", "defense": 10, "description": "Provides solid protection against attacks."},
        "Leather Armor": {"price": 25, "type": "armor", "defense": 5, "description": "Light armor offering minimal protection but allows quick movement."},
        "Antidote": {"price": 7, "type": "consumable", "cure": "poison", "description": "Cures poison and prevents further damage from toxins."}
    }

    def weaponsmith(money, inventory, storeitems):
        global state, click
        drawText("Welcome to the shop", 600, 300, red)
        y_pos = 500
        x_pos = 300
        max_per_row = 3

        for idx, (item_name, item_data) in enumerate(list(storeitems.items())):
            if drawButton(f"{item_name} - ${item_data['price']}", x_pos, y_pos, 385, 100, green, grey).collidepoint(pygame.mouse.get_pos()) and click:
                if money >= item_data["price"]:
                    money -= item_data["price"]
                    inventory.append(item_name)
                    del storeitems[item_name]


            x_pos += 400


            if (idx + 1) % max_per_row == 0:
                x_pos = 300
                y_pos += 150




        if drawButton("Exit Shop", 1400, 50, 200, 100, red, grey).collidepoint(pygame.mouse.get_pos()) and click:
            state = "protect_village"
        click = False
        return money










    click = False

    while running:
        screen.fill(black)
        mouse_pos = pygame.mouse.get_pos()

        # --- EVENT HANDLING ---
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "menu":
                        running = False
                    else:
                        last_state = state
                        state = "menu"
                        click = False

                elif state == "name":
                    if event.key == pygame.K_BACKSPACE:
                        playerName = playerName[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("Player name is:", playerName)
                        state = "game"
                        playernamed = True
                    else:
                        playerName += event.unicode

        # --- DRAW SECTION ---
        if state == "menu":
            drawText("The Dawn of Lumeria", 810, 150, red)
            drawText("Press ESC to quit", 850, 600, white)
            if playernamed == False:
                if drawButton("Start Game", 895, 400, 200, 100, black, grey).collidepoint(mouse_pos) and click:
                    state = "name"
                    click = False
            else:
                if last_state and drawButton("Resume", 890, 400, 200, 100, black, grey).collidepoint(mouse_pos) and click:
                    state = last_state
                    click = False


        elif state == "name":
            drawText("Enter your name: " + playerName, 800, 500, white)

        elif state == "game":
            story_lines = [
                f"Welcome, {playerName}! You are tasked with an important mission:",
                "saving the mystical kingdom of Lumeria from the mischievous Shadow Sprites",
                "that have stolen the kingdom’s glowing crystals. Without these crystals,",
                "the kingdom’s light will fade, and the creatures of Lumeria will fall into eternal darkness.",
                "",
                "You wake up to the first light of dawn filtering through your window.",
                "The air is still, but a weight presses on your chest—a sense of responsibility",
                "and purpose. Today is not an ordinary day; the choices you make will shape the path ahead.",
                "The quiet of the morning leaves only your thoughts and the soft sound of the world",
                "stirring outside.",
                "",
                "What is going to be your weapon choice for this adventure?"
            ]
            y_offset = 50
            for line in story_lines:
                drawText(line, 100, y_offset, white)
                y_offset += 60

            if drawButton("Sword", 500, 800, 300, 100, red, green).collidepoint(mouse_pos) and click:
                weapon = "Sword"
                state = "gear"
                click = False
            elif drawButton("Dagger", 850, 800, 300, 100, red, green).collidepoint(mouse_pos) and click:
                weapon = "Dagger"
                state = "gear"
                click = False
            elif drawButton("Bow", 500, 950, 300, 100, red, green).collidepoint(mouse_pos) and click:
                weapon = "Bow"
                state = "gear"
                click = False
            elif drawButton("Staff", 850, 950, 300, 100, red, green).collidepoint(mouse_pos) and click:
                weapon = "Staff"
                state = "gear"
                click = False

        elif state == "gear":
            drawText("Choose an extra item:", 200, 200, white)
            accesorieLines = [
                "Pendant of Wind – alerts the player to approaching enemies with a faint shimmer.",
                "Boots of Quiet – muffles footsteps, making the player harder to detect.",
                "Amulet of Light – illuminates dark areas slightly, helping navigation.",
                "Gloves of Grip – improves handling, reducing the chance of dropping items or tools."
            ]
            y_offset = 300
            for line in accesorieLines:
                drawText(line, 200, y_offset, white)
                y_offset += 60

            if drawButton("Pendant of Wind", 700, 800, 300, 100, red, green).collidepoint(mouse_pos) and click:
                gear = "Pendant of Wind"
                state = "story"
                click = False
            elif drawButton("Boots of Quiet", 1050, 800, 300, 100, red, green).collidepoint(mouse_pos) and click:
                gear = "Boots of Quiet"
                state = "story"
                click = False
            elif drawButton("Amulet of Light", 700, 950, 300, 100, red, green).collidepoint(mouse_pos) and click:
                gear = "Amulet of Light"
                state = "story"
                click = False
            elif drawButton("Gloves of Grip", 1050, 950, 300, 100, red, green).collidepoint(mouse_pos) and click:
                gear = "Gloves of Grip"
                state = "story"
                click = False

        elif state == "story":
            drawText(f"You chose the {weapon} and {gear}!", 200, 40, white)
            story_after_weapon = [
                f"With the {weapon} in your hands, a spark of determination burns brighter.",
                "Outside, the village stirs awake — but you sense danger on the horizon.",
                "",
                "Your path forward is unclear. The morning sun glints off the rooftops,",
                "and in the distance you hear both laughter and whispers of fear.",
                "",
                "It’s time to decide your first move:"
            ]
            y_offset = 100
            for line in story_after_weapon:
                drawText(line, 200, y_offset, white)
                y_offset += 60

            if drawButton("Visit the Village Elder", 500, 800, 400, 100, red, green).collidepoint(mouse_pos) and click:
                state = "elder"
                click = False
            elif drawButton("Head straight into the Forest", 1000, 800, 520, 100, red, green).collidepoint(mouse_pos) and click:
                state = "forest"
                click = False
            elif drawButton("Scout the Village Outskirts", 750, 950, 500, 100, red, green).collidepoint(mouse_pos) and click:
                state = "outskirts"
                click = False

        elif state == "elder":
            elder_story = [
                "The Elder’s hut smells of incense and old wood, the air thick with silence.",
                "He lifts his head as you enter, his wrinkled face carved with worry.",
                "",
                f"‘{playerName},’ he says, his voice rough like gravel, ‘I prayed you would come.’",
                "His eyes fix on your weapon, and then on the gear you carry.",
                "‘Darkness spreads faster than even I feared. The Shadow Sprites are no longer",
                "just tricksters in the night. They burn, they kill, they hunt without rest.’",
                "",
                "He grips your hand tightly, far stronger than you expected for his age.",
                "‘You must choose how you will face them. One path shields the innocent,",
                "the other strikes at the heart of the enemy. But you cannot walk both.’"
            ]

            y_offset = 100
            for line in elder_story:
                drawText(line, 200, y_offset, white)
                y_offset += 60

            if drawButton("Protect the Village – Defend the innocent", 200, 850, 750, 100, red, green).collidepoint(mouse_pos) and click:
                state = "protect_village"
                click = False
            elif drawButton("Strike the Heart – Take the fight to the enemy", 1000, 850, 850, 100, red, green).collidepoint(mouse_pos) and click:
                state = "strike_enemy"
                click = False


        elif state == "forest":
            forest_story = [
                "You step into the dense forest, sunlight barely piercing through the thick canopy.",
                "The air smells of pine and damp earth. Every rustle could be a harmless critter… or something worse.",
                "Your {weapon} feels reassuring in your hands, and the {gear} seems to hum with readiness.",
                "",
                "A fork in the path appears ahead. One trail leads deeper into the shadowy trees,",
                "the other climbs toward a sunlit ridge where the view is clearer but exposed."
            ]


            y_offset = 100
            for line in forest_story:
                drawText(line, 200, y_offset, white)
                y_offset += 60

            if drawButton("Take the shadowy path", 500, 800, 500, 100, red, green).collidepoint(mouse_pos) and click:
                state = "forest_shadow"
                click = False
            elif drawButton("Climb to the sunlit ridge", 1100, 800, 500, 100, red, green).collidepoint(mouse_pos) and click:
                state = "forest_ridge"
                click = False
        elif state == "outskirts":
            outskirts_story = [
                "The village outskirts are quiet, too quiet. The usual sounds of traders,",
                "children, and farmers have faded into an uneasy silence.",
                "",
                "You tread carefully along the dirt road, your eyes scanning every corner.",
                "Old wooden fences creak in the wind, and the distant fields lie abandoned.",
                "",
                "Then you see it—footprints in the mud. Small, clawed, and fresh.",
                "The Shadow Sprites have been here, far bolder than expected.",
                "",
                "A low growl echoes from behind a half-collapsed barn.",
                "Your grip tightens on the weapon in your hands, while your chosen gear",
                "hums with energy, ready to aid you.",
                "",
                "You have to act quickly. What will you do?"
            ]
            y_offset = 100
            for line in outskirts_story:
                drawText(line, 200, y_offset, white)
                y_offset += 40

            if drawButton("Investigate the barn", 500, 850, 400, 100, red, green).collidepoint(mouse_pos) and click:
                state = "outskirts_barn"
                click = False
            elif drawButton("Follow the footprints", 1100, 850, 400, 100, red, green).collidepoint(mouse_pos) and click:
                state = "outskirts_tracks"
                click = False

        elif state == "protect_village":
            protect_village_story = [
                "You walk through the quiet village, the Elder’s warning heavy on your mind.",
                "Shuttered windows, empty streets, the usual chatter replaced by uneasy silence.",
                "",
                "The villagers peek from behind curtains, some nodding at you timidly, others clutching their children.",
                "It’s clear: tonight, the village depends on your guidance, not just your strength.",
                "",
                "You pause at the square, considering your next move.",
                "There are those here who can help you prepare—an old trainer who once served the village militia,",
                "a scholar who knows the ways of traps and tactics, and the Elder himself, always ready with counsel.",
                "",
                "Which path will you take first to prepare the village for what may come?"
            ]

            y_offset = 100
            for line in protect_village_story:
                drawText(line, 200, y_offset, white)
                y_offset += 40


            if "Trainer" in availableChoices:
                if drawButton("Visit the shop – Buy equipment and gear", 200, 850, 800, 100, red, green).collidepoint(mouse_pos) and click:
                    state = "shop"
                    click = False
            if "Scholar" in availableChoices:
                if drawButton("Consult the scholar – Plan the strategy", 1100, 850, 800, 100, red, green).collidepoint(mouse_pos) and click:
                    state = "village_scholar"
                    click = False
        elif state == "shop":
            money = weaponsmith(inventory = inventory, money = money, storeitems = storeitems)
            drawText(f"money: {money}", 200, 100, white)


        pygame.display.update()

main()


