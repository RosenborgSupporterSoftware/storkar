; TODO:
; - consirder implementing a sync function that checks modification time against
;   previous dataset load time and reloads objects that are updated on file...

(define (load-sexp-objects path)
  (let iter ((files (directory-files path))
             (objects '()))
    (cond ((null? files)
            objects)
          (else
            (let ((file (path-join path (car files))))
              (cond ((file-regular? file)
                      (let ((id (basename (car files)))
                            (data (with-input-from-file file read)))
                        (iter (cdr files) (cons (cons id data) objects))))
                    (else
                      (iter (cdr files) objects))))))))

(define (display/pretty object)
  (display "(")
  (display (car object))
  (let iter ((obj (cdr object)))
    (cond ((null? obj)
            (display ")\n"))
          (else
            (display "\n ")
            (display (car obj))
            (iter (cdr obj))))))

(define (make-sexp-db directory)
  (let ((db (load-sexp-objects directory))
        (path directory))

    (define (get-path uuid)
      (path-join directory (string-append uuid ".sexp")))

    (define (get-all)
      (let iter ((objs db) (ls '()))
        (cond ((null? objs) ls)
              (else
                (iter (cdr objs) (cons (cdr (car objs)) ls))))))

    (define (del-object uuid)
      (let ((path (get-path uuid)))
        (if (file-exists? path) (delete-file path)))
      (set! db (alist-unlink db uuid)))

    (define (set-object uuid object)
      (del-object uuid)
      (set! db (cons (cons uuid object) db))
      (with-output-to-file (get-path uuid) (lambda () (display/pretty object))))

    (define (get-object uuid)
      (cond ((string=? uuid "new")
              `(("uuid" . ,(gen-uuid))))
            (else
              (let ((data (assoc uuid db)))
                (if (pair? data) (cdr data) #f)))))

    (lambda (dispatch . args)
      (cond ((eq? dispatch 'get-all)
              (get-all))
            ((eq? dispatch 'delete)
              (del-object (car args)))
            ((eq? dispatch 'set)
              (set-object (car args) (cadr args)))
            ((eq? dispatch 'get)
              (get-object (car args)))
            (else
              (display "sexp-db: unknown dispatch " (current-error-port))
              (display dispatch (current-error-port))
              (display ".\n" (current-error-port))
              #f)))))

