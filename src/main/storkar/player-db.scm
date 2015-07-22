(define *initialized* #f)
(define *basepath* "data/players")
(define *players* '())

; FIXME: check filetimestamp with load-time to see if there are updated
; player data files on disk? (to consider)

(define (update-player uuid data)
  (set! *players* (update-alist *players* uuid data)))

(define (load-players path)
  (let iter ((files (directory-files path)))
    (cond ((not (null? files))
            (let ((file (path-join path (car files))))
              (if (file-regular? file)
                  (let ((id (basename (car files)))
                        (data (with-input-from-file file read)))
                    ;(display "loaded player: ")
                    ;(display (cdr (assoc "name" data)))
                    ;(display " - ")
                    ;(display (cdr (assoc "uuid" data)))
                    ;(newline)
                    (update-player id data))))
            (iter (cdr files))))))

(define (player-db-initialized?)
  *initialized*)

(define (player-db-initialize)
  (cond ((not *initialized*)
          (set! *initialized* #t)
          (load-players *basepath*)))
  #t)

(define (get-all-players)
  (let iter ((players '())
             (stored *players*))
    (cond ((null? stored)
            (reverse players))
          (else
             (iter (cons (cdr (car stored)) players) (cdr stored))))))

(define (get-player uuid)
  (cond ((string=? uuid "new")
          `(("uuid" . ,(gen-uuid))))
        (else
          (let ((data (assoc uuid *players*)))
            (if (pair? data) (cdr data) #f)))))

(define (set-player uuid player)
  ;(display uuid) (newline)
  ;(display player) (newline)
  (let ((path (path-join *basepath* (string-append uuid ".sexp"))))
    (if (file-exists? path) (delete-file path))
    (with-output-to-file
      path
      (lambda () (display player) (newline)))) ; FIXME: prettify sexp as well
  (set! *players* (update-alist *players* uuid player)))

(define (delete-player uuid)
  (let ((path (path-join *basepath* (string-append uuid ".sexp"))))
    (if (file-exists? path) (delete-file path)))
  (set! *players* (alist-unlink *players* uuid)))

