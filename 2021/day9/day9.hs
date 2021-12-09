import Data.List.Split
import System.IO
import Data.List

neighbors (x, y) h w =
  filter
    (\(x', y') -> x' >= 0 && x' < w && y' >= 0 && y' < h)
    [(x + dx, y + dy) | (dx, dy) <- [(-1, 0), (1, 0), (0, 1), (0, -1)]]

--[(x + dx, y + dy) | dx <- [-1 .. 1], dy <- [-1 .. 1], not (dx == 0 && dy == 0)]

mapInd :: (a -> Int -> b) -> [a] -> [b]
mapInd f l = zipWith f l [0 ..]

readInt :: String -> Int
readInt = read

isLowPoint :: [[Int]] -> Int -> Int -> Int -> Int -> Bool
isLowPoint m x y h w =
  let v = m !! y !! x
   in all
        ( \(x, y) ->
            v < (m !! y !! x)
        )
        $ neighbors (x, y) h w

findLowPoints :: [[Int]] -> [(Int, Int)]
findLowPoints m =
  let h = length m
      w = length $ head m
   in filter (/= (-1, -1)) . concat $
        mapInd
          ( \r y ->
              mapInd
                ( \c x ->
                    if isLowPoint m x y h w
                      then (x, y)
                      else (-1, -1)
                )
                r
          )
          m

findBasins :: [[Int]] -> Int -> Int -> [Int]
findBasins m h w =
  let lps = findLowPoints m
   in map (\lp -> exploreBasin m [] [lp]) lps
  where
    exploreBasin :: [[Int]] -> [(Int, Int)] -> [(Int, Int)] -> Int
    exploreBasin m explored [] = length explored
    exploreBasin m explored q@((x, y) : qs) =
      let v = m !! y !! x
       in if (x,y) `elem` explored
            then exploreBasin m explored qs
            else
              let nns =
                    [
                    (nx, ny) |
                    (nx, ny) <- neighbors (x, y) h w,
                    (nx, ny) `notElem` explored,
                    m!!ny!!nx /= 9
                    ]
               in exploreBasin m ((x,y):explored) (qs<>nns)

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let lin  = endBy "\n" cont
        m    = map (map (\c -> readInt [c])) lin
        lps  = findLowPoints m
        lpss = map (\(x, y) -> 1 + m !! y !! x) lps
        bs   = findBasins m (length m) (length . head $ m)
        sbs  = product . take 3 . reverse $ sort bs
    return $ (sum lpss, sbs)
