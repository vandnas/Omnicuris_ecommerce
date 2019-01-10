from django.conf.urls import patterns, include, url

urlpatterns = patterns('ecommerce_app.views',
    url(r'^add_item/', 'upsert_in_item_table', name = 'upsert_item'),
    url(r'^delete_item/', 'delete_entry_from_item_table', name = 'delete_item'),
    url(r'^get_item/(\w+)/', 'get_entry_from_item_table', name = 'get_item'),
    url(r'^get_all_items/', 'get_entries_from_item_table', name = 'select_items'),
    url(r'^get_all_orders/', 'get_entries_from_order_table', name = 'select_orders'),
    url(r'^place_single_order/', 'insert_in_order_table', name = 'insert_order'),
    url(r'^place_bulk_order/', 'save_bulk_order_in_db', name = 'bulk_order'),
    )
