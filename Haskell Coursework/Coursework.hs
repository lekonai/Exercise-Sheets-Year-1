import Control.Monad
import Data.Maybe
import Data.List
import Data.Char
------------------------- Merge sort

merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge (x:xs) (y:ys)
    | x <  y    = x : merge    xs (y:ys)
    | x == y    = x : merge    xs    ys
    | otherwise = y : merge (x:xs)   ys

msort :: Ord a => [a] -> [a]
msort []  = []
msort [x] = [x]
msort xs  = msort (take n xs) `merge` msort (drop n xs)
  where
    n = length xs `div` 2

------------------------- Game world types

type Character = String
type Party     = [Character]

type Node      = Int
type Location  = String
type Map       = [(Node,Node)]

data Game      = Over
               | Game Map Node Party [Party]
  deriving (Eq,Show)

type Event     = Game -> Game


testGame :: Node -> Game
testGame i = Game [(0,1)] i ["Russell"] [[],["Brouwer","Heyting"]]


------------------------- Assignment 1: The game world

-- terminal example: connected [(1,2), (2,3), (4,6)] 2
connected :: Map -> Node -> [Node]
connected [] n = []
connected (m:ms) n
  | fst m == n    = snd m : connected ms n
  | snd m == n    = fst m : connected ms n
  | otherwise     = connected ms n

-- terminal example: connect 2 7 [(1,2), (2,3), (3,6), (4,6)]
connect :: Node -> Node -> Map -> Map
connect ni nj ms
  | (ni, nj) `elem` ms || (nj, ni) `elem` ms  = ms
  | otherwise                                 = connecting ni nj ms
    where
      connecting :: Node -> Node -> Map -> Map
      connecting ni nj (m:ms) = msort (m : (ni, nj) : ms)

disconnect :: Node -> Node -> Map -> Map
disconnect ni nj ms
  | (ni, nj) `elem` ms || (nj, ni) `elem` ms  = disconnecting ni nj ms
  | otherwise                                 = ms
    where
      disconnecting :: Node -> Node -> Map -> Map
      disconnecting ni nj (m:ms)
        | ((fst m) == ni && (snd m) == nj) || ((snd m) == ni && (fst m) == nj)  = ms
        | otherwise                                                             = m : disconnecting ni nj ms

-- terminal example: add ["Dijkstra", "Norvig"] (testGame 0)
add :: Party -> Event -- so this is Party -> Game -> Game
add _ Over              = Over
add [] (Game m n p ps)  = Game m n p ps
add (x:xs) (Game m n p ps)
  | not (x `elem` p)  = add xs (Game m n (insert x p) ps)
  | otherwise         = add xs (Game m n p ps)

addAt :: Node -> Party -> Event
-- terminal example: addAt 1 ["Dijkstra"] (testGame 0)
addAt _ _ Over                = Over
addAt _ [] (Game m n pj ps)   = Game m n pj ps -- practically an empty case
addAt nd pi (Game m n pj ps)  = Game m n pj (goToLocation 0 nd pi ps)

goToLocation :: Int -> Node -> Party -> [Party] -> [Party]
goToLocation _ _ [] (p:ps) = p:ps
goToLocation o nd pi (p:ps)
  | nd == 0 && o == 0 = (p ++ pi) : ps
  | nd == 0 && o == 1 = (p \\ pi) : ps
  | otherwise         = p : goToLocation o (nd - 1) pi ps

-- terminal example: addHere ["Dijkstra"] (testGame 0)
addHere :: Party -> Event
addHere pi (Game m n pj ps) = addAt n pi (Game m n pj ps)

-- terminal example: remove ["Brouwer","Russell"] (testGame 0)
remove :: Party -> Event
-- remove [] (Game m n p ps) = Game m n p ps -- just in case, will commit this
-- remove (x:xs) (Game m n p ps) = remove xs (Game m n (delete x p) ps)
remove pi Over             = Over
remove pi (Game m n pj ps) = Game m n (pj \\ pi) ps

-- terminal example: removeAt 1 ["Heyting"] (testGame 0)
removeAt :: Node -> Party -> Event
-- removeAt nd [] (Game m n pj ps) = Game m n pj ps -- this case isn't necessary
removeAt _ _ Over               = Over
removeAt nd pi (Game m n pj ps) = Game m n pj (goToLocation 1 nd pi ps)

removeHere :: Party -> Event
removeHere _ Over               = Over
removeHere pi (Game m n pj ps)  = removeAt n pi (Game m n pj ps)


------------------------- Assignment 2: Dialogues

prompt = ">>"
line0  = "There is nothing we can do."

data Dialogue = Action  String  Event
              | Branch  (Game -> Bool) Dialogue Dialogue
              | Choice  String  [( String , Dialogue )]

testDialogue :: Dialogue
testDialogue = Branch ( isAtZero )
  (Choice "Russell: Let's get our team together and head to Error." [])
  (Choice "Brouwer: How can I help you?"
    [ ("Could I get a haircut?", Choice "Brouwer: Of course." [])
    , ("Could I get a pint?",    Choice "Brouwer: Of course. Which would you like?"
      [ ("The Segmalt.",     Action "" id)
      , ("The Null Pinter.", Action "" id)]
      )
    , ("Will you join us on a dangerous adventure?", Action "Brouwer: Of course." (add ["Brouwer"] . removeHere ["Brouwer"]))
    ]
  )
 where
  isAtZero Over           = False
  isAtZero (Game _ n _ _) = n == 0


dialogue :: Game -> Dialogue -> IO Game

dialogue g (Action st ev) = 
  do
    putStrLn st
    return (ev g)

dialogue g (Branch c di dj) =
  do
    if c g == True
      then
        dialogue g di
    else
      dialogue g dj

-- second implementation
dialogue g (Choice sti chs) = do
  if length sti > 2 && not (isDigit (sti !! 0)) -- this is a very naff input
    then do
      putStrLn sti
      dialogue g (Choice "0" chs)
  else do
    if not ((read sti::Int) >= length chs)
      then do
        putStrLn ((show ((read sti::Int) + 1)) ++ " " ++ (fst (chs !! ((read sti::Int)))))
        dialogue g (Choice (show ((read sti::Int) + 1)) chs)
    else do
      if length chs == 0
        then
          return g
      else do
        x <- diaPromptVal (Choice sti chs)
        if (read x::Int) <= length chs && (read x::Int) > 0
          then
            dialogue g (snd (chs !! ((read x::Int) - 1)))
        else do
          return g -- this is when its 0, if you somehow manage to get through the first if clause then.. idk
          -- if (read x::Int) == 0 -- cancel dialogue
          --   then
          --     return g
          -- else do
          --   putStrLn "erroneous input" -- PRETTY SURE there's an error checking assignment, so this is not necessary yet
          --   return g

diaPromptVal :: Dialogue -> IO String
diaPromptVal (Choice sti chs) = do
  putStr (prompt ++ " ")
  x <- getLine
  if length x == 1
    then
      if numberChecker x
        then do
          if (read x::Int) <= length chs && (read x::Int) >= 0
            then
              return x
          else do
            putStrLn line6
            diaPromptVal (Choice sti chs)
      else do
        putStrLn line6
        diaPromptVal (Choice sti chs)
  else do
    putStrLn line6
    diaPromptVal (Choice sti chs)

findDialogue :: Party -> Dialogue
findDialogue p = searchTheDialogues p theDialogues
  where
    searchTheDialogues :: Party -> [(Party, Dialogue)] -> Dialogue
    searchTheDialogues [] _   = Action line0 id
    searchTheDialogues p []   = Action line0 id
    searchTheDialogues p xs
      | all (`elem` (fst (head xs))) p    = snd (head xs)
      | otherwise                         = searchTheDialogues p (tail xs)


------------------------- Assignment 3: The game loop

line1 = "You are in "
line2 = "You can travel to:"
line3 = "With you are:"
line4 = "You can see:"
line5 = "What will you do?"

type Counter = Int
data Decision = Trv Counter Int | Dia Counter Int | Tlk Counter Int 
  -- deriving Show
instance Show Decision where
  show (Trv cnt int) = show cnt ++ " " ++ show (theLocations !! int)
  show (Dia cnt int) = show cnt ++ " " ++ show int
  show (Tlk cnt int) = show cnt ++ " " ++ show int
-- this instance is only useful in one part, but i can't delete just two of them as all have to be derived i think

decisionFunction :: Game -> [Decision] -> [Decision]
decisionFunction (Game m n p ps) ds = (tokConns (connected m n) 0 (tokParty p p 0 (tokSee (ps !! n) (ps !! n) 0 [])))

tokConns :: [Node] -> Counter -> [Decision] -> [Decision]
tokConns [] c ds = ds
tokConns (m:ms) c ds = (Trv c m) : (tokConns ms 0 (ds))

tokParty :: Party -> Party -> Counter -> [Decision] -> [Decision]
tokParty [] pj c ds = ds
tokParty pi pj c ds = (Dia c (fromJust $ elemIndex (head pi) pj)) : (tokParty (tail pi) pj 0 ds)

tokSee :: Party -> Party -> Counter -> [Decision] -> [Decision]
tokSee [] pj c ds = ds
tokSee pi pj c ds = (Tlk c (fromJust $ elemIndex (head pi) pj)) : (tokSee (tail pi) pj 0 ds)

enumerator :: [Decision] -> Counter -> [Decision]
enumerator [] cnt = []
enumerator ((Trv c i):ds) cnt = (Trv (cnt + 1) i) : (enumerator ds (cnt + 1))
enumerator ((Dia c i):ds) cnt = (Dia (cnt + 1) i) : (enumerator ds (cnt + 1))
enumerator ((Tlk c i):ds) cnt = (Tlk (cnt + 1) i) : (enumerator ds (cnt + 1))

printingProcess :: Game -> Bool -> Bool -> Bool -> [Decision] -> IO ()
printingProcess (Game m n p ps) dtr ddi dtl [] = return ()
printingProcess (Game m n p ps) dtr ddi dtl (d:ds) = do
  case d of
    Trv c i -> do
      if not dtr
        then do
          putStrLn line2
          putStrLn (" " ++ show (Trv c i))
          printingProcess (Game m n p ps) True ddi dtl ds 
      else do
        putStrLn (" " ++ show (Trv c i))
        printingProcess (Game m n p ps) dtr ddi dtl ds 
    Dia c i -> do
      if not ddi
        then do
          putStrLn line3
          putStrLn (" " ++ show c ++ " " ++ show (p !! i))
          printingProcess (Game m n p ps) dtr True dtl ds 
      else do
        putStrLn (" " ++ show c ++ " " ++ show (p !! i))
        printingProcess (Game m n p ps) dtr ddi dtl ds 
    Tlk c i -> do
      if not dtl
        then do
          putStrLn line4
          putStrLn (" " ++ show c ++ " " ++ show ((ps !! n) !! i))
          printingProcess (Game m n p ps) dtr ddi True ds 
      else do
        putStrLn (" " ++ show c ++ " " ++ show ((ps !! n) !! i))
        printingProcess (Game m n p ps) dtr ddi dtl ds 

seek :: Int -> [Decision] -> Game -> IO Game
seek x [] (Game m n p ps) = return Over
seek x (d:ds) (Game m n p ps) = do
  case d of
    Trv c i ->
      if c == x
        then
          return (Game m i p ps)
      else
        seek x ds (Game m n p ps)
    Dia c i ->
      if c == x
        then 
          dialogue (Game m n p ps) (findDialogue [(p !! i)])
      else
        seek x ds (Game m n p ps)
    Tlk c i ->
      if c == x
        then
          dialogue (Game m n p ps) (findDialogue [((ps !! n) !! i)])
      else
        seek x ds (Game m n p ps)

multInput :: String -> [Int]
multInput x = msort (map read (words x) :: [Int])

multSeek :: [Int] -> [Decision] -> Game -> [String]
multSeek [] _ _ = []
multSeek (x:xs) (d:ds) (Game m n p ps) = do
  case d of
    Trv c i ->
      multSeek (x:xs) ds (Game m n p ps)
    Dia c i ->
      if c == x
        then 
          (p !! i) : multSeek (xs) ds (Game m n p ps) -- IMPLEMENT
      else
        multSeek (x:xs) ds (Game m n p ps)
    Tlk c i ->
      if c == x
        then
          ((ps !! n) !! i) : multSeek (xs) ds (Game m n p ps) -- IMPLEMENT
      else
        multSeek (x:xs) ds (Game m n p ps)

step :: Game -> IO Game
step (Game m n p ps) = do
  putStrLn (line1 ++ (theDescriptions !! n))
  printingProcess (Game m n p ps) False False False (enumerator (decisionFunction (Game m n p ps) []) 0)
  putStrLn line5
  x <- stepDecPromptVal (enumerator (decisionFunction (Game m n p ps) []) 0)-- get decision
  endGame <- if length x == 1 
    then do
      if (read x::Int) == 0
        then
          return Over
      else (seek (read x::Int) (enumerator (decisionFunction (Game m n p ps) []) 0) (Game m n p ps))
    else dialogue (Game m n p ps) (findDialogue (multSeek (multInput x) (enumerator (decisionFunction (Game m n p ps) []) 0) (Game m n p ps)))
  
  return endGame

numberChecker :: String -> Bool
-- numberChecker [] = False -- so then you don't get false positives when you have empty entries
numberChecker [] = True -- nevermind turns out i've worked around the issue anyway
numberChecker (s:ss)
  -- | isDigit s && ss == [] = True
  | isDigit s             = numberChecker ss
  | otherwise             = False

stepDecPromptVal :: [Decision] -> IO String
stepDecPromptVal ds = do
  putStr (prompt ++ " ")
  x <- getLine
  if length x >= 1
    then  
      if length x == 1
        then do
          if  numberChecker x == False || (read x::Int) > length ds || (read x::Int) <= -1
            then do
              putStrLn line6
              stepDecPromptVal ds 
          else do
            return x
      else do
        if any (== False) (map numberChecker (words x)) || length (words x) == 1 || not (multValidator (words x) (multEvaluator ds))
          then do
            putStrLn line6
            stepDecPromptVal ds   
        else do
          return x
  else do
    putStrLn line6
    stepDecPromptVal ds

multValidator :: [String] -> [Counter] -> Bool
multValidator [] y = True
multValidator (x:xs) y
  | (read x::Int) `elem` y  = multValidator xs y
  | otherwise   = False

multEvaluator :: [Decision] -> [Counter] -- basically this is just going to take all the counters/IDs so it can have a quantifier applied to it in validator?? ykwim
multEvaluator []               = []
multEvaluator ((Trv c i) : ds) = multEvaluator ds
multEvaluator ((Dia c i) : ds) = c : multEvaluator ds
multEvaluator ((Tlk c i) : ds) = c : multEvaluator ds

game :: IO ()
game = do
  firstLoop

firstLoop :: IO ()
firstLoop = loop start
  where
    loop :: Game -> IO ()
    loop Over   = return ()
    loop g      = do
      next <- step g
      loop next


------------------------- Assignment 4: Safety upgrades

line6 = "[Unrecognized input]"

------------------------- Assignment 5: Solving the game

data Command  = Travel [Int] | Select Party | Talk [Int]
  deriving Show

type Solution = [Command]

talk ::Game -> Dialogue -> [(Game,[Int])]
talk g d = explorerD g d []
  where
    explorerD :: Game -> Dialogue -> [Int] -> [(Game, [Int])]
    explorerD Over _ _            = []
    explorerD g (Action _ ev) is  = [(ev g, is)] -- thank god id functions count as valid events
    explorerD g (Branch c l r) is = if c g 
      then explorerD g l is
      else explorerD g r is
    explorerD g (Choice _ chs) is = concat [explorerD g d (is ++ [i]) | (i, (sti, d)) <- zip [1..] chs] -- bless lazy evaluation

nn :: Foldable t => t a -> Bool
nn = not . null

powerset :: [a] -> [[a]]
powerset = filterM (const[True, False])

allPossible :: Game -> [Party]
allPossible (Game m n p ps) = powerset ( concat ( filter nn [p] ++ (filter nn [(ps !! n)]) ) )
-- terminal example: filter nn (powerset (concat (allPossible (testGame 1))))
-- technically i don't actually need this function as i could just import it into select... but it makes select look
-- cleaner if i do this


select :: Game -> [Party]
select = allPossible
    
-- select g = filter nn (map helperParties (allPossible g) )
--   where
--     helperParties :: Party -> Party
--     helperParties p = cycle p theDialogues
--      where
--       cycle :: Party -> [(Party, Dialogue)] -> Party
--       cycle p []   = []
--       cycle p xs
--         | all (`elem` (fst (head xs))) p    = p
--         | otherwise                         = cycle p (tail xs)

travel :: Map -> Node -> [(Node,[Int])] -- it needs to return the indexes rather than the actual nodes to visit
travel m n = [(i, (breadthFirstS m i n [] (connected m i) [])) | i <- [(getMin m)..(getMax m)]]

type Visited = [Int]
type Queue = [Int]
type Path = [Int]
bfs :: Map -> Node -> Node -> Visited -> Queue -> Path -> [Int]
bfs m i d v [] p = p
bfs m i d v q p
  | i == d              = p
  | i `elem` v          = bfs m (head q) d v (tail q) p
  | nn (connected m i)  = bfs m (head q) d (v ++ [i]) ((tail q) ++ (filter (`notElem` (v ++ [i])) (connected m i))) (p ++ [i])
  | otherwise           = bfs m (head q) d (v ++ [i]) (tail q) (init p)
-- i = start, d = destination
-- FAILED ATTEMPT 1

getMin :: Map -> Node
getMin m = foldr1 min ((map fst m) ++ (map snd m))

getMax :: Map -> Node
getMax m = foldr1 max ((map fst m) ++ (map snd m))

-- terminal data: [(0,1),(0,2),(1,2),(2,3),(2,4),(3,5)]

allSteps :: Game -> [(Solution,Game)]
allSteps = undefined

solve :: Game -> Solution
solve = undefined

walkthrough :: IO ()
walkthrough = (putStrLn . unlines . filter (not . null) . map format . solve) start
  where
    format (Travel []) = ""
    format (Travel xs) = "Travel: " ++ unwords (map show xs)
    format (Select xs) = "Select: " ++ foldr1 (\x y -> x ++ ", " ++ y) xs
    format (Talk   []) = ""
    format (Talk   xs) = "Talk:   " ++ unwords (map show xs)


------------------------- Game data

start :: Game
start = Game theMap 0 [] theCharacters

theMap :: Map
theMap = [(1,2),(1,6),(2,4)]

theLocations :: [Location]
theLocations =
  [ "Home"           -- 0
  , "Brewpub"        -- 1
  , "Hotel"          -- 2
  , "Hotel room n+1" -- 3
  , "Temple"         -- 4
  , "Back of temple" -- 5
  , "Takeaway"       -- 6
  , "The I-50"       -- 7
  ]

theDescriptions :: [String]
theDescriptions =
  [ "your own home. It is very cosy."
  , "the `Non Tertium Non Datur' Brewpub & Barber's."
  , "the famous Logicester Hilbert Hotel & Resort."
  , "front of Room n+1 in the Hilbert Hotel & Resort. You knock."
  , "the Temple of Linearity, Logicester's most famous landmark, designed by Le Computier."
  , "the back yard of the temple. You see nothing but a giant pile of waste paper."
  , "Curry's Indian Takeaway, on the outskirts of Logicester."
  , "a car on the I-50 between Logicester and Computerborough. The road is blocked by a large, threatening mob."
  ]

theCharacters :: [Party]
theCharacters =
  [ ["Bertrand Russell"]                    -- 0  Home
  , ["Arend Heyting", "Luitzen Brouwer"]    -- 1  Brewpub
  , ["David Hilbert"]                       -- 2  Hotel
  , ["William Howard"]                      -- 3  Hotel room n+1
  , ["Jean-Yves Girard"]                    -- 4  Temple
  , []                                      -- 5  Back of temple
  , ["Haskell Curry", "Jean-Louis Krivine"] -- 6  Curry's takeaway
  , ["Gottlob Frege"]                       -- 7  I-50
  ]

theDialogues :: [(Party,Dialogue)]
theDialogues = let
  always _ = True
  end str  = Choice str []

  isconn  _ _  Over           = False
  isconn  i j (Game m _ _ _ ) = elem i (connected m j)

  here         Over           = 0
  here        (Game _ n _ _ ) = n

  inParty   _  Over           = False
  inParty   c (Game _ _ p _ ) = elem c p

  isAt    _ _  Over           = False
  isAt    n c (Game _ _ _ ps) = elem c (ps !! n)

  updateMap _  Over           = Over
  updateMap f (Game m n p ps) = Game (f m) n p ps

 in
  [ ( ["Russell"] , Choice "Russell: Let's go on an adventure!"
      [ ("Sure." , end "You pack your bags and go with Russell.")
      , ("Maybe later.", end "Russell looks disappointed.")
      ]
    )
  , ( ["Heyting","Russell"] , end "Heyting: Hi Russell, what are you drinking?\nRussell: The strong stuff, as usual." )
  , ( ["Bertrand Russell"] , Branch (isAt 0 "Bertrand Russell") ( let
      intro = "A tall, slender, robed character approaches your home. When he gets closer, you recognise him as Bertrand Russell, an old friend you haven't seen in ages. You invite him in.\n\nRussell: I am here with an important message. The future of Excluded-Middle Earth hangs in the balance. The dark forces of the Imperator are stirring, and this time, they might not be contained.\n\nDo you recall the artefact you recovered in your quest in the forsaken land of Error? The Loop, the One Loop, the Loop of Power? It must be destroyed. I need you to bring together a team of our finest Logicians, to travel deep into Error and cast the Loop into lake Bottom. It is the only way to terminate it."
      re1   = ("What is the power of the Loop?" , Choice "Russell: for you, if you put it on, you become referentially transparent. For the Imperator, there is no end to its power. If he gets it in his possession, he will vanquish us all." [re2])
      re2   = ("Let's go!" , Action "Let's put our team together and head for Error." (updateMap (connect 1 0) . add ["Bertrand Russell"] . removeHere ["Bertrand Russell"]) )
      in Choice intro [re1,re2]
      ) ( Branch ( (==7).here) (end "Russell: Let me speak to him and Brouwer."
      ) ( end "Russell: We should put our team together and head for Error." ) )
    )
  , ( ["Arend Heyting"] , Choice "Heyting: What can I get you?"
      [ ( "A pint of Ex Falso Quodbibet, please." , end "There you go." )
      , ( "The Hop Erat Demonstrandum, please."   , end "Excellent choice." )
      , ( "Could I get a Maltus Ponens?"          , end "Mind, that's a strong one." )
      ]
    )
  , ( ["Luitzen Brouwer"] , Branch (isAt 1 "Luitzen Brouwer")
      ( Choice "Brouwer: Haircut?"
        [ ( "Please." , let
          intro = "Brouwer is done and holds up the mirror. You notice that one hair is standing up straight."
          r1 i  = ( "There's just this one hair sticking up. Could you comb it flat, please?" , d i)
          r2    = ( "Thanks, it looks great." , end "Brouwer: You're welcome.")
          d  i  | i == 0    = Choice intro [r2]
                | otherwise = Choice intro [r1 (i-1),r2]
        in d 100)
        , ( "Actually, could you do a close shave?" , end "Of course. I shave everyone who doesn't shave themselves." )
        , ( "I'm really looking for help." , Choice "Brouwer: Hmmm. What with? Is it mysterious?"
          [ ( "Ooh yes, very. And dangerous." , Action "Brouwer: I'm in!" (add ["Luitzen Brouwer"] . removeHere ["Luitzen Brouwer"]) )
          ] )
        ]
      )
      ( end "Nothing" )
    )
  , ( ["David Hilbert"] , Branch (not . isconn 2 3) (let
        intro = "You wait your turn in the queue. The host, David Hilbert, puts up the first guest in Room 1, and points the way to the stairs.\n\nYou seem to hear that the next couple are also put up in Room 1. You decide you must have misheard. It is your turn next.\n\nHilbert: Lodging and breakfast? Room 1 is free."
        re1   = ("Didn't you put up the previous guests in Room 1, too?" , Choice "Hilbert: I did. But everyone will move up one room to make room for you if necessary. There is always room at the Hilbert Hotel & Resort." [("But what about the last room? Where do the guests in the last room go?" , Choice "Hilbert: There is no last room. There are always more rooms." [("How can there be infinite rooms? Is the hotel infinitely long?" , Choice "Hilbert: No, of course not! It was designed by the famous architect Zeno Hadid. Every next room is half the size of the previous." [re2])])])
        re2   =  ("Actually, I am looking for someone." , Action "Hilbert: Yes, someone is staying here. You'll find them in Room n+1. Through the doors over there, up the stairs, then left." (updateMap (connect 2 3)))
      in Choice intro [re1,re2]
      ) (end "Hilbert seems busy. You hear him muttering to himself: Problems, problems, nothing but problems. You decide he has enough on his plate and leave." )
    )
  , ( ["William Howard"] ,  Branch (isAt 3 "William Howard")
      (Choice "Howard: Yes? Are we moving up again?" [("Quick, we need your help. We need to travel to Error." , Action "Howard: Fine. My bags are packed anyway, and this room is tiny. Let's go!" (add ["William Howard"] . removeAt 3 ["William Howard"]))]
      ) (Branch (isAt 6 "William Howard") (Choice "Howard: What can I get you?"
        [ ("The Lambda Rogan Josh with the Raita Monad for starter, please." , end "Coming right up.")
        , ("The Vindaloop with NaN bread on the side." , Choice "Howard: It's quite spicy." [("I can handle it." , end "Excellent." ) ] )
        , ("The Chicken Booleani with a stack of poppadums, please.", end "Good choice." )
        ]
      ) (end "Howard: We need to find Curry. He'll know the way.")
    ) )
  , ( ["Jean-Yves Girard"] , Branch (isconn 4 5)  (end "You have seen enough here.") (Action "Raised on a large platform in the centre of the temple, Girard is preaching the Linearity Gospel. He seems in some sort of trance, so it is hard to make sense of, but you do pick up some interesting snippets. `Never Throw Anything Away' - you gather they must be environmentalists - `We Will Solve Church's Problems', `Only This Place Matters'... Perhaps, while he is speaking, now is a good time to take a peek behind the temple..." (updateMap (connect 4 5) ))
    )
  , ( ["Vending machine"] , Choice "The walls of the Temple of Linearity are lined with vending machines. Your curiosity gets the better of you, and you inspect one up close. It sells the following items:"
      [ ( "Broccoli"  , end "You don't like broccoli." )
      , ( "Mustard"   , end "It might go with the broccoli." )
      , ( "Watches"   , end "They seem to have a waterproof storage compartment. Strange." )
      , ( "Camels"    , end "You don't smoke, but if you did..." )
      , ( "Gauloises" , end "You don't smoke, but if you did..." )
      ]
    )
  , ( ["Jean-Louis Krivine"] , end "Looking through the open kitchen door, you see the chef doing the dishes. He is rinsing and stacking plates, but it's not a very quick job because he only has one stack. You also notice he never passes any plates to the front. On second thought, that makes sense - it's a takeaway, after all, and everything is packed in cardboard boxes. He seems very busy, so you decide to leave him alone."
    )
  , ( ["Haskell Curry"] , Branch (isAt 6 "Haskell Curry")
      (Choice "Curry: What can I get you?"
        [ ("The Lambda Rogan Josh with the Raita Monad for starter, please." , end "Coming right up.")
        , ("The Vindaloop with NaN bread on the side." , Choice "Curry: It's quite spicy." [("I can handle it." , end "Excellent." ) ] )
        , ("The Chicken Booleani with a stack of poppadums, please.", end "Good choice." )
        , ("Actually, I am looking for help getting to Error." , end "Curry: Hmm. I may be able to help, but I'll need to speak to William Howard.")
        ]
      ) (end "Nothing")
    )
  , ( ["Haskell Curry","William Howard"] , Branch (not . isconn 6 7) (Action "Curry:  You know the way to Error, right?\nHoward: I thought you did?\nCurry:  Not really. Do we go via Computerborough?\nHoward: Yes, I think so. Is that along the I-50?\nCurry:  Yes, third exit. Shall I go with them?\nHoward: Sure. I can watch the shop while you're away." (add ["Haskell Curry"] . removeAt 6 ["Haskell Curry"] . addAt 6 ["William Howard"] . remove ["William Howard"] . updateMap (connect 6 7) )) (end "It's easy, just take the third exit on I-50.")
    )
  , ( ["Gottlob Frege"] , end "A person who appears to be the leader of the mob approaches your vehicle. When he gets closer, you recognise him as Gottlob Frege. You start backing away, and he starts yelling at you.\n\nFrege: Give us the Loop! We can control it! We can wield its power!\n\nYou don't see a way forward. Perhaps Russell has a plan." )
  , ( ["Bertrand Russell","Gottlob Frege","Luitzen Brouwer"] , let
        intro = "Frege is getting closer, yelling at you to hand over the Loop, with the mob on his heels, slowly surrounding you. The tension in the car is mounting. But Russell calmly steps out to confront Frege.\n\nRussell:"
        re1   = ( "You cannot control its power! Even the very wise cannot see all ends!" , Choice "Frege: I can and I will! The power is mine!\n\nRussell:" [re2,re3] )
        re2   = ( "Brouwer, whom do you shave?" , Choice "Brouwer: Those who do not shave themselves. Obviously. Why?\n\nRussell:" [re3] )
        re3   = ( "Frege, answer me this: DOES BROUWER SHAVE HIMSELF?" , Action
                  "Frege opens his mouth to shout a reply. But no sound passes his lips. His eyes open wide in a look of bewilderment. Then he looks at the ground, and starts walking in circles, muttering to himself and looking anxiously at Russell. The mob is temporarily distracted by the display, uncertain what is happening to their leader, but slowly enclosing both Frege and Russell. Out of the chaos, Russell shouts:\n\nDRIVE, YOU FOOLS!\n\nYou floor it, and with screeching tires you manage to circle around the mob. You have made it across.\n\nEND OF ACT 1. To be continued..."
                  (const Over)
                )
      in Choice intro [re1,re2,re3]
    )
  , ( ["Bertrand Russell","Haskell Curry","Luitzen Brouwer"] , Branch ((==7).here) (end "Road trip! Road trip! Road trip!") (end "Let's head for Error!")
    )
  ]
