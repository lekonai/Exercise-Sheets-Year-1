import Data.Char(isDigit)
------------------------- RPN Calculator

tokenize :: String -> [String]
tokenize = words

parser :: [String] -> [Either Integer String]
parser [] = []
parser (s:ss)
    | s == "+" || s == "-" || s == "*" = Right s : parser ss
    | otherwise = Left ( read s :: Integer ) : parser ss

pop :: [Integer] -> Integer
pop = head

isInteger :: Either Integer String -> Bool
isInteger x =
    case x of
        Left i -> True
        Right c -> False

fetch :: Either a a -> a
fetch x =
    case x of
        Left i -> i
        Right c -> c

-- x is the list taken in and y is the current stack
-- evaluate :: [Either Integer String] -> [Integer] -> Integer
-- evaluate [] [y] = y
-- evaluate (x:xs) (y1:y2:ys)
--     | not (isInteger x)  = evaluate xs (y1 (mathsFunc (fetch x)) y2 : ys)
--     | otherwise = evaluate xs (fetch x:y1:y2:ys)
myOwnRPN :: String -> String
myOwnRPN xs = evaluator ( tokenize xs ) []

int :: String -> Integer
int x = read x :: Integer

evaluator :: [String] -> [String] -> String
evaluator [] [y] = y
evaluator x (y1:y2:ys)
    | head x == "*" || head x == "-" || head x == "+" = evaluator (tail x) (show ((int y2) + (int y1)) : ys) -- this actually needs to be changed but it cannot be changed yet as this thing doesn't damn evaluate yet
    | all isDigit (head x) = evaluator (tail x) (head x : y1 : y2 : ys)
    | otherwise = error "type error lol"
    

-- apply x y z = int(x) (mathsFunc y) int(z)

mathsFunc :: Num a => String -> a -> a -> a
mathsFunc "+" = (+)
mathsFunc "-" = (-)
mathsFunc "*" = (*)
