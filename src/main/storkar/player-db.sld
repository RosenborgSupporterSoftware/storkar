(define-library (storkar player-db)
  (import (chibi)
          (storkar sexp-db))
  (export player-db-initialize player-db-initialized? get-player-sexp-db
          get-all-players get-player set-player delete-player)
  (include "player-db.scm"))
