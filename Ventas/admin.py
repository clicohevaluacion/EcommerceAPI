# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.utils.html import format_html
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        return qs


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time')
    list_filter = ('date_time',)
    search_fields = ('date_time',)
    ordering = ('id',)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'cuantity', 'product')
    list_filter = ('product',)
    search_fields = ('product',)
    ordering = ('order',)

    def get_queryset(self, request):
        qs = super(OrderDetailAdmin, self).get_queryset(request)
        return qs
