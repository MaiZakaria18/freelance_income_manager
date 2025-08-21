# services/uncategorized_expenses.py
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from expenses.models import Expenses
from decimal import Decimal

def get_uncategorized_expenses(budget_plan, search=None, page=1, page_size=10):
    qs = Expenses.objects.filter(
        budget_plan=budget_plan,
        category__isnull=True
    )

    if search:
        qs = qs.filter(Q(tip__icontains=search) | Q(amount__icontains=search))

    qs = qs.order_by('-transaction_date')

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    expenses_list = [{
        "id": e.id,
        "transaction_date": e.transaction_date,
        "amount": float(e.amount),
        "tip": e.tip
    } for e in page_obj]

    total_uncategorized = qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    return {
        "pagination": {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "page_size": page_size
        },
        "expenses": expenses_list,
        "total_uncategorized": total_uncategorized
    }
