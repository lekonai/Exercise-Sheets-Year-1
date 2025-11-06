
-- import System.Random

import Data.Time.Clock

randomIO :: IO Int
randomIO = do
  t <- getCurrentTime
  (return . floor . (*1000) . toRational . utctDayTime) t



------------------------- Exercise 1


main :: IO ()
main = undefined

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

  let xsUpdate2 = removal xsUpdate (toInteger botMove)
  -- these types confusing as hell man :sob:

  if not (null xs)
    then
      return xs
      -- input xsUpdate
  else
    return []

botMove :: Foldable t => t Integer -> IO (IO Integer)
botMove xs = do
  num <- produceBotAct
  if elem num xs
    then
      return produceBotAct
  else
    botMove xs

produceBotAct :: IO Integer
produceBotAct = do
  num <- randomIO
  return (mod (toInteger num) 9)
