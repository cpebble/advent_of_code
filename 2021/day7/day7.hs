import Data.List (sort, sortBy)
import System.IO

-- | partitions the list at the points matching predicate, dropping those
-- elements that match.
breakDrop :: (a -> Bool) -> [a] -> [[a]]
breakDrop p = next . break p . dropWhile p
  where
    next ([], _) = []
    next (as, bs) = as : breakDrop p bs

count :: Eq a => a -> [a] -> Int
count x = length . filter (== x)

countFuel :: [Int] -> Int -> Int
countFuel crabs pos =
  sum $ calcFuels crabs pos
  where
    calcFuels :: [Int] -> Int -> [Int]
    calcFuels crabs pos = do
      crab <- crabs
      return . abs $ crab - pos

fcost :: Int -> Int
fcost n = (n*(n+1)) `div` 2

countFuel2 :: [Int] -> Int -> Int
countFuel2 crabs pos =
  sum $ calcFuels crabs pos
  where
    calcFuels :: [Int] -> Int -> [Int]
    calcFuels crabs pos = do
      crab <- crabs
      return . fcost . abs $ crab - pos


readInt :: String -> Int
readInt = read

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let crabs = map readInt $ breakDrop (== ',') cont
        scrabs = sort crabs
        fuels = [(i, countFuel2 scrabs i) | i <- [minimum scrabs .. maximum scrabs]]
        sfuels = take 1 $ sortBy (\a b -> snd a `compare` snd b) fuels
    return sfuels
