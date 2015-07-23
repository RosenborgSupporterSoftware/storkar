(define (do-action sexp-db verb uuid content)
  (cond ((string=? "PATCH" verb)
          (let* ((object (sexp-db 'get uuid))
                 (patched (patch-alist (if object object '()) content)))
            (sexp-db 'set uuid patched)
            patched))
        ((string=? "PUT" verb)
          (cond ((string=? "new" uuid)
                  (let ((uuid (gen-uuid)))
                    (sexp-db 'set uuid (update-alist content '("uuid" . uuid)))
                    (sexp-db 'get uuid)))
                (else
                  (let ((object (sexp-db 'get uuid))) ; FIXME: unnecessary fetch
                    (sexp-db 'set uuid content)
                    content))))
        ((string=? "GET" verb)
          (sexp-db 'get uuid))
        ((string=? "DELETE" verb)
          (sexp-db 'delete uuid))
        (else
          (display "UNHANDLED ")
          (display verb) (display " ") (display uuid) (newline)
          '()
          )))

(define (make-sexp-db-rest-wrapper rest-path sexp-db)
  (let ((db sexp-db)
        (rest-api-path rest-path))

    (define (get-rest-path)
      rest-api-path)

    (define (get-db-path)
      (db 'get-path))

    (define (handle request)
      (let ((pathelts (string-split (request 'get-path) #\/)))
        (cond ((and (equal? rest-api-path (request 'get-path))
                    (string=? "GET" (request 'get-method)))
                (db 'get-all))
              ((= 4 (length pathelts))
                (do-action db (request 'get-method) (list-ref pathelts 3)
                           (if (request 'get-body)
                               (json->sexp (request 'get-body))
                               '())))
              (else
                '())))) ; FIXME: respond with error

    (lambda (dispatch . args)
      (cond ((eq? dispatch 'get-rest-path)
              (get-rest-path))
            ((eq? dispatch 'get-db-path)
              (get-db-path))
            ((eq? dispatch 'handle)
              (handle (car args)))
            (else
              (display "sexp-db-rest-wrapper dispatch falthrough: "
                       (current-error-port))
              (display dispatch (current-error-port))
              (display ".\n" (current-error-port))
              )))))

