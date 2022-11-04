############################################################################################################
# NAME: Binairo: create
# AUTHOR: Christophe Van den Eynde
# FUNCTION: Create playable boards
############################################################################################################

# IMPORT PACKAGES ==========================================================================================
import pygame
pygame.init()
from General.Classes import Button, CenteredText, Submenu
from General.Functions import ActivateGameLoop, quitgame
from Binairo.Functions import board
from Settings.Default import Colors, Fonts
import os
import sys
import importlib
import ast
import time

import tracemalloc
# ==========================================================================================================

# GENERAL INFO =============================================================================================
# Initialize game ------------------------------------------------------------------------------------------

# Display size ---------------------------------------------------------------------------------------------
ScreenWidth = 800
ScreenHeight = 600

# Caption --------------------------------------------------------------------------------------------------
pygame.display.set_caption('Puzzle solver')

# Logo -----------------------------------------------------------------------------------------------------
Images = os.path.dirname(os.path.realpath(__file__)) + '\Images'
icon = pygame.image.load(Images + '\logo.png')
pygame.display.set_icon(icon)

# Clock ----------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
# ==========================================================================================================

# GAME LOOP: Binairo =======================================================================================
def Binairo_GameLoop(ScreenWidth, ScreenHeight, clock, Images):
# VARIABLES ------------------------------------------------------------------------------------------------
    running = True
    grid = None
    NumberOfCubes = 10
# INITITIALIZE SCREEN --------------------------------------------------------------------------------------
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.DOUBLEBUF|pygame.HWSURFACE, 32)
# MAIN LOOP ------------------------------------------------------------------------------------------------
    while running:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    key = '0'
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = '1'
                if event.key == pygame.K_DELETE or event.key == pygame.K_KP_PERIOD:
                    key = '.'
# MOUSE POSITION & CLICKS ----------------------------------------------------------------------------------
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
# SCREEN BACKGROUND ----------------------------------------------------------------------------------------
        Screen.fill(Colors["Background"])
# OPTIONS SUBMENU ------------------------------------------------------------------------------------------
        Title = Submenu(Screen, ScreenWidth - 165, ScreenHeight / 2 - 190, 145, 370, Colors["black"], Colors["Background"])
        Title.Outline()
        Title.Title("Binairo", Fonts["Button"], Colors["black"])
# OPTIONS BUTTONS ------------------------------------------------------------------------------------------
    # Number of cubes per row/ Board size ------------------------------------------------------------------
        # Dispay number
        pygame.draw.rect(Screen, Colors["Options"], (ScreenWidth - 160, ScreenHeight/2 - 170, 40, 40))
        Cubes = CenteredText(str(NumberOfCubes), Fonts["Button"], Colors["black"], int(ScreenWidth - 160 + 20), ScreenHeight/2 - 170 + 40/2)
        Cubes.render(Screen)
        # Increase number
        Increase = Button(Screen, ScreenWidth - 120, ScreenHeight/2 - 170, 20, 20, Colors["Options"], Colors["OptionsHighlight"])
        Increase.render(mouse)
        Increase.image(Images + '\ArrowUp.png')
        NrCubes = Increase.functionality(mouse, click, int(NumberOfCubes + 2))
        if NrCubes and NrCubes in range(2, 16, 2):
            pygame.time.delay(150)
            NumberOfCubes = NrCubes
        # Decrease number
        Decrease = Button(Screen, ScreenWidth - 120, ScreenHeight/2 - 150, 20, 20, Colors["Options"], Colors["OptionsHighlight"])
        Decrease.render(mouse)
        Decrease.image(Images + '\ArrowDown.png')
        NrCubes = Decrease.functionality(mouse, click, int(NumberOfCubes - 2))
        if NrCubes and NrCubes in range(2, 16, 2):
            pygame.time.delay(150)
            NumberOfCubes = NrCubes
    # Create new board -------------------------------------------------------------------------------------
        New = Button(Screen, ScreenWidth - 95, ScreenHeight/2 - 170, 70, 40, Colors["Options"], Colors["OptionsHighlight"])
        New.render(mouse)
        New.text(Fonts["Button"], Colors["black"], "New")
    # Reset board ------------------------------------------------------------------------------------------
        Reset = Button(Screen, ScreenWidth - 160, ScreenHeight/2 - 120, 135, 40, Colors["Options"], Colors["OptionsHighlight"])
        Reset.render(mouse)
        Reset.text(Fonts["Button"], Colors["black"], "Reset")
    # Get Hint ---------------------------------------------------------------------------------------------
        Hint = Button(Screen, ScreenWidth - 160, ScreenHeight/2 - 70, 135, 40, Colors["Options"], Colors["OptionsHighlight"])
        Hint.render(mouse)
        Hint.text(Fonts["Button"], Colors["black"], "Hint")
    # Check current (partial) board ------------------------------------------------------------------------
        Check = Button(Screen, ScreenWidth - 160, ScreenHeight/2 - 20, 135, 40, Colors["Options"], Colors["OptionsHighlight"])
        Check.render(mouse)
        Check.text(Fonts["Button"], Colors["black"], "Check")
# SOLVE BUTTONS ---------------------------------------------------------------------------------------
    # DFS button ------------------------------------------------------------------------------------------
        Dfs = Button(Screen, ScreenWidth - 160, ScreenHeight/2 + 30, 135, 40, Colors["Options"], Colors["OptionsHighlight"])
        Dfs.render(mouse)
        Dfs.text(Fonts["Button"], Colors["black"], "DFS")
    # BFS Button ------------------------------------------------------------------------------------------
        Heuristics = Button(Screen, ScreenWidth - 160, ScreenHeight/2 + 80, 135, 40, Colors["Options"], Colors["OptionsHighlight"])
        Heuristics.render(mouse)
        Heuristics.text(Fonts["Button"], Colors["black"], "Heuristics")

# NAVIGATION BUTTONS ---------------------------------------------------------------------------------------
    # Menu button ------------------------------------------------------------------------------------------
        Menu = Button(Screen, ScreenWidth - 160, ScreenHeight/2 + 130, 65, 40, Colors["Navigation"], Colors["NavigationHighlight"])
        Menu.render(mouse)
        Menu.text(Fonts["Button"], Colors["black"], "MENU")
        SelectedGame = Menu.functionality(mouse, click, ActivateGameLoop("Menu"))
        if SelectedGame: return SelectedGame
    # Exit Button ------------------------------------------------------------------------------------------
        Exit = Button(Screen, ScreenWidth - 90, ScreenHeight/2 + 130, 65, 40, Colors["Navigation"], Colors["NavigationHighlight"])
        Exit.render(mouse)
        Exit.text(Fonts["Button"], Colors["black"], "QUIT")
        SelectedGame = Exit.functionality(mouse, click, ActivateGameLoop("Quit"))
        if SelectedGame: return SelectedGame 


# BOARD ----------------------------------------------------------------------------------------------------
    # Create new Board -------------------------------------------------------------------------------------
        if not grid or New.functionality(mouse, click, True):
            # Display update
            pygame.display.update()
            # Initialize board
            grid = board(NumberOfCubes, (ScreenWidth, ScreenHeight))
            # Create empty board
            grid.CreateEmptyBoard()
            # BruteForce a solution
            grid.BruteForce()
            # Create a solvable boardstate for the solution
            grid.SolvableState()
            # Current board = solvable board
            grid.CurrentBoard()
            # Make the original values immutable
            grid.Immutable()
            # Print Background
            grid.CenterRectangle(ScreenWidth, ScreenHeight, 175, 0)
            # Slight delay (for smaller boards)
            pygame.time.delay(100)
    # Reset board ------------------------------------------------------------------------------------------
        elif Reset.functionality(mouse, click, True):
            grid.CurrentBoard() 
            grid.Immutable()
            # Slight delay (for smaller boards)
            pygame.time.delay(100)
    # Check Board ------------------------------------------------------------------------------------------
        elif Check.functionality(mouse, click, True):
            grid.Immutable()
            # Slight delay (for smaller boards)
            pygame.time.delay(100)
    # Get Hint ---------------------------------------------------------------------------------------------
        elif Hint.functionality(mouse, click, True):
            grid.Hint()
            grid.Immutable()
            # Slight delay
            pygame.time.delay(200)
        
        elif Dfs.functionality(mouse, click, True):
            start_time = time.time()
            tracemalloc.start()
            open('real_out.txt', 'w').close()
            grid.DFS_solve()
            # for i in range(len(step_array)):
                # grid.current = step_array[i]
                # time.sleep(1)
                # print(step_array[i])
                # grid.PrintBoard(Screen)
            file1 = open('real_out.txt', 'r')
            Lines = file1.readlines()
            count = 0
            for line in Lines:
               count = count + 1
               grid.current = ast.literal_eval(line)
               grid.BoardBackground(Colors["black"])
               grid.DrawCubes(Colors["Cube"], Colors["Correct"])
               grid.HiglightLines(Colors["Navigation"], mouse)
               grid.SelectCube(mouse, click)       
               grid.Pencil(key)
               grid.Updatecube(key)
               grid.PrintBoard(Screen)
               grid.CheckBoard(Screen, Fonts["Message"], Colors["Message"])
               pygame.display.update()
            #    time.sleep(0.1)
            print("Step: ", count, " steps.")
            print("Time:   ", time.time() - start_time, " seconds.")
            print("Memory: ", tracemalloc.get_traced_memory()[1], " bytes.")
            tracemalloc.stop()

        
        elif Heuristics.functionality(mouse, click, True):
            tracemalloc.start()
            start_time = time.time()
            open('real_out.txt', 'w').close()
            grid.Heuristics_solve()
            file1 = open('real_out.txt', 'r')
            Lines = file1.readlines()
            count = 0
            for line in Lines:
               count = count + 1
               grid.current = ast.literal_eval(line)
               grid.BoardBackground(Colors["black"])
               grid.DrawCubes(Colors["Cube"], Colors["Correct"])
               grid.HiglightLines(Colors["Navigation"], mouse)
               grid.SelectCube(mouse, click)       
               grid.Pencil(key)
               grid.Updatecube(key)
               grid.PrintBoard(Screen)
               grid.CheckBoard(Screen, Fonts["Message"], Colors["Message"])
               pygame.display.update()
            #    time.sleep(0.1)
            print("Step: ", count, " steps.")
            print("Time:   ", time.time() - start_time, " seconds.")
            print("Memory: ", tracemalloc.get_traced_memory()[1], " bytes.")
            tracemalloc.stop()

                
    # Row/col higlighting ----------------------------------------------------------------------------------
        grid.BoardBackground(Colors["black"])
        grid.DrawCubes(Colors["Cube"], Colors["Correct"])
        grid.HiglightLines(Colors["Navigation"], mouse)
    # Allow board updates ----------------------------------------------------------------------------------
        grid.SelectCube(mouse, click)       
        grid.Pencil(key)
        grid.Updatecube(key)
    # Print values -----------------------------------------------------------------------------------------
        grid.PrintBoard(Screen)
        grid.CheckBoard(Screen, Fonts["Message"], Colors["Message"])
# UPDATE DISPLAY -------------------------------------------------------------------------------------------
        pygame.display.update()
        clock.tick(60)
# COMPLETELY CLOSE THE GAME WHEN SCREEN IS CLOSED ----------------------------------------------------------
    return ActivateGameLoop("Quit")
# ==========================================================================================================

if __name__ == "__main__":
    x = Binairo_GameLoop(ScreenWidth, ScreenHeight, clock, Images)