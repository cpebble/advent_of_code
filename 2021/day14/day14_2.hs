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

--runSeq :: [String] -> H.HashMap String Char -> Int -> [String]
runSeq :: H.HashMap String Int -> H.HashMap String Char ->Int -> H.HashMap String Int
runSeq template mapping 0 = template
runSeq template mapping n =
    runSeq runLine mapping (n-1)
    where
      runLine =
        foldl (\m (k@[c1,c2],v) ->
            let c' = mapping H.! k
                p1 = [c1, c']
                p2 = [c', c2]
                m1 = H.insertWith (+) p1 v m
            in H.insertWith (+) p2 v m1
          ) H.empty (H.toList template)

count   :: Eq a => a -> [a] -> Int
count x =  length . filter (==x)

genPairs :: String -> [String]
genPairs [] = error "Shouldn't"
genPairs [t1] = []
genPairs (c1:c2:cs) = [c1, c2]:genPairs (c2:cs)


countScores :: [(Char, Int)] -> [Int]
countScores []  = []
countScores ((c1, i):ls)
   = i:countScores ls


main = do
    h <- openFile "input" ReadMode
    cont <- hGetContents h
    let (start,pairS) = splitAtFirst '\n' cont
    let (Right a) = parse (parseinp []) "" $ tail pairS
    let m = H.fromList a
    --let out = runSeq start m 1
    let temp = H.fromList $ zip (genPairs start) [1,1..]
    let res = runSeq temp m 40
    let sq = foldl (\m (k:_,v) ->
                H.insertWith (+) k v m
             ) (H.fromList [(last start,1)]) $ H.toList res
    let s = countScores . H.toList $ sq
    return $ maximum s - minimum s
    -- let flist = [count x fishies | x <- [0..10]]
