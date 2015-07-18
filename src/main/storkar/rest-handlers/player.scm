(import (chibi)
        (storkar player-db))

(define (initialize)
  (if (not (player-db-initialized?))
      (player-db-initialize))
  #t)

(define (string-starts-with prefix str)
  (let ((plen (string-length prefix))
        (slen (string-length str)))
    (cond ((>= slen plen)
            (string=? prefix (substring str 0 plen)))
          (else
            #f))))

(define (get-request request)
  (cond ((string-starts-with "/rest/player" (request 'get-path))
          (get-players))
        (else
          '())))

(define (put-request request)
  #f)

(define (post-request request)
  #f)

(define (get-rest-path)
  "/rest/player")

