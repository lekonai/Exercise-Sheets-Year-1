
data IntTree = Empty | Node Int IntTree IntTree
  -- deriving Show

t :: IntTree
t = Node 4 (Node 2 (Node 1 Empty Empty) (Node 3 Empty Empty)) (Node 5 Empty (Node 6 Empty Empty))


------------------------- Exercise 1

isEmpty :: IntTree -> Bool
isEmpty Empty = True
isEmpty _     = False

rootValue :: IntTree -> Int
rootValue Empty        = 0
rootValue (Node i _ _) = i

height :: IntTree -> Int
height Empty = 0
height (Node i l r) = 1 + max (height l) (height r)

member :: Int -> IntTree -> Bool
member n Empty = False
member n (Node i l r)
  | i == n = True
  | otherwise = (member n l) || (member n r)

-------------------------

instance Show IntTree where
    show = unlines . aux ' ' ' '
      where
        aux _ _ Empty = []
        aux c d (Node x s t) = 
          [ c:' ':m | m <- aux ' ' '|' s ] ++ 
          ['+':'-':show x] ++ 
          [ d:' ':n | n <- aux '|' ' ' t ]



insert :: Int -> IntTree -> IntTree
insert x Empty = Node x Empty Empty
insert x (Node y left right)
    | x == y    = Node y left right
    | x <  y    = Node y (insert x left) right
    | otherwise = Node y left (insert x right)

build :: [Int] -> IntTree
build = foldr insert Empty

flatten :: IntTree -> [Int]
flatten Empty        = []
flatten (Node x l r) = flatten l ++ [x] ++ flatten r

treemap :: (Int -> Int) -> IntTree -> IntTree
treemap f Empty        = Empty
treemap f (Node x l r) = Node (f x) (treemap f l) (treemap f r)

------------------------- Exercise 2

present :: Int -> IntTree -> Bool
present n Empty = False
present n (Node i l r)
  | i == n = True
  | n > i = present n r
  | n < i = present n l
  | otherwise = False


smallest :: IntTree -> Int
smallest Empty            = error "The tree is empty"
smallest (Node x Empty r) = x
smallest (Node x l r)     = smallest l

largest :: IntTree -> Int
largest Empty            = error "The tree is empty"
largest (Node x l Empty) = x
largest (Node x l r)     = largest r

ordered :: IntTree -> Bool
ordered Empty = error "The tree is empty"
ordered (Node i Empty Empty) = True
ordered (Node i Empty right)
  | i < largest right = True
  | otherwise = False
ordered (Node i left Empty) 
  | i > smallest left = True
  | otherwise = False
ordered (Node i left right)
  | i > largest left && i < smallest right  = (ordered left) && (ordered right)
  | otherwise                               = False

deleteLargest :: IntTree -> IntTree
deleteLargest Empty = error "The tree is empty"
deleteLargest (Node i left Empty) = Empty
deleteLargest (Node i left right) = Node i left (deleteLargest right)

deleteSmallest :: IntTree -> IntTree
deleteSmallest Empty = error "The tree is empty"
deleteSmallest (Node i Empty right) = Empty
deleteSmallest (Node i left right) = Node i (deleteSmallest left) right


delete :: Int -> IntTree -> IntTree
delete _ Empty = error "This tree is empty"
delete y (Node x l r)
    | not (present y (Node x l r))  = error "This number is not within the tree"
    | largest (Node x l r) == y     = deleteLargest (Node x l r)
    | smallest (Node x l r) == y    = deleteSmallest (Node x l r)
    | y < x     = Node x (delete y l) r 
    | y > x     = Node x l (delete y r)
    | isEmpty l = undefined 
    | otherwise = undefined

-- if y happens to be the smallest amount then you can deploy deleteLargest/Smallest
-- 

sorted :: IntTree -> Bool
sorted Empty = undefined
sorted t     = undefined
  where
    inRange :: Int -> Int -> IntTree -> Bool
    inRange = undefined

------------------------- Exercise 3

{-

instance Show a => Show (Tree a) where
    show = unlines . aux ' ' ' '
      where
        aux _ _ Empty = []
        aux c d (Node x s t) = 
          [ c:' ':m | m <- aux ' ' '|' s ] ++ 
          ['+':'-':show x] ++ 
          [ d:' ':n | n <- aux '|' ' ' t ]


type IntTree = Tree Int

-}


------------------------- Exercise 4

{-
preorder :: Tree a -> [a]
preorder t = walk [t]
 where
  walk = undefined

inorder :: Tree a -> [a]
inorder = undefined

postorder :: Tree a -> [a]
postorder = undefined

breadthfirst :: Tree a -> [a]
breadthfirst = undefined
-}

------------------------- Exercise 5

data Balance = Negative | Neutral | Positive

data AVLTree a = Leaf | AVLNode Balance a (AVLTree a) (AVLTree a)

{-
instance Show a => Show (AVLTree a) where
  show = show . forget

forget :: AVLTree a -> Tree a
forget = undefined
-}


insertUpdate :: Ord a => a -> AVLTree a -> (Bool,AVLTree a)
insertUpdate = undefined

insertAVL :: Ord a => a -> AVLTree a -> AVLTree a
insertAVL x = snd . insertUpdate x

toAVL :: Ord a => [a] -> AVLTree a
toAVL []     = Leaf
toAVL (x:xs) = insertAVL x (toAVL xs)
