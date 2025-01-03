module Lib where
import Data.List.Split
import qualified Data.List as L
import System.IO

target = "src/input"
-- target = "day1.example"

t1 :: [[String]] -> Int
t1 elvs =
    maximum $ map (sum . map (read :: String -> Int)
        ) elvs
t2 :: [[String]] -> Int
t2 elvs =
    sum . (take 3) . reverse . L.sort $ map (sum . map (read :: String -> Int)
        ) elvs


day = do
    handle <- openFile target ReadMode
    cont <- hGetContents handle
    let elves = splitOn "\n\n" cont
    let elves_ = map lines elves
    print $ t2 elves_



