module Main where

import Text.ParserCombinators.Parsec

symbol :: String -> CharParser () String
symbol s = string s <* many (char ' ')

lexeme :: CharParser () a -> CharParser () a
lexeme p = p <* spaces

evalexp :: CharParser () Int
evalexp = do
  t <- parseTerm
  evalExp' t

parseTerm =
  do t <- lexeme (many1 digit); return (read t :: Int)
    <|> do
      symbol "("
      n <- evalexp
      symbol ")"
      return n

parse2Term =
  do t <- lexeme (many1 digit); return (read t :: Int)
    <|> do
      symbol "("
      n <- eval2Exp
      symbol ")"
      return n

evalExp' :: Int -> CharParser () Int
evalExp' n =
  do
    op <- lexeme (oneOf "+-*")
    let opf = getOp op
    t' <- parseTerm
    let n' = opf n t'
    evalExp' n'
    <|> return n

-- >>> parse evalexp "" "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
-- Right 12240
-- >>> parse evalexp "" "2 * 3 + (4 * 5)"
-- Right 26
getOp '+' = (+)
getOp '-' = (-)
getOp '*' = (*)
getOp _ = undefined

evalFile n =
  do
    char '\n'
    n' <- evalexp
    evalFile (n + n')
    <|> return n

eval2Exp = do
  n <- eval2Exp'
  rest n
  where
    rest n =
      do
        symbol "*"
        n' <- eval2Exp'
        rest (n' * n)
        <|> return n

{- Test
>>> parse eval2Exp "" "1 + (2 * 3) + (4 * (5 + 6))" 
Right 51

>>> parse eval2Exp "" "2 * 3 + (4 * 5)" 
Right 46

>>> parse eval2Exp "" "5 + (8 * 3 + 9 + 3 * 4 * 3)" 
Right 1445

>>> parse eval2Exp "" "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
Right 669060
-}

eval2Exp' = do
  n <- parse2Term
  rest n
  where
    rest n = do
      op <- lexeme (oneOf "+-")
      let opf = getOp op
      n' <- parse2Term
      rest (opf n n')
      <|> return n

compute :: Int -> [String] -> Either ParseError Int
compute n [] = return n
compute n (s : ss) =
  do
    n' <- parse evalexp "" s
    compute (n + n') ss
compute2 :: Int -> [String] -> Either ParseError Int
compute2 n [] = return n
compute2 n (s : ss) =
  do
    n' <- parse eval2Exp "" s
    compute2 (n + n') ss

--
main :: IO ()
main = do
  content <- readFile "input"
  print (compute 0 $lines content)
  print (compute2 0 $lines content)
