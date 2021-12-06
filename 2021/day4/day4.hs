import System.IO

-- | partitions list into sub-lists of length given by the Int:
splitEvery :: Int -> [a] -> [[a]]
splitEvery _ [] = []
splitEvery n xs = as : splitEvery n bs
  where
    (as, bs) = splitAt n xs

-- | partitions the list at the points matching predicate, dropping those
-- elements that match.
breakDrop :: (a -> Bool) -> [a] -> [[a]]
breakDrop p = next . break p . dropWhile p
  where
    next ([], _) = []
    next (as, bs) = as : breakDrop p bs

splitBoards x
  | length x < 5 = []
  | otherwise =
    let (b, xs) = splitAt 6 x
     in b : splitBoards xs

parseBoard [] = []
parseBoard ("" : xs) = parseBoard xs
parseBoard (x : xs) =
  map (read :: String -> Int) (splitEvery 3 x) : parseBoard xs

--parseBoard (x:xs) =
--map (\x -> (False, read x :: Int)) (splitEvery 3 x) : parseBoard xs

-- Returns -1 if no win
-- or I if win on round I
runSeq :: (Num t, Eq a) => [a] -> [a] -> t -> t
runSeq _ [] i = i -1
runSeq [] _ i = -1
runSeq (s : seq) boardLine i =
  runSeq seq (filter (/= s) boardLine) (i + 1)

calcBoardIsWinning :: [Int] -> [[Int]] -> Int
calcBoardIsWinning sequ board =
  foldl min 90000
    . filter (/= (-1))
    $ map (\x -> runSeq sequ x 0) board

--calcWinning :: [Int] -> [[[Int]]] -> t
calcWinning sequ listOfBoards =
  let wins = filter (< 90000) $ map (calcBoardIsWinning sequ) listOfBoards
   in wins

--boardscore :: [Int] -> [[Int]] -> Int
boardscore sequ b =
  sum $ concatMap (filter (`notElem` sequ)) b

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let (sequ : boards) = lines cont
    let seq2 = map (read :: String -> Int) $ breakDrop (== ',') sequ
        pboards = map parseBoard (splitBoards boards)
        wins = calcWinning seq2 pboards
        (winI, winB) =
          foldl1
            ( \(accw, accb) (w, b) ->
                if w < accw
                  then (w, b)
                  else (accw, accb)
            )
            $ zip wins pboards
        ws = boardscore (take (winI+1) seq2) winB
    return (ws)
