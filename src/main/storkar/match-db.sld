(define-library (storkar match-db)
  (import (chibi)
          (storkar sexp-db))
  (export match-db-initialize match-db-initialized? get-match-sexp-db
          get-all-matches get-match set-match delete-match)
  (include "match-db.scm"))
