# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.http import Http404

from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination


class JSONResponse(HttpResponse):
    """
	An HttpResponse that renders its content into JSON.
	"""

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SetPaginationItemsLista(PageNumberPagination):
    page_size = 1000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        queryset = Product.objects.all()

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price=price)
        stock = self.request.query_params.get('stock', None)
        if stock is not None:
            queryset = queryset.filter(stock=stock)

        queryset = queryset.order_by('name')

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        product = []
        for list_elt in request.data:
            existe = Product.objects.filter(id=list_elt.get('id'))

            if existe.count() > 0:
                existe.update(**list_elt)
            else:
                Product.objects.create(**list_elt)

            product.append(list_elt.get('id'))
        results = Product.objects.filter(id__in=product)
        output_serializer = ProductSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            self.perform_destroy(instance)
            # existe = Product.objects.get(id=request.data.get('id'))
            # self.perform_destroy(existe)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        queryset = Order.objects.all()

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        date_time = self.request.query_params.get('date_time', None)
        if date_time is not None:
            queryset = queryset.filter(date_time=date_time)

        queryset = queryset.order_by('id')

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        order = []
        for list_elt in request.data:
            existe = Order.objects.filter(id=list_elt.get('id'))

            if existe.count() > 0:
                existe.update(**list_elt)
            else:
                Order.objects.create(**list_elt)

            order.append(list_elt.get('id'))
        results = Order.objects.filter(id__in=order)
        output_serializer = OrderSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderDetailViewSet(ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        queryset = OrderDetail.objects.all()

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        date_time = self.request.query_params.get('date_time', None)
        if date_time is not None:
            queryset = queryset.filter(date_time=date_time)

        queryset = queryset.order_by('id')

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        orderdetail = []
        for list_elt in request.data:
            existe = OrderDetail.objects.filter(id=list_elt.get('id'))

            if existe.count() > 0:
                existe.update(**list_elt)
            else:
                OrderDetail.objects.create(**list_elt)

            orderdetail.append(list_elt.get('id'))
        results = OrderDetail.objects.filter(id__in=orderdetail)
        output_serializer = OrderDetailSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
