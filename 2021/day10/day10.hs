import qualified Data.HashMap.Strict as H
import System.IO
import Data.List

--import Text.ParserCombinators.Parsec

mapping = H.fromList [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]

mappingP = H.fromList [(')', 3), (']', 57), ('}', 1197), ('>', 25137)]

data Cause = Inv | Inc
  deriving (Show)

data Result
  = Err (Cause, String, Char)
  | Succ String
  deriving (Show)

isErr (Err _) = True
isErr (Succ _) = False

isInv (Err (Inv, _, _)) = True
isInv _ = False

calcScores :: [Result] -> [Int]
calcScores n =
  do
    c <- n
    case c of
      Succ s -> []
      Err (Inv, _, c) -> return $ mappingP H.! c
      Err (Inc, _, _) -> []

calcScores2 :: [Result] -> [Int]
calcScores2 n =
  do
    c <- n
    case c of
      Succ s -> []
      Err (Inv, _, _) -> []
      Err (Inc, s, _) -> return $ calcLine s 0
  where
    ctoi ')' = 1
    ctoi ']' = 2
    ctoi '}' = 3
    ctoi '>' = 4
    ctoi _ = error "A"
    calcLine :: String -> Int -> Int
    calcLine [] sc = sc
    calcLine (c : cs) sc =
      calcLine cs (sc * 5 + ctoi c)

parseLine [] = Succ []
parseLine s@(c : cs)
  | c `elem` "(<[{" =
    let expected = mapping H.! c
     in case parseLine cs of
          Err (Inc, s, _) -> Err (Inc, s <> [expected], c)
          Err x -> Err x
          Succ [] -> Err (Inc, [expected], c)
          Succ cs_ | head cs_ == expected -> parseLine (tail cs_)
          Succ cs_ -> Err (Inv, "Invalid expected " <> show expected, head cs_)
  | otherwise = Succ s

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let parsed = map parseLine (lines cont)
    --Part 1: return . sum $ calcScores parsed
    let sorted = sort $ calcScores2 parsed
    return $ sorted!!((length sorted `div` 2))
