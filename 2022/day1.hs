import Data.List
import Data.List.Split
import System.IO

target = "day1.example"


main = do
    handle <- openFile target ReadMode
    cont <- hGetContents handle
    let elves = List.splitOn "\n\n" cont
    print elves


