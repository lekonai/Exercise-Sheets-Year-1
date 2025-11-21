

------------------------- Exercise 1

allTrue :: [Bool] -> Bool
allTrue = foldr (&&) True

someTrue :: [Bool] -> Bool
someTrue = foldr (||) False

largest :: Ord a => [a] -> a
largest = foldr1 max

smallest :: Ord a => [a] -> a
smallest = foldr1 min

every :: (a -> Bool) -> [a] -> Bool
every p = foldr ( ( && ) . p ) True

some :: (a -> Bool) -> [a] -> Bool
some p = foldr ( ( || ) . p ) False

select :: (a -> Bool) -> [a] -> [a]
select f = foldr (g f) []
    where
        g f x ys
            | f x       = x : ys
            | otherwise = ys


member :: Eq a => a -> [a] -> Bool
member y = foldr ( ( || ) . (== y) ) False

find :: Eq a => a -> [(a,b)] -> Maybe b
find x = foldr (\(y, r) a -> if (x == y) then Just r else a) Nothing

------------------------- Exercise 2


evenLength :: [a] -> Bool
evenLength = foldr (\_ -> not) True

count :: (a -> Bool) -> [a] -> Int
count p = foldr (\x -> if p x then (+1) else id) 0

successive :: Char -> String -> Int
successive c = snd . foldr f (0,0)
    where
        f d (i, j) 
            | d == c        = (i + 1, max (i + 1) j)
            | otherwise     = (0, j)


------------------------- Exercise 3

{-

Category 1 (foldl "just works"):

Category 2 (a "flip" is needed, but same result):

Category 3 (different result even with "flip"):

-}

------------------------- Exercise 4

------------------------- Exercise 5



