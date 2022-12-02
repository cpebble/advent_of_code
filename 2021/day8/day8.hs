import qualified Data.Set as S
import System.IO

-- | partitions the list at the points matching predicate, dropping those
-- elements that match.
breakDrop :: (a -> Bool) -> [a] -> [[a]]
breakDrop p = next . break p . dropWhile p
  where
    next ([], _) = []
    next (as, bs) = as : breakDrop p bs

oneSegment = 2

fourSegment = 4

sevenSegment = 3

eightSegment = 7

handleLine l =
  let [entry, out] = breakDrop (== '|') l
      entries = breakDrop (== ' ') entry
      outentries = breakDrop (== ' ') out
      res =
        filter
          ( \x ->
              length x == oneSegment
                || length x == fourSegment
                || length x == sevenSegment
                || length x == eightSegment
          )
          outentries
   in length res

part2 line =
  let [entry, out] = breakDrop (== '|') line
      entries = breakDrop (== ' ') entry
      outS = map S.fromList $ breakDrop (== ' ') out
      mapping = handleEntries entries
      outputM = [c | s <- outS, (c,set) <- mapping, s == set ]
  in (read outputM :: Int)
isKnownLength x = x == 2 || x == 4 || x == 3 || x == 7

-- 2 3 5
--handleEntries :: [[Char]] -> [S.Set Char]
handleEntries entries =
  let sets@(one, four, seven, eight) = findKnowns entries
   in do
        num <- entries
        let numS = S.fromList num
        return $ case length numS of
          1 -> undefined
          2 -> ('1', numS)
          3 -> ('7', numS)
          4 -> ('4', numS)
          5 | length (S.intersection numS seven) == 3 -> ('3', numS)
          5 | length (S.intersection numS four) == 3 -> ('5', numS)
          5 -> ('2', numS)
          6 | length (S.intersection numS four) == 4 -> ('9', numS)
          6 | length (S.intersection numS seven) == 3 -> ('0', numS)
          6 -> ('6', numS)
          7 -> ('8', numS)
          _ -> error "Encountered weird-ass number"
  where
    findKnowns :: [String] -> (S.Set Char, S.Set Char, S.Set Char, S.Set Char)
    findKnowns line =
      let oneSet = S.fromList . head $ filter ((== 2) . length) line
          fourSet = S.fromList . head $ filter ((== 4) . length) line
          sevenSet = S.fromList . head $ filter ((== 3) . length) line
          eightSet = S.fromList . head $ filter ((== 7) . length) line
       in (oneSet, fourSet, sevenSet, eightSet)

handleOutput mapping out = undefined

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let inlines = lines cont
        out = map handleLine inlines
        out2 = map part2 inlines
    return $ sum out2
