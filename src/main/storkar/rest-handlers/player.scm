(import (chibi)
        (storkar player-db)
        (storkar sexp-db-rest-wrapper))

(define *rest-wrapper* #f)

(define (initialize)
  (if (not (player-db-initialized?))
      (player-db-initialize))
  (set! *rest-wrapper* (make-sexp-db-rest-wrapper "/rest/player" (get-player-sexp-db)))
  #t)

(define (get-rest-path)
  (*rest-wrapper* 'get-rest-path))

(define (rest-request request)
  (*rest-wrapper* 'handle request))
