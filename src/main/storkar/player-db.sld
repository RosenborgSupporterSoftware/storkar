(define-library (storkar player-db)
  (import (chibi) (chibi filesystem) (chibi config)
          (presto config) (presto alist) (presto fileutils))
  (export player-db-initialize player-db-initialized? get-players get-player)
  (include "player-db.scm"))
