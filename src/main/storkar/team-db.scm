(define *initialized* #f)
(define *basepath* "data/teams")
(define *team-db* '())

(define (team-db-initialized?)
  *initialized*)

(define (team-db-initialize)
  (if (not *initialized*)
      (set! *team-db* (make-sexp-db *basepath*)))
  (set! *initialized* #t)
  #t)

(define (get-team-sexp-db)
  *team-db*)

(define (get-all-teams)
  (*team-db* 'get-all))

(define (get-team uuid)
  (*team-db* 'get uuid))

(define (set-team uuid team)
  (*team-db* 'set uuid team))

(define (delete-team uuid)
  (*team-db* 'delete uuid))
