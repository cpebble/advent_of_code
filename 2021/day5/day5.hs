import qualified Data.HashMap.Strict as H
import System.IO
import Text.ParserCombinators.Parsec

parseInput x =
  (eof >> return x)
    <|> do
      l <- parseLine
      spaces
      parseInput (l : x)

parseLine = do
  x1 <- parseNum
  char ','
  y1 <- parseNum
  string " -> "
  x2 <- parseNum
  char ','
  y2 <- parseNum
  return ((x1, y1), (x2, y2))

parseNum :: CharParser () Int
parseNum = do
  a <- many digit
  return $ readInt a

readInt :: String -> Int
readInt = read

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let (Right inp) = parse (parseInput []) "example" cont
    let m = fillArr inp
    return $ calcOverlaps m
    --return inp

fillArr :: [((Int, Int), (Int, Int))] -> H.HashMap (Int, Int) Int
fillArr dat =
  let lists = map genListOf2 dat
  in foldl insertLine H.empty lists
  where
    insertLine m ls=
        foldl (\m x -> H.insertWith (+) x 1 m) m ls


genListOf ((x1, y1), (x2, y2))
  | x1 == x2 = [(x1, yn) | yn <- [min y1 y2 .. max y1 y2]]
  | y1 == y2 = [(xn, y1) | xn <- [min x1 x2 .. max x1 x2]]
  | otherwise = []

genListOf2 ((x1, y1), (x2, y2))
  | x1 == x2 = [(x1, yn) | yn <- [min y1 y2 .. max y1 y2]]
  | y1 == y2 = [(xn, y1) | xn <- [min x1 x2 .. max x1 x2]]
  | y1 > y2 && x1 > x2 = zip [x1,x1-1..x2] [y1,y1-1..y2]
  | y1 > y2 && x1 < x2 = zip [x1..x2] [y1,y1-1..y2]
  | y1 < y2 && x1 > x2 = zip [x1,x1-1..x2] [y1..y2]
  | y1 < y2 && x1 < x2 = zip [x1..x2] [y1..y2]
  | otherwise = error "A"

calcOverlaps m =
    foldl (\s (k,v) -> if v > 1 then s+1 else s) 0 $ H.toList m
