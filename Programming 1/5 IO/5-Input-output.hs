
-- import System.Random 


import Data.Time.Clock

randomIO :: IO Int
randomIO = do
  t <- getCurrentTime
  (return . floor . (*1000) . toRational . utctDayTime) t


------------------------- Exercise 1

repeatMe :: IO ()
repeatMe = do
  x <- getLine
  if x == ""
    then repeatMe
  else
    putStrLn("You just told me " ++ x)

------------------------- Exercise 2

lizzy :: IO ()
lizzy = do
  putStrLn(welcome)
  lizzyLoop

lizzyLoop :: IO ()
lizzyLoop = do
  stri <- getLine
  r <- randomIO :: IO Int
  if stri /= "Exit"
    then do
      putStrLn(randomresponse stri r)
      lizzyLoop
  else
    putStrLn(exit)
  

------------------------- Exercise 3

welcome :: String
welcome =
  "\nDr. Lizzy -- Good morning, how are you today. Please tell me what's on your mind.\n"

exit :: String
exit =
  "\nDr. Lizzy -- Thank you for coming in today. I think we made good progress. I will see you next week at the same time.\n"

response :: String -> String
response str =
  "\nDr. Lizzy -- " ++ x ++ y ++ "\n"
     where
       x = responses1 !! (length str `mod` 3)
       y = responses2 !! (length str `mod` 5)
       responses1 =
         ["Interesting that you say \"" ++ str ++ "\"\n"
         ,"Hmm... "
         ,"Let\'s examine that more closely, shall we.\n"
         ]
       responses2 =
         ["Please tell me more about that."
         ,"How does that make you feel?"
         ,"Now, why do you mention that?"
         ,"Do you think this has something to do with your mother?"
         ,"Go on."
         ]

randomresponse :: String -> Int -> String
randomresponse str r =
  "\nDr. Lizzy -- " ++ x ++ y ++ "\n"
     where
       x = responses1 !! (r `mod` 3)
       y = responses2 !! (r `mod` 5)
       responses1 =
         ["Interesting that you say \"" ++ str ++ "\"\n"
         ,"Hmm... "
         ,"Let\'s examine that more closely, shall we.\n"
         ]
       responses2 =
         ["Please tell me more about that."
         ,"How does that make you feel?"
         ,"Now, why do you mention that?"
         ,"Do you think this has something to do with your mother?"
         ,"Go on."
         ]

-- Challenge


