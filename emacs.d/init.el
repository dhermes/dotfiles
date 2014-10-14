(add-to-list 'load-path "~/.emacs.d/")

;; Prevent vertical window splitting.
(setq split-height-threshold nil)
(setq split-width-threshold 75)

;; From http://bzg.fr/emacs-strip-tease.html
;; Prevent the cursor from blinking
(blink-cursor-mode 0)
;; Don't use messages that you don't read
(setq initial-scratch-message "")
(setq inhibit-startup-message t)

;; Turn on mark highlighting
(setq transient-mark-mode t)

;; Put white-marker in 80th column (if it exists).
(require 'column-marker)
(add-hook 'javascript-mode-hook (lambda () (interactive) (column-marker-1 80)))
(add-hook 'latex-mode-hook (lambda () (interactive) (column-marker-1 80)))

;; Window management

(defun prev-window ()
  (interactive)
  (other-window -1))

(global-set-key (kbd "M-o") 'other-window)
(global-set-key (kbd "M-i") 'prev-window)

;; Show column-number in the mode line
(column-number-mode 1)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; BEGIN: Python setup
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; H/T http://stackoverflow.com/a/21905123/1068170
;; trying ipython tab completion: that works :)
(setq
 python-shell-interpreter "ipython"
 python-shell-interpreter-args ""
 python-shell-prompt-regexp "In \\[[0-9]+\\]: "
 python-shell-prompt-output-regexp "Out\\[[0-9]+\\]: "
 python-shell-completion-setup-code
     "from IPython.core.completerlib import module_completion"
 python-shell-completion-module-string-code
     "';'.join(module_completion('''%s'''))\n"
 python-shell-completion-string-code
     "';'.join(get_ipython().Completer.all_completions('''%s'''))\n")

;; Hook for code folding.
(add-hook 'python-mode-hook 'hs-minor-mode)

(fset 'py-launch-interpreter
   "\C-c\C-p")
(global-set-key (kbd "C-c !") 'py-launch-interpreter)
(fset 'py-execute-line
   "\C-a\C-@\C-e\C-c\C-r")
(global-set-key (kbd "C-c C-j") 'py-execute-line)

;; Put white-marker in 80th column (if it exists).
(add-hook 'python-mode-hook (lambda () (interactive) (column-marker-1 80)))

;; H/T: http://www.emacswiki.org/emacs/AutoIndentation
;; Enter key executes newline-and-indent
(defun set-newline-and-indent ()
  "Map the return key with `newline-and-indent'"
  (local-set-key (kbd "RET") 'newline-and-indent))
(add-hook 'python-mode-hook 'set-newline-and-indent)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; END: Python setup
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(require 'auto-complete)
(global-auto-complete-mode t)

;; Mini-buffer customization
(require 'ido)
(setq ido-enable-flex-matching t)
  (setq ido-everywhere t)
  (ido-mode 1)

;; Colors
(add-to-list 'custom-theme-load-path "~/.emacs.d/themes")
(load-theme 'tty-dark t)

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

;; BEGIN: Org-Mode init.
;; See http://orgmode.org/worg/org-tutorials/orgtutorial_dto.html
(require 'org)
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(setq org-log-done t)
;; END: Org-Mode init.
