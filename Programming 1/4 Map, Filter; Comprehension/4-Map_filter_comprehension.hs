import Distribution.Simple (unifiedIPIDRequired)

------------------------- Exercise 1

-- a

doubles :: [Int] -> [Int] -- map
doubles = map (*2)

doubles2 xs = [x * 2 | x <- xs] -- list comp

doubles3 (x:xs) = x * 2 : doubles xs -- recursion

-- b

multiplesOfThree :: [Int] -> [Int]
multiplesOfThree [] = []
multiplesOfThree (x:xs) -- recursion
    | mod x 3 == 0  = x : multiplesOfThree xs
    | otherwise     = multiplesOfThree xs

multiplesOfThree2 :: [Int] -> [Int]
multiplesOfThree2 xs = [x | x <- xs, mod x 3 == 0] -- list comp

multiplesOfThree3 :: [Int] -> [Int]
multiplesOfThree3 = filter divisibleThree -- filter/map.
    where
        divisibleThree x -- an actual auxiliary! wow
            | mod x 3 == 0 = True
            | otherwise = False

-- c

-- map and filter:
doubleMultiplesOfThree :: [Int] -> [Int]
doubleMultiplesOfThree = doubles . multiplesOfThree

-- list comprehension
doublesMultiplesOfThree2 :: [Int] -> [Int]
doublesMultiplesOfThree2 xs = [x * 2 | x <- xs, mod x 3 == 0]

-- recursion
doublesMultiplesOfThree3 :: [Int] -> [Int]
doublesMultiplesOfThree3 [] = []
doublesMultiplesOfThree3 (x:xs)
    | divisibleThree x = x * 2 : doublesMultiplesOfThree3 xs
    | otherwise = doublesMultiplesOfThree3 xs
    where
        divisibleThree x
            | mod x 3 == 0  = True
            | otherwise     = False


------------------------- Exercise 2

-- b

-- filter
shorts :: [String] -> [String]
shorts = filter tooLong
    where
        tooLong x
            | length x >= 4 = False
            | otherwise = True

-- list comprehension
shorts2 :: [String] -> [String]
shorts2 xs = [ x | x <- xs, length x < 4]

-- c

-- map and filter
incrementPositives :: [Int] -> [Int]
incrementPositives = map (+ 1) . filter (> 0)

-- map and filter with aux
incrementPositives2 :: [Int] -> [Int]
incrementPositives2 = map increment . filter positive
    where
        increment x = x + 1
        positive x
            | x > 0     = True
            | otherwise = False

-- list comprehension
incrementPositives3 :: [Int] -> [Int]
incrementPositives3 xs = [x + 1 | x <- xs, x > 0]

-- d

-- omar styled
difference :: String -> String -> String
difference [] ys = []
difference xs ys
    | isIn ys (head xs)   = difference (tail xs) ys
    | otherwise                   = head xs : difference (tail xs) ys
        where
            isIn :: String -> Char -> Bool
            isIn [] x = False
            isIn ys x
                | head ys == x            = True
                | otherwise                 = isIn (tail ys) x

-- list comprehension
difference2 :: String -> String -> String
difference2 xs ys = [ x | x <- xs, x `notElem` ys]

-- e

-- standard
oddLengthSums :: [[Int]] -> [Int]
oddLengthSums [] = []
oddLengthSums (x:xs)
    | correctLengthAndOdd x     = sum x : oddLengthSums xs
    | otherwise                 = oddLengthSums xs
        where
            correctLengthAndOdd x
                | odd (length x)        = True
                | otherwise             = False

-- list comprehension
oddLengthSums2 :: [[Int]] -> [Int]
oddLengthSums2 xs = [ sum x | x <- xs, odd (length x) ]

------------------------- Exercise 3

-- a

numbered :: [a] -> [(Int,a)]
numbered = zip [1..]

-- b

-- normal style
everyother :: [a] -> [a]
everyother xs = map snd (filtrationSystem (numbered xs))
    where
        filtrationSystem = filter theFilter
            where
                theFilter x
                    | odd (fst x)   = True
                    | otherwise     = False

-- list comprehension
everyother2 :: [a] -> [a]
everyother2 xs = [snd x | x <- numbered xs, odd (fst x)]

-- c

-- normal style
same :: Eq a => [a] -> [a] -> [Int]
same xs ys = sameAux (numbered (zip xs ys))
    where
        sameAux [] = []
        sameAux (x:xs)
            | uncurry (==) (snd x)      = fst x : sameAux xs
            | otherwise                 = sameAux xs

-- list comprehension

same2 xs ys = [ fst x | x <- numbered (zip xs ys), uncurry (==) (snd x)]


------------------------- Exercise 5

combinations :: [a] -> [b] -> [(a,b)]
combinations xs ys = [ (x , y) | x <- xs, y <- ys ]

-- selfcombinations :: [a] -> [(a,a)]
-- selfcombinations xs = [ (x, y) | x <- xs, y <- tail xs]

pyts :: Int -> [(Int,Int,Int)]
pyts n = [ (a, b, c) | a <- [1..n], b <- [1..n], c <- [1..n], (c^2) == (a^2) + (b^2) ]

-- unique :: [(Int, Int, Int)] -> [(Int, Int, Int)] -> [(Int, Int, Int)]
-- unique xs ((x, y, z):allem)
--     -- | uncurry xs == (x, y, z) = xs : unique xs allem
--     | xs `elem` x || xs `elem` y || xs `elem` z = xs : unique xs allem
--     | otherwise                                 = xs : (x, y, z) : unique xs allem



------------------------- Exercise 6

choice :: [[a]] -> [[a]]
choice [] = [[]]
-- choice (xs:ys:zs) = [ x:y:z | x <- xs, y <- ys, z <- zs]
choice (xs: xss) = [ x : y | x <- xs, y <- choice xss]


-- choice2 :: [[a]] -> [[a]]
-- choice2 (xs:ys) = [ (x, y) | x <- xs, y <- ys]
-- so for some reason the last part of the list just doesnt.. do the same thing?? this is weird

splits :: [a] -> [([a],[a])]
splits xs = [ splitAt n xs | n <- [0..length xs] ]

permutations :: [a] -> [[a]]
permutations [] = [[]]
permutations (x:xs) = [ as ++ [x] ++ bs | ys <- permutations xs , (as, bs) <- splits ys]