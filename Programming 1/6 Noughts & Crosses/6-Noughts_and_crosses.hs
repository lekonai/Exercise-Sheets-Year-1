
-- import System.Random

import Data.List
import Data.Time.Clock

randomIO :: IO Int
randomIO = do
  t <- getCurrentTime
  (return . floor . (*1000) . toRational . utctDayTime) t


------------------------- Exercise 1

type Board = [Int] 

winCheck :: Board -> Int
winCheck bd
  | horizontalCheck bd /= 0 = horizontalCheck bd
  | verticalCheck bd /= 0   = verticalCheck bd
  | diagonalCheck bd /= 0   = diagonalCheck bd
  | otherwise               = 0

-- there's surely a more intuitive way of going about this
horizontalCheck :: Board -> Int
horizontalCheck [] = 0
horizontalCheck bd 
  | head bd == head (tail bd) && head bd == head (tail (tail bd)) && head bd /= 0   = head bd
  | otherwise                                                                       = horizontalCheck (tail (tail (tail bd)))

verticalCheck :: Board -> Int
verticalCheck bd
  | bd !! 0 == bd !! 3 && bd !! 0 == bd !! 6 && bd !! 0 /= 0  = bd !! 0
  | bd !! 1 == bd !! 4 && bd !! 1 == bd !! 7 && bd !! 1 /= 0  = bd !! 1
  | bd !! 2 == bd !! 5 && bd !! 2 == bd !! 8 && bd !! 2 /= 0  = bd !! 2
  | otherwise                                                 = 0

diagonalCheck :: Board -> Int
diagonalCheck bd
  | bd !! 0 == bd !! 4 && bd !! 0 == bd !! 8 && bd !! 0 /= 0  = bd !! 0
  | bd !! 2 == bd !! 4 && bd !! 2 == bd !! 6 && bd !! 2 /= 0  = bd !! 2
  | otherwise                                                 = 0


displayBoard (b:bd) = do
  if b /= 0
    then
      if b == 1
        then
          putStr "X"
      else
        putStr "O"
  else
    putStr " "
  
  if ((mod (length bd) 3) == 0 && length bd /= 0)
    then
      putStrLn "\n-----"
  else
    if length bd /= 0
      then
        putStr "|"
    else
      putStrLn ""
    
  if not (null bd)
    then
      displayBoard bd
  else
    putStr ""

main :: IO ()
main = do
  putStrLn "The indexing works from left to right"
  putStrLn "Would you like to play with a bot? y/n"
  x <- getLine
  if x == "y"
    then
      mainLoop [1,2,3,4,5,6,7,8,9] True [0,0,0,0,0,0,0,0,0]
  else
    mainLoopBot [1,2,3,4,5,6,7,8,9] [0,0,0,0,0,0,0,0,0] 

  

mainLoop :: [Int] -> Bool -> Board -> IO ()
mainLoop xs n bd = do
  displayBoard bd
  if n == True
    then
      putStrLn "Player X Turn"
  else
    putStrLn "Player O Turn"
  
  xsUpdate <- input xs

  let newBd = boardUpdate (head (xs \\ xsUpdate)) n bd
  if winCheck newBd /= 0 
    then
      if winCheck newBd == 1
        then
          finalDialogue newBd (winCheck newBd)
      else
        finalDialogue newBd (winCheck newBd)
  else
    if null xsUpdate
      then 
        finalDialogue newBd 0
    else 
      mainLoop xsUpdate (not n) newBd

mainLoopBot = undefined

-- mainLoopBot :: [Int] -> Bool -> Board -> IO ()
-- mainLoopBot xs bd = do
--   displayBoard bd
--   xsUpdate <- input xs
--   let newBd = boardUpdate (head (xs \\ xsUpdate)) n bd
--   if winCheck newBd /= 0 
--     then
--       if winCheck newBd == 1
--         then
--           finalDialogue newBd (winCheck newBd)
--       else
--         finalDialogue newBd (winCheck newBd)
--   else
--     if null xsUpdate
--       then 
--         finalDialogue newBd 0
--     else
--       do
--         xsUpdateAgain <- xsUpdate (removal (botMove xsUpdate))
--         let secondBd = boardUpdate (head (xsUpdate \\ xsUpdateAgain) False newBd)
        
--         if winCheck secondBd /= 0 
--           then
--             if winCheck secondBd == 1
--               then
--                 finalDialogue secondBd (winCheck secondBd)
--             else
--               finalDialogue secondBd (winCheck secondBd)
--         else
--           if null xsUpdate
--             then 
--               finalDialogue secondBd 0
--           else 
--             mainLoopBot xsUpdate secondBd



  
finalDialogue :: Board -> Int -> IO ()
finalDialogue bd n = do
  displayBoard bd
  if n /= 0
    then
      if n == 1
        then
          putStrLn "Player X Won!"
      else
        putStrLn "Player O Won!"
  else
    putStrLn "Game Over! No One Wins!"

boardUpdate :: Int -> Bool -> Board -> Board
boardUpdate x p bd = updater x p bd 1
  where
    updater :: Int -> Bool -> Board -> Int -> Board
    updater x p [] c = []
    updater x p (b:bd) c 
      | (x == c) && p == True   = 1 : updater x p bd (c + 1)
      | (x == c) && p == False  = 2 : updater x p bd (c + 1)
      | otherwise               = b : updater x p bd (c + 1)

removal :: [Int] -> Int -> [Int]
removal [] y = []
removal (x:xs) y
  | x == y      = removal xs y
  | otherwise   = x : removal xs y

input :: [Int] -> IO [Int]
input xs = do
  putStrLn "You have these options: "
  print xs
  num <- getLine
  let xsUpdate = removal xs (read num :: Int)
  if not (null xs)
    then
      return xsUpdate
  else
    return []

botMove xs = do
  num <- produceBotAct
  if num `elem` xs
    then
      return num
  else
    botMove xs

produceBotAct :: IO Integer
produceBotAct = do
  num <- randomIO
  return (mod (toInteger num) 9)
