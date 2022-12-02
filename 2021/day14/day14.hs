import System.IO
import qualified Data.HashMap.Strict as H
import Text.ParserCombinators.Parsec
    ( letter,
      newline,
      string,
      eof,
      optional,
      (<|>),
      many,
      parse,
      CharParser )

splitAtFirst :: Eq a => a -> [a] -> ([a], [a])
splitAtFirst x = fmap (drop 1) . break (x ==)

parseinp :: [(String,Char)] -> CharParser () [(String,Char)]
parseinp res =
    do
      pairS <- many letter
      string " -> "
      insS <- letter
      optional newline
      parseinp $ (pairS,insS):res
    <|> do
         eof
         return res

runSeq :: String -> H.HashMap String Char -> Int ->  String
runSeq template mapping 0 = template
runSeq template mapping n =
    runSeq (runline mapping template "") mapping (n-1)
    where
      runline :: H.HashMap String Char -> String -> String -> String
      runline m [] line = reverse line
      runline m [t1] line = runline m [] (t1:line)
      runline m (t1:t2:ts) line =
        case H.lookup [t1, t2] m of
          Nothing -> runline m (t2:ts) (t1:line)
          Just c -> runline m (t2:ts) (c:t1:line)

count   :: Eq a => a -> [a] -> Int
count x =  length . filter (==x)

calcScore s =
    let ls = [count x s | x <- "CPSFOVNPKBH", count x s > 0]
    in maximum ls - minimum ls

main = do
    h <- openFile "input" ReadMode
    cont <- hGetContents h
    let (start,pairS) = splitAtFirst '\n' cont
    let (Right a) = parse (parseinp []) "" $ tail pairS
    let m = H.fromList a
    let out = runSeq start m 20
    return $ calcScore out
    -- let flist = [count x fishies | x <- [0..10]]
