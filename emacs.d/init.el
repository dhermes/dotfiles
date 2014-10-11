;; From http://bzg.fr/emacs-strip-tease.html
;; Prevent the cursor from blinking
(blink-cursor-mode 0)
;; Don't use messages that you don't read
(setq initial-scratch-message "")
(setq inhibit-startup-message t)

;; Turn on mark highlighting

(setq transient-mark-mode t)

;; Window management

(defun prev-window ()
  (interactive)
  (other-window -1))

(global-set-key (kbd "M-o") 'other-window)
(global-set-key (kbd "M-i") 'prev-window)

;; Show column-number in the mode line
(column-number-mode 1)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Python setup
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(add-to-list 'load-path "~/.emacs.d/")

(require 'ipython)
(require 'python-mode)
(add-to-list 'auto-mode-alist '("\\.py\\'" . python-mode))

(require 'auto-complete)
(global-auto-complete-mode t)

(fset 'py-execute-line
   "\C-a\C-@\C-e\C-c\C-r")
(global-set-key (kbd "C-c C-j") 'py-execute-line)

;; Mini-buffer customization
(require 'ido)
(setq ido-enable-flex-matching t)
  (setq ido-everywhere t)
  (ido-mode 1)

;; Colors
(require 'color-theme)
(color-theme-initialize)
(color-theme-tty-dark)

;; Line specific python rules
(require 'column-marker)
(add-hook 'python-mode-hook (lambda () (interactive) (column-marker-1 80)))
(add-hook 'javascript-mode-hook (lambda () (interactive) (column-marker-1 80)))
(add-hook 'latex-mode-hook (lambda () (interactive) (column-marker-1 80)))

;; Require newline
(setq require-final-newline t)

;; NO BACKUPS
(setq make-backup-files nil)

;; PBPASTE
;; http://www.lingotrek.com/2010/12/integrate-emacs-with-mac-os-x-clipboard.html
(when (eq system-type 'darwin)
  (defun mac-copy ()
  (shell-command-to-string "pbpaste"))

  (defun mac-paste (text &optional push)
  (let ((process-connection-type nil))
  (let ((proc (start-process "pbcopy-process" "*Messages*" "pbcopy")))
  (process-send-string proc text)
  (process-send-eof proc))))

  (setq interprogram-cut-function 'mac-paste)
  (setq interprogram-paste-function 'mac-copy)
)

;; TRAILING WHITESPACE
(add-hook 'before-save-hook 'delete-trailing-whitespace)

;; PYLINT
(autoload 'python-pylint "python-pylint")
(autoload 'pylint "python-pylint")

;; http://hugoheden.wordpress.com/2009/03/08/copypaste-with-emacs-in-terminal/
;; I prefer using the "clipboard" selection (the one the
;; typically is used by c-c/c-v) before the primary selection
;; (that uses mouse-select/middle-button-click)
(setq x-select-enable-clipboard t)

;; If emacs is run in a terminal, the clipboard- functions have NO
;; effect. Instead, we use of xsel, see
;; http://www.vergenet.net/~conrad/software/xsel/ -- "a command-line
;; program for getting and setting the contents of the X selection"
(when (eq system-type 'gnu/linux)
  (unless window-system
    (when (getenv "DISPLAY")
      ;; Callback for when user cuts
      (defun xsel-cut-function (text &optional push)
        ;; Insert text to temp-buffer, and "send" content to xsel stdin
        (with-temp-buffer
          (insert text)
          ;; I prefer using the "clipboard" selection (the one the
          ;; typically is used by c-c/c-v) before the primary selection
          ;; (that uses mouse-select/middle-button-click)
          (call-process-region (point-min) (point-max) "xsel" nil 0 nil "--clipboard" "--input")))
      ;; Call back for when user pastes
      (defun xsel-paste-function()
        ;; Find out what is current selection by xsel. If it is different
        ;; from the top of the kill-ring (car kill-ring), then return
        ;; it. Else, nil is returned, so whatever is in the top of the
        ;; kill-ring will be used.
        (let ((xsel-output (shell-command-to-string "xsel --clipboard --output")))
          (unless (string= (car kill-ring) xsel-output)
             xsel-output )))
      ;; Attach callbacks to hooks
      (setq interprogram-cut-function 'xsel-cut-function)
      (setq interprogram-paste-function 'xsel-paste-function)
      ;; Idea from
      ;; http://shreevatsa.wordpress.com/2006/10/22/emacs-copypaste-and-x/
      ;; http://www.mail-archive.com/help-gnu-emacs@gnu.org/msg03577.html
    )
  )
)

;; BEGIN: Make sure we never have tabs, only space.
;; http://www.emacswiki.org/emacs/NoTabs
(setq-default indent-tabs-mode nil)
;; END: Make sure we never have tabs, only space.

;; BEGIN: Make things like eshell respect ANSI color.
;; http://www.emacswiki.org/emacs/AnsiColor
(add-hook 'shell-mode-hook 'ansi-color-for-comint-mode-on)
;; This removes colors from eshell:
(add-hook 'eshell-preoutput-filter-functions
          'ansi-color-filter-apply)
;; This correctly prints colors in eshell but is said to be slow:
;; (add-hook 'eshell-preoutput-filter-functions
;;           'ansi-color-apply)
;; END: Make things like eshell respect ANSI color.

(require 'cuda-mode)
(add-to-list 'auto-mode-alist '("\\.cu\\'" . cuda-mode))

;; BEGIN: Org-Mode init.
;; See http://orgmode.org/worg/org-tutorials/orgtutorial_dto.html
(require 'org)
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(setq org-log-done t)
;; END: Org-Mode init.
