import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur, hauteur = 800, 600
taille_case = 20
vitesse = 12

# Couleurs
couleur_fond = (0, 0, 0)
couleur_serpent = (0, 255, 0)
couleur_pomme = (255, 0, 0)
couleur_texte = (255, 255, 255)

# Définition des directions
HAUT = (0, -1)
BAS = (0, 1)
GAUCHE = (-1, 0)
DROITE = (1, 0)

# Classe représentant le serpent
class Serpent:
    def __init__(self):
        self.longueur = 1
        self.corps = [(largeur // 2, hauteur // 2)]
        self.direction = DROITE

    def deplacer(self):
        tete = (self.corps[0][0] + self.direction[0] * taille_case,
                self.corps[0][1] + self.direction[1] * taille_case)

        # Correction pour réapparaître de l'autre côté
        tete = (tete[0] % largeur, tete[1] % hauteur)

        self.corps.insert(0, tete)
        if len(self.corps) > self.longueur:
            self.corps.pop()

    def manger_pomme(self):
        self.longueur += 1

    def verifier_collision(self):
        if self.corps[0] in self.corps[1:]:
            raise CollisionException("Le serpent s'est mangé lui-même!")

# Classe représentant la pomme
class Pomme:
    def __init__(self):
        self.position = self.generer_position()

    def generer_position(self):
        x = random.randint(0, (largeur - taille_case) // taille_case) * taille_case
        y = random.randint(0, (hauteur - taille_case) // taille_case) * taille_case
        return x, y

    def deplacer(self):
        self.position = self.generer_position()

# Exception pour gérer les collisions
class CollisionException(Exception):
    pass

# Fonction pour dessiner les yeux du serpent
def dessiner_yeux(surface, position_tete):
    oeil_radius = 4
    ecart_yeux = 5
    ecart_pupille = 2

    oeil_gauche = (position_tete[0] + ecart_yeux, position_tete[1] + ecart_yeux)
    oeil_droit = (position_tete[0] + taille_case - ecart_yeux - 2 * oeil_radius, position_tete[1] + ecart_yeux)

    pupille_radius = oeil_radius - ecart_pupille

    pygame.draw.circle(surface, couleur_texte, oeil_gauche, oeil_radius)
    pygame.draw.circle(surface, couleur_texte, oeil_droit, oeil_radius)

    # Vous pouvez également dessiner une pupille noire au centre de l'œil
    pygame.draw.circle(surface, couleur_fond, (oeil_gauche[0] + ecart_pupille, oeil_gauche[1]), pupille_radius)
    pygame.draw.circle(surface, couleur_fond, (oeil_droit[0] + ecart_pupille, oeil_droit[1]), pupille_radius)

# Initialisation de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake Game")

# Initialisation du serpent et de la pomme
serpent = Serpent()
pomme = Pomme()

# Initialisation du jeu
score = 0
font = pygame.font.Font(None, 36)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and serpent.direction != BAS:
                serpent.direction = HAUT
            elif event.key == pygame.K_DOWN and serpent.direction != HAUT:
                serpent.direction = BAS
            elif event.key == pygame.K_LEFT and serpent.direction != DROITE:
                serpent.direction = GAUCHE
            elif event.key == pygame.K_RIGHT and serpent.direction != GAUCHE:
                serpent.direction = DROITE

    # Déplacement du serpent
    serpent.deplacer()

    # Vérification des collisions
    try:
        serpent.verifier_collision()
    except CollisionException as e:
        print(e)
        # Gérer la fin du jeu ici (rejouer ou quitter)

        # Afficher l'écran de fin de jeu
        fenetre.fill(couleur_fond)

        # Afficher le message "Game Over"
        font_game_over = pygame.font.Font(None, 72)
        message_game_over = font_game_over.render("Game Over", True, couleur_texte)
        rect_game_over = message_game_over.get_rect(center=(largeur // 2, hauteur // 2 - 50))
        fenetre.blit(message_game_over, rect_game_over)

        # Afficher le score final
        font_score_final = pygame.font.Font(None, 36)
        message_score_final = font_score_final.render(f"Score final: {score}", True, couleur_texte)
        rect_score_final = message_score_final.get_rect(center=(largeur // 2, hauteur // 2 + 50))
        fenetre.blit(message_score_final, rect_score_final)

        pygame.display.flip()

        # Attendre quelques secondes avant de quitter
        pygame.time.delay(3000)

        # Réinitialiser le jeu
        serpent = Serpent()
        pomme = Pomme()
        score = 0

    # Vérification de la capture de la pomme
    if serpent.corps[0] == pomme.position:
        serpent.manger_pomme()
        pomme.deplacer()
        score += 1  # Augmenter le score du joueur

    # Affichage
    fenetre.fill(couleur_fond)

    # Dessiner le serpent avec des rectangles
    for i, pos in enumerate(serpent.corps):
        pygame.draw.rect(fenetre, couleur_serpent, (pos[0], pos[1], taille_case, taille_case))

        # Dessiner les yeux uniquement à la tête du serpent
        if i == 0:
            dessiner_yeux(fenetre, pos)

    # Dessiner la pomme avec un rectangle
    pygame.draw.rect(fenetre, couleur_pomme, (pomme.position[0], pomme.position[1], taille_case, taille_case))

    # Afficher le score
    texte_score = font.render(f"Score: {score}", True, couleur_texte)
    fenetre.blit(texte_score, (10, 10))

    pygame.display.flip()

    # Limiter la vitesse du jeu
    pygame.time.Clock().tick(vitesse)
