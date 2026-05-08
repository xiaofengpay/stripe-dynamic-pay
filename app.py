from flask import Flask, render_template, request, redirect
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def get_product_name(amount):
    amount = int(amount)
    # 吉祥数字特殊处理
    special = {
        520: "520爱心特别版数字艺术作品",
        666: "666顺顺利利数字艺术作品",
        888: "888吉祥如意数字艺术作品",
        999: "999至尊限量数字艺术作品",
        1314: "1314一生一世数字艺术作品",
        5200: "5200超级爱心数字艺术作品",
        6666: "6666大吉大利数字艺术作品",
        8888: "8888超级吉祥数字艺术作品",
    }
    if amount in special:
        return special[amount]
    
    # 普通金额按区间
    if 100 <= amount <= 499:
        return f"精选数字艺术作品 ¥{amount}元"
    elif 500 <= amount <= 999:
        return f"高级数字艺术作品 ¥{amount}元"
    elif 1000 <= amount <= 2999:
        return f"珍藏数字艺术作品 ¥{amount}元"
    elif 3000 <= amount <= 5999:
        return f"高端定制数字艺术作品 ¥{amount}元"
    elif 6000 <= amount <= 10000:
        return f"至尊收藏级数字艺术作品 ¥{amount}元"
    else:
        return f"数字艺术作品 ¥{amount}元"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount or not amount.isdigit():
            return "请输入正确金额", 400
        
        amount = int(amount)
        if amount < 100 or amount > 10000:
            return "金额必须在 100~10000 元之间", 400
        
        product_name = get_product_name(amount)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card", "alipay", "wechat_pay"],
                line_items=[{
                    "price_data": {
                        "currency": "cny",
                        "product_data": {
                            "name": product_name,
                        },
                        "unit_amount": amount * 100,   # 转为分
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://你的域名.com/success",   # 后面改成你自己的
                cancel_url="https://你的域名.com/",
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return str(e), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
