from django.shortcuts import render
from django.http import JsonResponse
from .models import Booth, Transaction, Institution
from .forms import TransactionForm
from django.contrib import messages
from django.views import View
import logging
from django.db.models import Sum, Count

logger = logging.getLogger(__name__)


def dashboard(request):
    transactions = Transaction.objects.all()
    institutions = Institution.objects.all()

    # Calculate the total limit value
    total_limit = institutions.aggregate(total_limit=Sum("limit"))["total_limit"] or 0

    for institution in institutions:
        total_spent = (
            Transaction.objects.filter(service=institution).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        institution.remaining_value = institution.limit - total_spent
        institution.service_revenue = total_spent * institution.revenue
    total_service_revenue = sum(institution.service_revenue for institution in institutions)

    booth_id = request.GET.get("booth_id")
    service_id = request.GET.get("service_id")

    if booth_id:
        try:
            booth = Booth.objects.get(id=booth_id)
            services_data = [
                {
                    "id": service.id,
                    "name": service.name,
                    "revenue": float(service.revenue),
                }
                for service in booth.services.all()
            ]

            transactions = Transaction.objects.filter(booth=booth)
            if service_id:
                transactions = transactions.filter(service_id=service_id)

            transactions_data = [
                {
                    "id": f"WB{transaction.id:07d}",
                    "service": transaction.service.name,
                    "amount": float(transaction.amount),
                    "taxamount": float(
                        (transaction.amount)
                        - (transaction.amount * 0.15)
                    ),
                }
                for transaction in transactions
            ]

            # Calculate institution transaction counts for the bar chart
            institutions_transactions = (
                transactions.values("service__name")
                .annotate(transaction_count=Count("id"))
                .order_by("-transaction_count")
            )

            institutions_transactions_data = [
                {
                    "institution": item["service__name"],
                    "transaction_count": item["transaction_count"],
                }
                for item in institutions_transactions
            ]

            data = {
                "location": booth.location,
                "services": services_data,
                "transactions": transactions_data,
                "institutions_transactions": institutions_transactions_data,
            }
            return JsonResponse(data)
        except Booth.DoesNotExist:
            logger.warning(f"Booth {booth_id} not found")
            return JsonResponse({"error": "Booth not found"}, status=404)
        except Exception as e:
            logger.error(f"Error processing booth {booth_id}: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)
    else:
        booths = Booth.objects.all()
        context = {
            "booths": booths,
            "transactions": transactions,
            "institutions": institutions,
            "total_limit": total_limit,
            "total_service_revenue": total_service_revenue,
        }
        return render(request, "dashboard.html", context)


class CreateTransactionView(View):
    def get(self, request):
        form = TransactionForm()
        # Get the last transaction ID and calculate the next one
        last_transaction = Transaction.objects.last()
        next_transaction_id = f"WB{(last_transaction.id + 1 if last_transaction else 1):07d}"
        return render(
            request,
            "create.html",
            {
                "form": form,
                "next_transaction_id": next_transaction_id,
            },
        )

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            transaction_id = f"WB{transaction.id:07d}"
            next_transaction_id = f"WB{(transaction.id + 1):07d}"
            messages.success(
                request, f"Transaction {transaction_id} created successfully."
            )
            # Instead of redirecting, render the same page with the new form and next_transaction_id
            new_form = TransactionForm()  # Create a new, empty form
            return render(
                request,
                "create.html",
                {
                    "form": new_form,
                    "next_transaction_id": next_transaction_id,
                },
            )
        else:
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "create.html",
                {
                    "form": form,
                },
            )


def load_services(request):
    booth_id = request.GET.get("booth_id")
    services = Institution.objects.filter(booths__id=booth_id)
    return JsonResponse(list(services.values("id", "name")), safe=False)


def booths_dashboard(request):
    booths = Booth.objects.all()
    booth_transactions = {}

    for booth in booths:
        total_amount = (
            Transaction.objects.filter(booth=booth).aggregate(total=Sum("amount"))[
                "total"
            ]
            or 0
        )
        booth_transactions[booth.name] = total_amount

    context = {
        "booth_transactions": booth_transactions,
    }
    return render(request, "booths.html", context=context)
