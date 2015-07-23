(define-library (storkar league-db)
  (import (chibi)
          (storkar sexp-db))
  (export league-db-initialize league-db-initialized? get-league-sexp-db
          get-all-leagues get-league set-league delete-league)
  (include "league-db.scm"))
