(import (chibi)
        (storkar league-db)
        (storkar sexp-db-rest-wrapper))

(define *rest-wrapper* #f)

(define (initialize)
  (if (not (league-db-initialized?))
      (league-db-initialize))
  (set! *rest-wrapper* (make-sexp-db-rest-wrapper "/rest/league" (get-league-sexp-db)))
  #t)

(define (get-rest-path)
  (*rest-wrapper* 'get-rest-path))

(define (rest-request request)
  (*rest-wrapper* 'handle request))
