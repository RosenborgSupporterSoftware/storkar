(define *initialized* #f)
(define *basepath* "data/matches")
(define *match-db* '())

(define (match-db-initialized?)
  *initialized*)

(define (match-db-initialize)
  (if (not *initialized*)
      (set! *match-db* (make-sexp-db *basepath*)))
  (set! *initialized* #t)
  #t)

(define (get-match-sexp-db)
  *match-db*)

(define (get-all-matches)
  (*match-db* 'get-all))

(define (get-match uuid)
  (*match-db* 'get uuid))

(define (set-match uuid match)
  (*match-db* 'set uuid match))

(define (delete-match uuid)
  (*match-db* 'delete uuid))
