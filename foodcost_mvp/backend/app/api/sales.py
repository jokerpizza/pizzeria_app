from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from datetime import date, datetime, timedelta
from collections import defaultdict

router = APIRouter()

@router.get("/daily")
def daily_sales(db: Session = Depends(get_db)):
    today = date.today()
    start_cur = today - timedelta(days=today.weekday())
    end_cur = today
    length = (end_cur - start_cur).days
    end_prev = start_cur - timedelta(days=1)
    start_prev = end_prev - timedelta(days=length)

    def get_sums(start, end):
        sales = defaultdict(float)
        rows = db.query(models.Order.finished_at, models.OrderItem.price, models.OrderItem.quantity)\
            .join(models.OrderItem)\
            .filter(models.Order.finished_at != None)\
            .filter(models.Order.finished_at >= datetime.combine(start, datetime.min.time()))\
            .filter(models.Order.finished_at <= datetime.combine(end, datetime.max.time()))\
            .all()
        for dt, price, qty in rows:
            d = dt.date()
            sales[d] += price * qty
        return sales

    cur_sales = get_sums(start_cur, end_cur)
    prev_sales = get_sums(start_prev, end_prev)

    data = []
    for i in range((end_cur - start_cur).days + 1):
        d_cur = start_cur + timedelta(days=i)
        d_prev = start_prev + timedelta(days=i)
        data.append({
            "day": d_cur.strftime("%a"),
            "current": round(cur_sales.get(d_cur, 0.0), 2),
            "previous": round(prev_sales.get(d_prev, 0.0), 2)
        })
    return data

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    def get_stats(start, end):
        rows = db.query(models.Order.id, models.OrderItem.price, models.OrderItem.quantity)\
            .join(models.OrderItem)\
            .filter(models.Order.finished_at != None)\
            .filter(models.Order.finished_at >= datetime.combine(start, datetime.min.time()))\
            .filter(models.Order.finished_at <= datetime.combine(end, datetime.max.time()))\
            .all()
        total = sum(price * qty for _, price, qty in rows)
        order_ids = {oid for oid, _, _ in rows}
        return total, len(order_ids)

    total_today, count_today = get_stats(today, today)
    total_week, count_week = get_stats(start_week, today)
    total_month, count_month = get_stats(start_month, today)
    return {
        "today": round(total_today, 2),
        "week": round(total_week, 2),
        "month": round(total_month, 2),
        "docsToday": count_today,
        "docsWeek": count_week,
        "docsMonth": count_month
    }
