# Memo from the delivery team

Hi Haruka! Here is what we know about `delivery_time()`. Please make a real page from it.

- `distance`: how far we drive, in **kilometers**.
- `speed`: how fast the car goes, in **kilometers per hour**. We usually drive at 40.
- `stop`: extra time for stops on the way (parking, stairs...), in **hours**. Usually there is none.
- It gives back the time of the whole delivery, in **hours**. `2.0` means two hours.
- If `speed` is 0 or less, it stops with a `ValueError`. (A car that does not move never arrives!)

Thanks! — The delivery team
