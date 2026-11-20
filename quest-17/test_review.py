"""プルリクエスト #58 のテストです。このファイルは編集しないでください。

  python test_review.py          （ステージ2）
  python test_review.py --nit    （ステージ3）
"""
import base64
import sys

from points import describe, points, refund_points

failures = []
if points(5) != 3 or points(3) != 2 or points(7) != 4:
    failures.append("points() が変わっています。前は正しく動いていました。直すのは blocking のものだけです。")
if describe(5) != "A 5-dollar lunch gives 3 points.":
    failures.append("describe() が変わっています。そのコメントは blocking ではありませんでした。")
if refund_points(5) != -3:
    failures.append(f"refund_points(5) が {refund_points(5)} を返します。blocking のコメントをもう一度読みましょう。")

if failures:
    for f in failures:
        print("FAILED:", f)
    sys.exit(1)
print("すべてのテストに合格しました。blocking のコメントを直せました！")
print("Code word:", base64.b64decode("Z2F2ZWw=").decode())

if "--nit" in sys.argv:
    print()
    one, many = describe(1), describe(7)
    if one != "A 1-dollar lunch gives 1 point.":
        print(f"FAILED: describe(1) の結果: {one!r}。Kaito の nit をもう一度読みましょう。")
        sys.exit(1)
    if many != "A 7-dollar lunch gives 4 points.":
        print(f"FAILED: describe(7) の結果: {many!r}。単語を変えるのは、1のときだけです。")
        sys.exit(1)
    print("nit も片づきました。Kaito も喜ぶでしょう！")
    print("Code word (nit):", base64.b64decode("cG9saXNo").decode())
