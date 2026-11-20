# Postmortem: The order page was down after the v2.0 release

**Author:** @daiki-ops · **Date:** 2026-12-02 · **Status:** Done

This postmortem is **blameless**. We look at what happened and how to stop it next time.
We do not look for a person to blame.

## Summary

We announced v2.0 on December 1, and deployed it to production the next morning.
Right after the deploy, nobody could order lunch for 35 minutes. The server did not start, because the production settings still used an old setting name.

## Impact

- Nobody could order lunch from 09:12 to 09:47.
- 41 customers saw an error page. 9 customers called the support desk.
- Pre-orders from the day before were safe.

## Timeline (all times are JST)

| Time | What happened |
| --- | --- |
| 09:05 | We deployed v2.0.0 to production. |
| 09:12 | The first customer saw an error page. |
| 09:15 | @yui-dev got the first call from a customer, and told the team. |
| 09:20 | We thought the database was down, and restarted it. Nothing changed. |
| 09:31 | @kaito-m read the server log: `Error: unknown setting 'pickup'`. |
| 09:40 | We changed `pickup` to `pickup_time` in the production settings. |
| 09:47 | The server started. Customers could order again. |

## Root cause

v2.0.0 renamed the setting `pickup` to `pickup_time`. This was a **breaking change**, and it was in the CHANGELOG.
We changed the settings on the staging server, but **not** on the production server.
The production server read the old name `pickup`, and stopped.

The database was **not** the cause. We lost 11 minutes because we guessed before we read the log.

## What went well

- Pre-orders were saved, so no orders were lost.
- Yui told the team quickly.

## What went wrong

- Nobody checked the production settings before the deploy.
- We restarted the database before we read the log.

## Action items

| Action | Owner | Status |
| --- | --- | --- |
| Check for old setting names in the deploy script, and stop the deploy. | @daiki-ops | Done |
| Add "update the production settings" to the release checklist. | @haruka-m | In progress |
| Send an alert to the team when there are no orders for 10 minutes at lunch time. | TBD | Open |
| Read the server log first. Add this to the incident guide. | @misaki-w | Done |
