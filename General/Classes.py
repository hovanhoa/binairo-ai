############################################################################################################
# NAME: Menu
# AUTHOR: Christophe Van den Eynde
# FUNCTION: All scripts concerning the Menu of the pygame apllication
############################################################################################################

# PACKAGES =================================================================================================
import pygame
# ==========================================================================================================

# [CLASS] INTERACTIVE BUTTONS ==============================================================================
class Button():
# Initialisation -------------------------------------------------------------------------------------------
    def __init__(self, Screen, X, Y, Width, Height, NormalColor, HighlightColor, SelectedPuzzle = False):
        self.Screen = Screen
        self.X = int(X)
        self.Y = int(Y)
        self.Width = int(Width)
        self.Height = int(Height)
        self.NormalColor = NormalColor
        self.HighlightColor = HighlightColor
        self.Selected = SelectedPuzzle
# Rendering & Highlight-------------------------------------------------------------------------------------
    def render(self, mouse):
        if (self.X + self.Width > mouse[0] > self.X and self.Y + self.Height > mouse[1] > self.Y) or self.Selected:
            pygame.draw.rect(self.Screen, self.HighlightColor, (self.X, self.Y, self.Width, self.Height))
        else:
            pygame.draw.rect(self.Screen, self.NormalColor, (self.X, self.Y, self.Width, self.Height))
# Adding text to button  -----------------------------------------------------------------------------------
    def text(self, Font, Color, Text):
        self.text = CenteredText(Text, Font, Color, int(self.X + (self.Width / 2)), int(self.Y + (self.Height / 2)))
        self.text.render(self.Screen)
# Adding image to button -----------------------------------------------------------------------------------
    def image(self, Image):
        Image = pygame.image.load(Image)
        Image = pygame.transform.scale(Image, (self.Width, self.Height))
        ImageArea = Image.get_rect()
        ImageArea.center = (self.X + self.Width/2, self.Y + self.Height/2)
        self.Screen.blit(Image, ImageArea)
# Adding functionality to Button ---------------------------------------------------------------------------
    def functionality(self, mouse, click, function):
        if self.X + self.Width > mouse[0] > self.X and self.Y + self.Height > mouse[1] > self.Y and click[0] == 1:
            return function # OR return function
# ==========================================================================================================

# [CLASS] CENTERED TEXT ====================================================================================
class CenteredText():
# Initialisation -------------------------------------------------------------------------------------------
    def __init__(self, Text, Font, Color, X, Y):
        self.Text = Text
        self.Font = Font
        self.Color = Color
        self.Position = (int(X), int(Y))
# Rendering ------------------------------------------------------------------------------------------------
    def render(self, Screen):
        TextSurface = self.Font.render(self.Text, True, self.Color)
        TextArea = TextSurface.get_rect()
        TextArea.center  = self.Position
        Screen.blit(TextSurface, TextArea)
# ==========================================================================================================

# [CLASS] CENTERED TEXT ====================================================================================
class MultiLineText():
# Initialisation -------------------------------------------------------------------------------------------
    def __init__(self, Text, Font, Color, Position, MaxWidth):
        self.Text = Text
        self.Font = Font
        self.Color = Color
        self.Position = Position
        self.MaxWidth = int(MaxWidth)
# Rendering ------------------------------------------------------------------------------------------------
    def render(self, Screen):
        X = int(self.Position[0])
        Y = int(self.Position[1])
        space = self.Font.size(' ')[0]  # The width of a space.

        for Sentence in self.Text.splitlines():
            for Word in Sentence.split(' '):
                WordSurface = self.Font.render(Word, True, self.Color)
                WordWidth, WordHeight = WordSurface.get_size()
                if X + WordWidth >= self.MaxWidth:
                    X = self.Position[0]            # reset X
                    Y += WordHeight                 # jump to next line
                Screen.blit(WordSurface, (X, Y))
                X += WordWidth + space
            X = self.Position[0]
            Y += WordHeight
# ==========================================================================================================

# [CLASS] SUBMENU ==========================================================================================
class Submenu():
# Initialisation -------------------------------------------------------------------------------------------
    def __init__(self, Screen, X, Y, Width, Height, EdgeColor, InnerColor):
        self.Screen = Screen
        self.X = int(X)
        self.Y = int(Y)
        self.Width = int(Width)
        self.Height = int(Height)
        self.EdgeColor = EdgeColor
        self.InnerColor = InnerColor
# Submenu outline ------------------------------------------------------------------------------------------
    def Outline(self):
        # Submenu - outline
        pygame.draw.rect(self.Screen, self.EdgeColor, (self.X - 2, self.Y - 2, self.Width + 4, self.Height + 4))
        # Submenu - color
        pygame.draw.rect(self.Screen, self.InnerColor, (self.X, self.Y, self.Width, self.Height))
# Submenu title --------------------------------------------------------------------------------------------
    def Title(self, Text, Font, Color):
        # Get text size
        TextSurface = Font.render(Text, True, Color)
        TextWidth, TextHeight = TextSurface.get_size()
        # Text outline & background
        #Text_X = (self.X + self.Width + 2) - (TextWidth)*1.5      
        pygame.draw.rect(self.Screen, self.EdgeColor, (self.X + self.Width/8 - 2, self.Y - TextHeight*1.5/2 - 2, self.Width/8*6 +4, TextHeight * 1.5 + 4))
        pygame.draw.rect(self.Screen, self.InnerColor, (self.X + self.Width/8, self.Y -TextHeight*1.5/2, self.Width/8*6, TextHeight * 1.5))
        # Text
        Text_X = (self.X + self.Width/2 +2 )
        Title = CenteredText(Text, Font, Color, Text_X, self.Y)
        Title.render(self.Screen)
# Submenu image --------------------------------------------------------------------------------------------
    def Image(self, Image):
        Image = pygame.image.load(Image)
        Image = pygame.transform.scale(Image, (115, 115))
        ImageArea = Image.get_rect()
        ImageArea.center = (self.X + self.Width/2, self.Y +80)
        self.Screen.blit(Image, ImageArea)
# Submenu text ---------------------------------------------------------------------------------------------
    def MultiLineText(self, Text, Font, Color):
        self.Text = MultiLineText(Text, Font, Color, (self.X + 10, int(self.Y + 80 + 150/ 2)), self.X + self.Width - 20)
        self.Text.render(self.Screen)
    
# ===========================================================================================================
