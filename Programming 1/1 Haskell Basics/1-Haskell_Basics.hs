import Distribution.SPDX (LicenseId(ZPL_1_1))
import System.Win32 (xBUTTON1)
import Language.Haskell.TH.PprLib (float, integer)

------------------------- Exercise 1

square :: Int -> Int
square x = x * x

pythagoras :: Int -> Int -> Int -> Bool
pythagoras a b c 
    | square c /= square a + square b = False 
    | otherwise = True 

------------------------- Exercise 2

factorial :: Int -> Int
factorial x
    | x <= 1    = 1
    | otherwise = x * factorial (x - 1)

power :: Int -> Int -> Int
power x y 
    | y == 0     = 1
    | y < 0      = -99999999 -- so i need a real exception here i reckon
    | otherwise  = x * power x (y - 1)

--note: you will need to create your own cases,
--      replacing the equals (=) sign with guards

euclid :: Int -> Int -> Int
-- euclid x y
--     | x == y = x
--     | mod (max x y) (min x y) /= 0  = euclid (min x y) (mod (max x y) (min x y))
--     | otherwise = min x y 

-- top solution doesn't follow what it asks for but the bottom one does
euclid x y
    | x == y = x
    | otherwise = euclid (min x y) (max x y - min x y)

------------------------- Exercise 3

pow :: Int -> Int -> Int
pow x y = if y == 0 then 1 else x * pow x (y - 1)

------------------------- Exercise 4

collatz :: Int -> Int
collatz x 
    | x == 1    = 1
    | even x    = collatz (div x 2) -- ??
    | odd x     = collatz (3 * x) + 1


collatzCount :: Int -> Int -> Int
collatzCount x y
    | x == 1    = y
    | even x    = collatzCount (div x 2) (y + 1)
    | odd x     = collatzCount ((3 * x) + 1) (y + 1)

collatzMax :: Int -> (Int,Int) -> (Int,Int)
collatzMax x (y, z)
    | x == 1                        = (y, z)
    | collatzCount (x - 1) 0 > z    = collatzMax (x - 1) (x - 1, collatzCount (x - 1) 0)
    | otherwise                     = collatzMax (x - 1) (y, z)


------------------------- Exercise 5

ackermann :: Int -> Int -> Int
ackermann m n
    | m == 0 && n > 0 = n + 1
    | m > 0 && n == 0 = ackermann (m - 1) 1
    | m > 0 && n > 0 = ackermann (m - 1) (ackermann m (n - 1))
    -- not going to lie i just kind of give up with this