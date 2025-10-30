import System.Win32 (COORD(yPos), xBUTTON1, fILE_FLAG_SEQUENTIAL_SCAN)
import Data.Char (intToDigit)
import GHC.Base (VecElem(Int16ElemRep))
import Text.Printf (errorBadArgument)
import Distribution.Simple.Setup (trueArg, falseArg)
import Main (msort)
import Distribution.Compat.Prelude (Integral(div))
import Data.ByteString (length)
------------------------- Exercise 1

add :: [Int] -> Int
add []     = 0
add (x:xs) = x + add xs

times :: Num a => [a] -> a
times [] = 1
times (x:xs) = x * times xs

range :: Int -> Int -> [Int]
-- range _ _ = []
range n m
    | n + 1 == m    = [n, m]
    | otherwise     = n : range ( n + 1 ) m

factorial :: Int -> Int
factorial 0 = 1
factorial x = times (range 1 x)


------------------------- Exercise 2

count :: [a] -> Int
count []     = 0
count (_:xs) = 1 + count xs

append :: [a] -> [a] -> [a]
append [] y = y
-- append [x] ys = x : ys
append (x:xs) y = x : append xs y

concatenate :: [[a]] -> [a]
concatenate [] = []
concatenate (x:xs) = append x (concatenate xs)

------------------------- Exercise 3

member :: Eq a => a -> [a] -> Bool
member x (y:ys)
    | x == y = True
    | null ys = False
    | otherwise = member x ys

member2 :: Int -> [Int] -> Bool
member2 x [] = False
member2 x (y:ys) = if (x == y) && (ys /= []) then True else member x ys

remove :: Int -> [Int] -> [Int]
remove x (y:ys)
    | null ys = y:ys
    | x == y = remove x ys
    | otherwise = y : remove x ys

at :: [a] -> Int -> a
-- this acts like (!!) apparently, i've never seen that function before
at [] i = error "no list."
at xs i
    | i < 0 || length (xs) < (i - 1) = error "index is negative / too large" -- for some reason this doesn't work, well.
    | i == 0 = head xs
    | otherwise = at (tail xs) (i - 1)

------------------------- Exercise 4

final :: [a] -> a
final [] = error "no list, what ?? why!! put a list bro"
final [x] = x
final (x:xs) = final (xs)

ordered :: Ord a => [a] -> Bool
ordered [] = error "no list bro put a list in"
ordered [x] = True
ordered (x:y:zs)
    | x < y = ordered (y:zs) -- strict increasing
    | x > y = False
    | null zs = True
    | otherwise = False


pair :: [a] -> [b] -> [(a,b)]
pair [] y = []
pair x [] = []
pair (x:xs) (y:ys) = (x,y) : pair xs ys

find :: Eq a => a -> [(a,String)] -> String
find _ [] = ""
find k ((x,y) : xs)
    | k == x = y
    | null xs = ""
    | otherwise = find k xs

------------------------- Exercise 5

-- done

------------------------- Exercise 6

merge :: [Int] -> [Int] -> [Int]
merge [] [] = []
merge [] y = y
merge x [] = x
merge (x:xs) (y:ys)
    | x > y = y : merge (x:xs) ys
    | y > x = x : merge xs (y:ys)
    | otherwise = x : y : merge xs ys
    
msort :: [Int] -> [Int]
msort [] = []
msort [x] = [x]
msort xs = merge (msort (take n xs)) (msort (drop n xs))
    where
        n = div (length xs 2)

------------------------- Exercise 7

type Hanoi = ([Int],[Int],[Int])

hanoi :: Int -> [Hanoi]
hanoi = undefined