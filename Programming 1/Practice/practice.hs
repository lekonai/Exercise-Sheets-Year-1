-- pack :: [Char] -> [String]
-- pack x = packer x []
--     where
--         packer :: [Char] -> [String] -> [String]
--         packer (x:xs) []        = packer xs [x]
--         packer [] n             = n
--         packer (x:xs) n
--             | x == ((n !! 0) !! 0)  = packer xs ((last n) ++ [x])
--             | otherwise             = packer xs (n : [x])

-- yeah :: [(Float, Float)] -> (Float, Float)
-- yeah x = (((sum (map fst x)) / fromIntegral (length x)), ((sum (map fst x)) / fromIntegral (length x)))

data Tree a = Leaf | Node a (Tree a) (Tree a)
    deriving (Show)
upToSix :: Int -> (Bool,Int,Int)
upToSix n
    | 6 < n = (False,0,0)
    | otherwise = (True, 2*n , 2*n + 1)
grow f r
    | b = Node r (grow f x) (grow f y)
    | otherwise = Leaf
    where
        (b,x,y) = f r

flatten :: Tree a -> [a]
-- flatten (Node n l r)
--     | (l /= Leaf) && (r /= Leaf) = [n] ++ flatten l ++ flatten r
--     | (l /= Leaf) && (r == Leaf) = [n] ++ flatten l
--     | (l == Leaf) && (r /= Leaf) = [n] ++ flatten r
--     | otherwise                  = [n]

flatten (Node n Leaf Leaf)  = [n]
flatten (Node n l Leaf)     = [n] ++ flatten l
flatten (Node n Leaf r)     = [n] ++ flatten r
flatten (Node n l r)        = [n] ++ flatten l ++ flatten r

-- t :: Tree a
t = Node 4 (Node 2 (Node 1 Leaf Leaf) (Node 3 Leaf Leaf)) (Node 5 Leaf (Node 6 Leaf Leaf))

inOrder :: Tree a -> [a]
inOrder Leaf = []
inOrder (Node n l r) = inOrder l ++ [n] ++ inOrder r

preOrder :: Tree a -> [a]
preOrder Leaf = []
preOrder (Node n l r) = [n] ++ preOrder l ++ preOrder r

postOrder :: Tree a -> [a]
postOrder Leaf = []
postOrder (Node n l r) = postOrder l ++ postOrder r ++ [n]