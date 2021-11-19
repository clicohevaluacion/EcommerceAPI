# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.http import Http404

import json, requests
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
            queryset = queryset.filter(name__icontains=name)
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

            if "stock" in list_elt:
                if int(list_elt["stock"]) < 0:
                    return Response({"Error": ["Ingrese un stock mayor o igual a Cero"]}, status=status.HTTP_400_BAD_REQUEST)

            if "price" in list_elt:
                if float(list_elt["price"]) < 0:
                    return Response({"Error": ["Ingrese un Precio mayor o igual a Cero"]}, status=status.HTTP_400_BAD_REQUEST)

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
            existe = OrderDetail.objects.filter(product=instance)
            if existe.count() > 0:
                return Response(
                    {"Error": ["No se puede eliminar un producto que exite en una Orden, elimine primero la Orden"]},
                    status=status.HTTP_400_BAD_REQUEST)
            self.perform_destroy(instance)
        except:
            return Response({"Error": ["No se pudo borrar el producto"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Respuesta": ["Se elimino el Producto"]}, status=status.HTTP_204_NO_CONTENT)

class MovProductView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        existe = Product.objects.filter(id=request.data["id"])
        if existe.count() > 0:
            if (existe[0].stock + int(request.data["movement"])) < 0:
                return Response({"Error": ["No hay suficiente stock"]}, status=status.HTTP_400_BAD_REQUEST)
            existe.update(stock=existe[0].stock + int(request.data["movement"]))
            return Response({"Respuesta": ["Se modifico el stock"]}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": ["No existe el Producto"]}, status=status.HTTP_400_BAD_REQUEST)

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
            with transaction.atomic():
                orderdetail = OrderDetail.objects.filter(order=instance)
                if orderdetail.count() > 0:
                    for elto in range(len(orderdetail)):
                        exiteProducto = Product.objects.filter(id=orderdetail[elto].product)
                        exiteProducto.update(stock=exiteProducto[0].stock + int(orderdetail[elto].cuantity))
                    orderdetail.delete()
                self.perform_destroy(instance)
        except:
            return Response({"Error": ["Error al eliminar la orden"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Respuesta": ["Se elimino la orden"]}, status=status.HTTP_200_OK)

    @action(detail=True)
    def get_total(self, request, pk):
        ordersdetails = OrderDetail.objects.filter(order=pk)


        if ordersdetails.count() > 0:

            countprice = 0
            for elto in range(len(ordersdetails)):
                exiteProducto = Product.objects.filter(id=ordersdetails[elto].product)

                if exiteProducto.count() > 0:
                     product = Product.objects.get(id=ordersdetails[elto].product)
                     countprice = countprice + (product.price * ordersdetails[elto].cuantity)
                else:
                    return Response({"Error": ["No existe el producto"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": ["No existe detalles de la Orden"]}, status=status.HTTP_400_BAD_REQUEST)

        content = {'price order': countprice}
        return Response(content)

    @action(detail=True)
    def get_total(self, request, pk):
        ordersdetails = OrderDetail.objects.filter(order=pk)

        if ordersdetails.count() > 0:
            sumprice = 0
            for elto in range(len(ordersdetails)):
                exiteProducto = Product.objects.filter(id=ordersdetails[elto].product)

                if exiteProducto.count() > 0:
                     product = Product.objects.get(id=ordersdetails[elto].product)
                     sumprice = sumprice + (product.price * ordersdetails[elto].cuantity)
                else:
                    return Response({"Error": ["No existe el producto"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": ["No existe detalles de la Orden"]}, status=status.HTTP_400_BAD_REQUEST)

        content = {'price order': sumprice}
        return Response(content)

    @action(detail=True)
    def get_total_usd(self, request, pk):
        ordersdetails = OrderDetail.objects.filter(order=pk)

        if ordersdetails.count() > 0:
            sumprice = 0
            for elto in range(len(ordersdetails)):
                exiteProducto = Product.objects.filter(id=ordersdetails[elto].product)

                if exiteProducto.count() > 0:
                     product = Product.objects.get(id=ordersdetails[elto].product)
                     sumprice = sumprice + (product.price * ordersdetails[elto].cuantity)
                else:
                    return Response({"Error": ["No existe el producto"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": ["No existe detalles de la Orden"]}, status=status.HTTP_400_BAD_REQUEST)

        url = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        text = url.text

        data = json.loads(text)
        casa = 0
        for elto in data:
            if elto['casa']['nombre'] == 'Dolar Blue':
                casa = float(elto['casa']['venta'].replace(",", "."))
        if casa == 0:
            return Response({"Error": ["No se pudo encontrar el precio del Dolar Blue"]}, status=status.HTTP_404_NOT_FOUND)


        content = {'price order USD': round(sumprice / casa, 2)}
        return Response(content)

class OrderDetailViewSet(ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        queryset = OrderDetail.objects.all()

        order = self.request.query_params.get('order', None)
        if order is not None:
            queryset = queryset.filter(order=order)
        cuantity = self.request.query_params.get('cuantity', None)
        if cuantity is not None:
            queryset = queryset.filter(cuantity=cuantity)
        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product=product)

        queryset = queryset.order_by('id')

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        orderdetail = []
        for list_elt in request.data:
            if "cuantity" in list_elt:
                if not int(list_elt["cuantity"]) > 0:
                    return Response({"Error": ["Ingrese una Cantidad mayor a 0 (Cero)"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error": ["Ingrese una Cantidad"]}, status=status.HTTP_400_BAD_REQUEST)

            if "order" in list_elt:
                if list_elt["order"] is not None:
                    existeOrder = Order.objects.filter(id=list_elt.get("order"))
                    if existeOrder.count() > 0:
                        list_elt["order"] = Order.objects.get(id=list_elt.get("order"))
                    else:
                        return Response({"Error": ["No existe la orden"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error": ["Ingrese una orden"]}, status=status.HTTP_400_BAD_REQUEST)

            if "product" in list_elt:
                if list_elt["product"] is not None:
                    exiteProducto = Product.objects.filter(id=list_elt.get("product"))

                    if exiteProducto.count() > 0:
                        list_elt["product"] = Product.objects.get(id=list_elt.get("product"))
                    else:
                        return Response({"Error": ["No existe el producto"]}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Error": ["Ingrese un Producto"]}, status=status.HTTP_400_BAD_REQUEST)

            existe = OrderDetail.objects.filter(order=list_elt.get('order'), product=list_elt.get('product'))

            if existe.count() > 0:
                if (list_elt["product"].stock + (existe[0].cuantity - int(list_elt["cuantity"]))) < 0:
                    return Response({"Error": ["No posee el Stock suficiente en el producto"]}, status=status.HTTP_400_BAD_REQUEST)

                with transaction.atomic():
                    exiteProducto.update(stock=list_elt["product"].stock + (existe[0].cuantity - int(list_elt["cuantity"])))
                    existe.update(**list_elt)
            else:
                with transaction.atomic():
                    exiteProducto.update(stock=list_elt["product"].stock-int(list_elt["cuantity"]))
                    OrderDetail.objects.create(**list_elt)

            orderdetail.append(list_elt.get('order'))
        results = OrderDetail.objects.filter(order__in=orderdetail)
        output_serializer = OrderDetailSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                orderdetail = OrderDetail.objects.get(product=request.data["product"], order=request.data["order"])
                exiteProducto = Product.objects.filter(id=orderdetail.product)
                exiteProducto.update(stock=exiteProducto[0].stock + orderdetail.cuantity)
                self.perform_destroy(orderdetail)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderwithDetailsViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderwithDetailsSerializer
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

            if not existe.count() > 0:

                with transaction.atomic():
                    neworder = Order.objects.create(id=list_elt["id"], date_time=list_elt["date_time"])
                    for list_elt_detail in list_elt["order"]:

                        if "product" in list_elt_detail:
                            if list_elt_detail["product"] is not None:
                                exiteProducto = Product.objects.filter(id=list_elt_detail.get("product"))

                                if exiteProducto.count() > 0:
                                    list_elt_detail["product"] = Product.objects.get(id=list_elt_detail.get("product"))
                                else:
                                    return Response({"Error": ["No existe el producto"]},
                                                    status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({"Error": ["Ingrese un Producto"]}, status=status.HTTP_400_BAD_REQUEST)

                        OrderDetail.objects.create(order=neworder, cuantity=list_elt_detail["cuantity"], product=list_elt_detail["product"])
                        exiteProducto.update(stock=list_elt_detail["product"].stock - int(list_elt_detail["cuantity"]))
            else:
                return Response({"Error": ["Ya existe la orden"]}, status=status.HTTP_400_BAD_REQUEST)

            order.append(list_elt.get('id'))
        results = Order.objects.filter(id__in=order)
        output_serializer = OrderwithDetailsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)
