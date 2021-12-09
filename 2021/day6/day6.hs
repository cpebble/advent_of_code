import System.IO
import Distribution.Types.Lens

-- | partitions the list at the points matching predicate, dropping those
-- elements that match.
breakDrop :: (a -> Bool) -> [a] -> [[a]]
breakDrop p = next . break p . dropWhile p
  where
    next ([], _) = []
    next (as, bs) = as : breakDrop p bs

fround :: [Int] -> [Int]
fround fs = do
    f <- fs
    if f == 0
    then [6,8]
    else return (f-1)

runRounds fs 0 = fs
runRounds fs n = runRounds (fround fs) (n-1)
    
count   :: Eq a => a -> [a] -> Int
count x =  length . filter (==x)

runRounds2 [] _ = error ""
runRounds2 l 0 = l
runRounds2 (zeros:fs) n =
   let newList = [
        fs!!0,
        fs!!1,
        fs!!2,
        fs!!3,
        fs!!4,
        fs!!5,
        fs!!6 + zeros,
        fs!!7,
        zeros]
    in runRounds2 (newList) (n-1)

readInt :: String -> Int
readInt = read
main =
  do
    handle <- openFile "input2" ReadMode
    cont <- hGetContents handle
    let fishies = map readInt $ breakDrop (==',') cont
    let flist = [count x fishies | x <- [0..10]]
    print flist
    print $ sum (runRounds2 flist 9999999)
    return ()
