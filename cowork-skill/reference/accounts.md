# Capture accounts

One account per entitlement tier. `/tutorial` asks the user which **tier** a
module is documented at (§1 of `SKILL.md`) and resolves the login from this
table. **The user is never asked to pick an account by name** — they are asked
for the tier, which is what the document states and what a reader checks their
own plan against.

| Tier | Plan name | Account | Org |
|---|---|---|---|
| 1 | Foundation | `<fill in>` | `<fill in>` |
| 2 | Control | `<fill in>` | `<fill in>` |
| 3 | Vigilance | `<fill in>` | `<fill in>` |

## No credentials in this file

It ships with a published plugin. Record only the identifier needed to pick the
right session — the passwords live wherever the rest of the test logins are
kept, and never here.

## Keeping it current

Accounts get recreated more often than tiers get renumbered, which is the whole
reason the question is worded by tier: a rotated login is a one-line edit in
this table and no change to `SKILL.md`. Add a row rather than repurposing one if
a fourth tier appears.

## The tier names

**Tier 1 = Foundation, Tier 2 = Control, Tier 3 = Vigilance.** Write the plan
name in the document, not the number — a reader recognises *Control* on their
invoice and has never seen "Tier 2". One earlier guide called Tier 2
"Lifecycle"; that is wrong, contradicts every other source, and should not be
copied forward.

## If a tier has no working account

Say so and hold the document. Do not capture on a neighbouring tier: §2 makes
the screenshots the proof of the tier the document claims, so a Foundation guide
shot on the Vigilance login promises the reader menu entries their plan will
never show them.
