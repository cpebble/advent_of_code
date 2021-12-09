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
              length x == oneSegment   ||
              length x == fourSegment  ||
              length x == sevenSegment ||
              length x == eightSegment
          )
          outentries
   in (length res)

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let inlines = lines cont
        out = map handleLine inlines
    return $ sum out
