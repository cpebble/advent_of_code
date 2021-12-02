import System.IO
example :: [Int]
example =
  [199,200,208,210,200,207,240,269,260,263]

p1 :: [Int] -> Int -> Int -> Int
p1 [] prev incs = incs
p1 (x:xs) prev incs =
    if x > prev then
        p1 xs x (incs + 1)
    else
        p1 xs x incs

p2 nums@(x:y:z:_) =
    (x + y + z) : p2 (tail nums)
p2 _ = []

main =
    do
      handle <- openFile "input" ReadMode
      cont <- hGetContents handle
      let dec = map (read :: String -> Int) $ lines cont
      print $ p1 dec 0 (-1)
      print $ p1 (p2 dec) 0 (-1)
