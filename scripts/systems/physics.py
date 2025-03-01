import pygame
from scripts import settings

class Physics:
    
    
    def check_collision(self, obj1, obj2):
        """Check for collision between two objects."""
        rect1 = pygame.Rect(obj1.pos_x, obj1.pos_y, obj1.width, obj1.height)
        rect2 = pygame.Rect(obj2.pos_x, obj2.pos_y, obj2.width, obj2.height)
        
        # Area for hover 
        return rect1.colliderect(rect2) 
    
    # Player collisions 
    def check_collision_player_item(self, player, obj2):
        rect1 = pygame.Rect(player.pos_x, player.pos_y, player.image.get_width(), player.image.get_height())
        rect2 = pygame.Rect(obj2.pos_x, obj2.pos_y, obj2.image.get_width(), obj2.image.get_height())
        
        # Area for hover 
        return rect1.colliderect(rect2) 
    
    def player_collisions_with_structures(self,player):
        """Check and resolve collisions with walls."""
        player_half_width = player.player_rect.width // 2
        player_half_height = player.player_rect.height // 2

        # Future positions
        next_x = player.pos_x + player.movement[0] * player.move_speed
        next_y = player.pos_y + player.movement[1] * player.move_speed

        # Create future rects for X and Y movement
        future_rect_x = pygame.Rect(
            next_x - player_half_width, player.pos_y - player_half_height,
            player.player_rect.width, player.player_rect.height
        )
        future_rect_y = pygame.Rect(
            player.pos_x - player_half_width, next_y - player_half_height,
            player.player_rect.width, player.player_rect.height
        )

        # Check for collisions with walls
        self.check_collision_with_structures(player,future_rect_x, "x")
        self.check_collision_with_structures(player,future_rect_y, "y")

    # Auxiliary functions (collision calculations)
    def check_collision_with_structures(self,player, future_rect, axis):
        """Check for collisions with walls on a specific axis."""
        for x in range(player.game.world.grid_length_x):
            for y in range(player.game.world.grid_length_y):
                if player.game.world.world[x][y]["structure"] == "wall":
                    wall_rect = pygame.Rect(
                        x * settings.TILE_SIZE, y * settings.TILE_SIZE,
                        settings.TILE_SIZE, settings.TILE_SIZE
                    )
                    if future_rect.colliderect(wall_rect):
                        self.resolve_collision_with_structures(player,axis, wall_rect)
    def resolve_collision_with_structures(self,player, axis, wall_rect):
        """Resolve collision on a specific axis."""
        if axis == "x":
            if player.movement[0] > 0:  # Moving right
                player.pos_x = wall_rect.left - player.player_rect.width // 2
            elif player.movement[0] < 0:  # Moving left
                player.pos_x = wall_rect.right + player.player_rect.width // 2
            player.movement[0] = 0
        elif axis == "y":
            if player.movement[1] > 0:  # Moving down
                player.pos_y = wall_rect.top - player.player_rect.height // 2
            elif player.movement[1] < 0:  # Moving up
                player.pos_y = wall_rect.bottom + player.player_rect.height // 2
            player.movement[1] = 0