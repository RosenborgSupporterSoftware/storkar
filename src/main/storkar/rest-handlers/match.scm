(import (chibi)
        (storkar match-db)
        (storkar sexp-db-rest-wrapper))

(define *rest-wrapper* #f)

(define (initialize)
  (if (not (match-db-initialized?))
      (match-db-initialize))
  (set! *rest-wrapper* (make-sexp-db-rest-wrapper "/rest/match" (get-match-sexp-db)))
  #t)

(define (get-rest-path)
  (*rest-wrapper* 'get-rest-path))

(define (rest-request request)
  (*rest-wrapper* 'handle request))

