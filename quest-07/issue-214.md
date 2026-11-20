# Issue #214: Crash when saving a note with an accent in the title

**Labels:** `bug`, `confirmed`  
**State:** closed (duplicate)  
**Opened by:** @tomoki-s

---

**@tomoki-s** commented

I run `python notes.py save` and it crashes. The note title is "café menu".
I get this error:

    UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3

Is anyone else seeing this?

---

**@yui-dev** commented

+1

---

**@daiki-ops** commented

+1, same here. This is blocking my team.

---

**@kaito-m** commented

I think this is a Windows problem. I use macOS, so I can't reproduce it.
Maybe you should switch to Linux? :)

---

**@daiki-ops** commented

@kaito-m I'm on Linux and it also fails. Not a Windows problem.

---

**@haruka-m** commented

I found a quick fix. Try this:

    export NOTES_UNICODE=1
    python notes.py save

---

**@tomoki-s** commented

@haruka-m I tried it. Nothing changed, same error. Maybe I did it wrong?

---

**@misaki-w** (maintainer) commented

Thanks for the reports, everyone. I can reproduce this.

**Steps to reproduce:**

1. Run `python notes.py save` with a title that has an accent.
2. The tool tries to write the file as ASCII, and it fails.

**Workaround:** `NOTES_UNICODE` is not a real setting. Please don't use it.
The tool reads `NOTES_ENCODING`. Set it to `utf-8` and run the command again.

---

**@yui-dev** commented

@misaki-w That works for me. Thank you!

---

**@kaito-m** commented

Sorry about the Linux joke. Glad it's fixed for you all.

---

**@daiki-ops** commented

Any news on a real fix? We don't want to set a variable on every machine.

---

**@misaki-w** (maintainer) commented

Yes. The fix is merged into `main`. It will be in the next patch release, **2.3.1**.
(2.4.0 is the next feature release. It is planned for next month, but the fix will come before it.)

---

**@haruka-m** commented

I guessed that it was fixed in 2.3.0, but I was wrong. Thanks for being patient with me, Misaki!

---

**@misaki-w** (maintainer) commented

This is the same bug as #198, which has a longer discussion.
Closing this issue as a duplicate of #198.
Please follow #198 for updates.
