(define *initialized* #f)
(define *basepath* "data/leagues")
(define *league-db* '())

(define (league-db-initialized?)
  *initialized*)

(define (league-db-initialize)
  (if (not *initialized*)
      (set! *league-db* (make-sexp-db *basepath*)))
  (set! *initialized* #t)
  #t)

(define (get-league-sexp-db)
  *league-db*)

(define (get-all-leagues)
  (*league-db* 'get-all))

(define (get-league uuid)
  (*league-db* 'get uuid))

(define (set-league uuid league)
  (*league-db* 'set uuid league))

(define (delete-league uuid)
  (*league-db* 'delete uuid))
