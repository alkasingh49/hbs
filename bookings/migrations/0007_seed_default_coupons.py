from django.db import migrations


DEFAULT_COUPONS = [
    ('WELCOME10', 10),
    ('SUMMER15', 15),
    ('STAY20', 20),
]


def create_default_coupons(apps, schema_editor):
    Coupon = apps.get_model('bookings', 'Coupon')

    for code, discount_percent in DEFAULT_COUPONS:
        Coupon.objects.get_or_create(
            code=code,
            defaults={
                'discount_percent': discount_percent,
                'active': True,
            },
        )


def remove_default_coupons(apps, schema_editor):
    Coupon = apps.get_model('bookings', 'Coupon')
    Coupon.objects.filter(code__in=[code for code, _ in DEFAULT_COUPONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_coupon_booking_discount_percent_booking_coupon'),
    ]

    operations = [
        migrations.RunPython(create_default_coupons, remove_default_coupons),
    ]
