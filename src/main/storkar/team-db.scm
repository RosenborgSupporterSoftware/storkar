(define *initialized* #f)
(define *basepath* "data/teams")
(define *teams* '())

; FIXME: check filetimestamp with load-time to see if there are updated
; team data files on disk? (to consider)

(define (update-team uuid data)
  (set! *teams* (update-alist *teams* uuid data)))

(define (load-teams path)
  (let iter ((files (directory-files path)))
    (cond ((not (null? files))
            (let ((file (path-join path (car files))))
              (if (file-regular? file)
                  (let ((id (basename (car files)))
                        (data (with-input-from-file file read)))
                    (display "loaded team: ")
                    (display (cdr (assoc "name" data)))
                    (display " - ")
                    (display (cdr (assoc "uuid" data)))
                    (newline)
                    (update-team id data))))
            (iter (cdr files))))))

(define (team-db-initialized?)
  *initialized*)

(define (team-db-initialize)
  (cond ((not *initialized*)
          (set! *initialized* #t)
          (load-teams *basepath*)))
  #t)

(define (get-all-teams)
  (let iter ((teams '())
             (stored *teams*))
    (cond ((null? stored)
            (reverse teams))
          (else
             (iter (cons (cdr (car stored)) teams) (cdr stored))))))

(define (get-team uuid)
  (cond ((string=? uuid "new")
          `(("uuid" . ,(gen-uuid))))
        (else
          (let ((data (assoc uuid *teams*)))
            (if (pair? data) (cdr data) #f)))))

(define (set-team uuid team)
  ;(display uuid) (newline)
  ;(display team) (newline)
  (let ((path (path-join *basepath* (string-append uuid ".sexp"))))
    (if (file-exists? path) (delete-file path))
    (with-output-to-file
      path
      (lambda () (display team) (newline)))) ; FIXME: prettify sexp as well
  (set! *teams* (update-alist *teams* uuid team)))

(define (delete-team uuid)
  (let ((path (path-join *basepath* (string-append uuid ".sexp"))))
    (if (file-exists? path) (delete-file path)))
  (set! *teams* (alist-unlink *teams* uuid)))

