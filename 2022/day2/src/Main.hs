module Main (main) where

target = "example"

winMap =
  [ ('A', 'B'),
    ('B', 'C'),
    ('C', 'A')
  ]

scoreMap =
  [ ('A', 1),
    ('B', 2),
    ('C', 3)
  ]

type SMap = [(Char, Char)]

runWithMap :: SMap -> [String] -> Int
runWithMap smap lines =
  map
    ( \round ->
        let (Just move) = lookup round !! 2 smap
            (Just toWin) = lookup round !! 0 winMap
            (Just moveScore) = lookup move scoreMap
            roundScore =
              ( undefined
              )
         in moveScore + roundScore
    )
    lines

main :: IO ()
main = do
  handle <- openFile target ReadMode
  cont <- hGetContents handle
  let l = lines cont

