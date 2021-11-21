import json

from django.views import View
from django.http import JsonResponse
from users.models import User
from ledgers.models import Ledger
from users.userauth import user_auth


class LedgerView(View):
    # Create a ledger
    @user_auth
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            ledger_list = Ledger.objects.filter(user = user.id)[::-1]

            if Ledger.objects.filter(user = user.id).exists() and len(ledger_list) >= 1:
                Ledger.objects.create(
                    note          = data['note'],
                    income        = data['income'],
                    expense       = data['expense'],
                    total_income  = ledger_list[0].total_income + data['income'],
                    total_expense = ledger_list[0].total_expense + data['expense'],
                    category      = data['category'],
                    user          = User.objects.get(id=user.id)
                )

            else:
                Ledger.objects.create(
                    note          = data['note'],
                    income        = data['income'],
                    expense       = data['expense'],
                    total_income  = data['income'],
                    total_expense = data['expense'],
                    category      = data['category'],
                    user          = User.objects.get(id = user.id)
                )

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    # Read all the ledger
    @user_auth
    def get(self, request):
        user = request.user

        if not Ledger.objects.filter(user = user.id, is_removed = False).exists():
            return JsonResponse({'message' : 'Ledger Does Not Exist'}, status = 404)

        ledger_list = Ledger.objects.filter(user = user.id, is_removed = False)

        result = []

        for ledger in ledger_list:
            result.append(
                {
                    'note'          : ledger.note,
                    'income'        : ledger.income,
                    'expense'       : ledger.expense,
                    'total_income'  : ledger.total_income,
                    'total_expense' : ledger.total_expense,
                    'category'      : ledger.category
                })

        return JsonResponse({'message' : 'success', 'result' : result}, status = 200)


class DetailView(View):
    # Read a selected ledger with details
    @user_auth
    def get(self, request, post_id):
        user = request.user

        if not Ledger.objects.filter(id = post_id, user = user.id, is_removed = False).exists():
            return JsonResponse({'message' : 'Ledger Does Not Exist'}, status = 404)

        ledger = Ledger.objects.get(id = post_id, user = user.id, is_removed = False)

        result = {
                    'note'          : ledger.note,
                    'income'        : ledger.income,
                    'expense'       : ledger.expense,
                    'total_income'  : ledger.total_income,
                    'total_expense' : ledger.total_expense,
                    'category'      : ledger.category
                }

        return JsonResponse({'message' : 'success', 'result' : result}, status = 200)

# delete a selected ledger
    @user_auth
    def delete(self, request, post_id):
        user = request.user

        if not Ledger.objects.filter(id = post_id, user = user.id, is_removed = False).exists():
            return JsonResponse({'message' : 'DOES NOT EXIST'}, status = 404)

        selected_ledger               = Ledger.objects.get(id = post_id, user = user.id, is_removed = False)
        selected_ledger.is_removed    = True
        selected_ledger.save()

        return JsonResponse({'message' : 'selected ledger removed'}, status = 200)

    # Edit a selected ledger
    @user_auth
    def put(self, request, post_id):
        try:
            user = request.user

            data = json.loads(request.body)

            if not Ledger.objects.filter(id=post_id, user=user.id, is_removed = False).exists():
                return JsonResponse({'message' : 'LEDGER DOES NOT EXIST'}, status = 404)

            selected_ledger = Ledger.objects.get(id = post_id, user = user.id, is_removed = False)
            previous_ledger = Ledger.objects.get(id = (post_id-1), user = user.id, is_removed = False)
            next_ledgers = Ledger.objects.filter(user = user.id, is_removed = False)[post_id:]

            selected_ledger.note          = data['note']
            selected_ledger.income        = data['income']
            selected_ledger.expense       = data['expense']
            selected_ledger.total_income  = previous_ledger.total_income + data['income']
            selected_ledger.total_expense = previous_ledger.total_expense + data['expense']
            selected_ledger.save()

            count = 0
            for ledger in next_ledgers:
                if count == 0:
                    ledger.total_income  = selected_ledger.total_income + next_ledgers[count].income
                    ledger.total_expense = selected_ledger.total_expense + next_ledgers[count].expense
                    ledger.save()
                    count += 1
                else:
                    ledger.total_income  = next_ledgers[count-1].total_income + next_ledgers[count].income
                    ledger.total_expense = next_ledgers[count-1].total_expense + next_ledgers[count].expense
                    ledger.save()
                    count += 1

            return JsonResponse({'message' : 'EDIT SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

