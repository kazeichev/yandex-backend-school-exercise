from datetime import datetime
from django.db.models import Q
from rest.models import Order, Courier, CourierWorkingHour, CourierOrder, OrderDeliveryHour


class CourierManager:
    @staticmethod
    def create(courier_id, courier_type, regions, working_hours):
        courier = Courier.objects.create(
            courier_id=courier_id,
            courier_type=courier_type,
            regions=regions
        )

        for hours in working_hours:
            splitted_hours = hours.split("-")
            CourierWorkingHour.objects.create(
                courier=courier,
                start_time=splitted_hours[0],
                end_time=splitted_hours[1]
            )

        return courier

    @staticmethod
    def get_started_orders(courier_id):
        return CourierOrder.objects \
            .filter(courier=courier_id, assign_time__isnull=False, complete_time__isnull=True) \
            .order_by('assign_time')\
            .all()


class OrderManager:
    @staticmethod
    def create(order_id, weight, region, delivery_hours):
        order = Order.objects.create(
            order_id=order_id,
            weight=weight,
            region=region
        )

        for time in delivery_hours:
            hours = time.split("-")
            OrderDeliveryHour.objects.create(
                order=order,
                start_time=hours[0],
                end_time=hours[1]
            )

        return order

    @staticmethod
    def get_orders_to_assign(courier_id):
        try:
            courier = Courier.objects.get(courier_id=courier_id)
        except Exception:
            raise ValueError("Передан некорректный id курьера")

        working_hours = CourierWorkingHour.objects.filter(courier=courier).all()

        if working_hours is None:
            raise ValueError("У курьера нет рабочих часов")

        orders_filter = Order.objects.filter(
            weight__lt=courier.get_max_weight(),
            region__in=courier.regions,
            courierorder__assign_time__isnull=True,
            courierorder__complete_time__isnull=True
        )

        hours_query = Q()

        for hours in working_hours:
            hours_query = hours_query | (
                    Q(orderdeliveryhour__start_time__range=(hours.start_time, hours.end_time)) |
                    Q(orderdeliveryhour__end_time__range=(hours.start_time, hours.end_time))
            )

        hours_filter = Order.objects.filter(hours_query)
        orders = (orders_filter & hours_filter).distinct().order_by('weight')

        return list(orders.all())

    @staticmethod
    def assign_orders_to_courier(courier_id, orders):
        try:
            courier = Courier.objects.get(courier_id=courier_id)
        except Exception:
            raise ValueError("Передан некорректный id курьера")

        assigned_order_ids = []
        free_weight = courier.get_free_weight()
        started_orders = CourierManager.get_started_orders(courier_id)

        if started_orders.count() > 0:
            assign_time = started_orders.last().assign_time
        else:
            assign_time = datetime.now()

        while free_weight > 0 and len(orders) > 0:
            order = orders.pop()

            if free_weight - order.weight >= 0:
                free_weight -= order.weight
                CourierOrderManager.create(courier, order, assign_time)
                assigned_order_ids.append({"id": order.order_id})

        if len(assigned_order_ids) > 0:
            response = {
                "orders": assigned_order_ids,
                "assign_time": assign_time.isoformat()
            }
        else:
            response = {
                "orders": []
            }

        return response


class CourierOrderManager:
    @staticmethod
    def create(courier, order, assign_time=None, complete_time=None):
        return CourierOrder.objects.create(
            courier=courier,
            order=order,
            assign_time=assign_time if assign_time is not None else datetime.now(),
            complete_time=complete_time
        )
