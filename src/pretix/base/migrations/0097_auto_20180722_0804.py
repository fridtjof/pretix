# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-22 08:04
from __future__ import unicode_literals

from django.db import migrations


def create_payments(apps, schema_editor):
    Order = apps.get_model('pretixbase', 'Order')  # noqa
    OrderPayment = apps.get_model('pretixbase', 'OrderPayment')  # noqa
    OrderRefund = apps.get_model('pretixbase', 'OrderRefund')  # noqa
    payments = []
    refunds = []
    for o in Order.objects.filter(payments__isnull=True).iterator():
        if o.status == 'n' or o.status == 'e':
            payments.append(OrderPayment(
                local_id=1,
                state='created',
                amount=o.total,
                order=o,
                provider=o.payment_provider,
                info=o.payment_info,
                migrated=True,
                fee=o.fees.filter(fee_type="payment", internal_type=o.payment_provider).first(),
            ))
            pass
        elif o.status == 'p':
            payments.append(OrderPayment(
                local_id=1,
                state='confirmed',
                amount=o.total,
                order=o,
                provider=o.payment_provider,
                payment_date=o.payment_date,
                info=o.payment_info,
                migrated=True,
                fee=o.fees.filter(fee_type="payment", internal_type=o.payment_provider).first(),
            ))
        elif o.status == 'r':
            p = OrderPayment.objects.create(
                local_id=1,
                state='refunded',
                amount=o.total,
                order=o,
                provider=o.payment_provider,
                payment_date=o.payment_date,
                info=o.payment_info,
                migrated=True,
                fee=o.fees.filter(fee_type="payment", internal_type=o.payment_provider).first(),
            )
            refunds.append(OrderRefund(
                local_id=1,
                state='done',
                amount=o.total,
                order=o,
                provider=o.payment_provider,
                info=o.payment_info,
                source='admin',
                payment=p
            ))
        elif o.status == 'c':
            payments.append(OrderPayment(
                local_id=1,
                state='canceled',
                amount=o.total,
                order=o,
                provider=o.payment_provider,
                payment_date=o.payment_date,
                info=o.payment_info,
                migrated=True,
                fee=o.fees.filter(fee_type="payment", internal_type=o.payment_provider).first(),
            ))

        if len(payments) > 500:
            OrderPayment.objects.bulk_create(payments)
            payments.clear()
        if len(refunds) > 500:
            OrderRefund.objects.bulk_create(refunds)
            refunds.clear()
    if len(payments) > 0:
        OrderPayment.objects.bulk_create(payments)
    if len(refunds) > 0:
        OrderRefund.objects.bulk_create(refunds)


def notifications(apps, schema_editor):
    NotificationSetting = apps.get_model('pretixbase', 'NotificationSetting')
    for n in NotificationSetting.objects.filter(action_type='pretix.event.action_required'):
        n.pk = None
        n.action_type = 'pretix.event.order.refund.created.externally'
        n.save()


class Migration(migrations.Migration):
    dependencies = [
        ('pretixbase', '0096_auto_20180722_0801'),
    ]

    operations = [
        migrations.RunPython(create_payments, migrations.RunPython.noop),
        migrations.RunPython(notifications, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='order',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_info',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_manual',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_provider',
        ),
    ]