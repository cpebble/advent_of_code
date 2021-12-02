import System.IO

example :: [String]
example =
  [ "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2"
  ]

type Pos = (Int, Int)

navigate :: [String] -> Pos -> Pos
navigate [] p = p
navigate (dir:dirs) (depth, pos) = 
    let (dir2: amount:_) = words dir
        amountI = (read :: String -> Int) amount
    in case dir2 of
        "forward" -> navigate dirs (depth, pos+amountI)
        "down"    -> navigate dirs (depth + amountI, pos)
        "up"      -> navigate dirs (depth - amountI, pos)
        _ -> error dir 


navigate2 :: [String] -> Pos -> Int -> Pos
navigate2 [] p _ = p
navigate2 (dir:dirs) (depth, pos) aim = 
    let (dir2: amount:_) = words dir
        amountI = (read :: String -> Int) amount
    in case dir2 of
        "forward" -> navigate2 dirs (depth + amountI * aim, pos+amountI) aim
        "down"    -> navigate2 dirs (depth, pos) (aim+amountI)
        "up"      -> navigate2 dirs (depth, pos) (aim-amountI)
        _ -> error dir 

main =
  do
    handle <- openFile "input" ReadMode
    cont <- hGetContents handle
    let dec = lines cont
    let res = navigate dec (0, 0)
    let (d,p)= navigate2 dec (0,0) 0
    print res
    print (d*p)
    return ()
