(define *initialized* #f)
(define *basepath* "data/players")
(define *player-db* '())

(define (player-db-initialized?)
  *initialized*)

(define (player-db-initialize)
  (if (not *initialized*)
      (set! *player-db* (make-sexp-db *basepath*)))
  (set! *initialized* #t)
  #t)

(define (get-all-players)
  (*player-db* 'get-all))

(define (get-player uuid)
  (*player-db* 'get uuid))

(define (set-player uuid player)
  (*player-db* 'set uuid player))

(define (delete-player uuid)
  (*player-db* 'delete uuid))
