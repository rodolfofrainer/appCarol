from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json

from .forms import CreateNewItemForm, CreateNewMarketForm, WageForm, ItemsCalculateForm
from .models import MarketCreatedModel, ItemCreatedModel, UserProfileModel
from .serializers import ItemsSerializer


class BasePageView(View):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {'form': ItemsCalculateForm(request=self.request)}

        items_set = set()
        queryset = ItemCreatedModel.objects.filter(
            market_id__user_id=self.request.user.id)
        for item in queryset:
            items_set.add(item.name)

        items_list = sorted(list(items_set))

        if len(items_list) < 1:
            items_list = []
        context['items_list'] = items_list
        return context
    
    def get_items_list(self):
        # Retrieve or calculate your items_list here
        items_set = set()
        queryset = ItemCreatedModel.objects.filter(
            market_id__user_id=self.request.user.id)
        for item in queryset:
            items_set.add(item.name)
        items_list = sorted(list(items_set))
        if len(items_list) < 1:
            items_list = []
        print(items_list)
        return items_list
    
    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        items_list = self.get_items_list()
        request.session['items_list'] = items_list
        context = self.get_context_data()
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ComparisonPageView(View):
    template_name = 'comparison.html'
    
    def get(self, request):
        # Retrieve the items_list from the session
        items_list = request.session.get('items_list', [])

        # You can now use the items_list in your template or logic
        context = {'items_list': items_list}
        print(request.session.keys())
        return render(request, self.template_name, context)
    
    def post(self, request):
        if request.method == 'POST':
            # Get the shopping list from the request
            data = json.loads(request.body)
            shopping_list = data.get('shoppingList', [])

            # Perform calculations or processing with the shopping list
            results = self.calculate_results(shopping_list)

            # Return the results as JSON response
            return JsonResponse({'results': results})
        else:
            return JsonResponse({'error': 'Invalid request method'})

    def calculate_results(self, shopping_list):
        # Perform calculations or processing with the shopping list
        results = []

        for item in shopping_list:
            # Calculate something based on each item
            # Append the result to the results list
            result = f"Processed item: {item}"
            results.append(result)

        return results

@method_decorator(login_required, name='dispatch')
class MarketPageView(View):
    template_name = 'marketCreation.html'
    form_class = CreateNewMarketForm

    def get_context_data(self, **kwargs):
        context = {'form': self.form_class(), }
        context['list_of_markets'] = MarketCreatedModel.objects.filter(
            user_id=self.request.user.id)
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'distance': 0, 'favorite': 0})
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user
            item.save()
            messages.success(request, f'Market created successfully!')
            return redirect('market_page')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

    def favorite_market(self, pk):
        market = MarketCreatedModel.objects.get(pk=pk)
        market.favorite = True
        market.save()
        return redirect('market_page')

    def unfavorite_market(self, pk):
        market = MarketCreatedModel.objects.get(pk=pk)
        market.favorite = True
        market.save()
        return redirect('market_page')


@method_decorator(login_required, name='dispatch')
class CreateItemView(View):
    template_name = 'itemCreation.html'
    form_class = CreateNewItemForm
    context = {}

    def get_context_data(self, **kwargs):
        try:
            qs = ItemCreatedModel.objects\
                .filter(market_id__user_id=self.request.user.id)\
                .select_related('market_id')
            list_of_markets = {i.market_id: i for i in qs}
        except IndexError:
            list_of_markets = {}

        self.context['list_of_markets'] = list_of_markets
        return self.context

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user, initial={'price': 0.00})
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        form.fields['market_id'].queryset = MarketCreatedModel.objects.filter(
            user_id=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.name = item.name.lower()
            item.user_id = request.user.id
            item.save()
            messages.success(request, f'Item created successfully!')
            return redirect('create_item')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def delete_item(self, pk:int):
        user_id = ItemCreatedModel.objects.filter(market_id__user_id = self.user.id)
        if user_id:
            product = get_object_or_404(ItemCreatedModel, pk=pk)
            product.delete()
            return redirect('create_item')
        else:
            messages.warning(self,'Something went wrong')
            return redirect('home')


@method_decorator(login_required, name='dispatch')
class myWagePageView(View):
    template_name = 'wageHour.html'
    form_class = WageForm

    def get_context_data(self, **kwargs):
        user_wage = UserProfileModel.objects.get(user=self.request.user).wage
        context = {'wage': user_wage}
        return context

    def get(self, request, *args, **kwargs):
        user_profile = UserProfileModel.objects.get(user=request.user)
        initial_data = {'wage': user_profile.wage}
        form = self.form_class(initial=initial_data)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_profile = UserProfileModel.objects.get(user=request.user)

        if form.is_valid():
            item = form.save(commit=False)
            user_profile.wage = item.wage
            user_profile.save()
            messages.success(request, 'Wage updated successfully!')
            return redirect('mywage_page')

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)


class ProductListView(View):
    @api_view(['GET'])
    def display_all_items(request):
        queryset = ItemCreatedModel.objects.filter(
            market_id__user_id=request.user.id)
        serializer = ItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    def display_item(self, pk):
        product = get_object_or_404(ItemCreatedModel, pk=pk)
        if self.method == 'GET':
            serializer = ItemsSerializer(product)
            return Response(serializer.data)
        elif self.method == 'POST':
            serializer = ItemsSerializer(data=self.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif self.method == 'PUT':
            serializer = ItemsSerializer(product, data=self.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.method == 'DELETE':
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
