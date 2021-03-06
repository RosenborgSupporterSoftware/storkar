(import (chibi)
        (storkar team-db)
        (storkar sexp-db-rest-wrapper))

(define *rest-wrapper* #f)

(define (initialize)
  (if (not (team-db-initialized?))
      (team-db-initialize))
  (set! *rest-wrapper* (make-sexp-db-rest-wrapper "/rest/team" (get-team-sexp-db)))
  #t)

(define (get-rest-path)
  (*rest-wrapper* 'get-rest-path))

(define (rest-request request)
  (*rest-wrapper* 'handle request))
