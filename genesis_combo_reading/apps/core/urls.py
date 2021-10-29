from django.conf.urls import url

from genesis_combo_reading import container


urlpatterns = [
    url(r'^DeliverData/GetGatewayData.aspx$',
        container.get_gateway_data_view(),
        name="get_gateway_data"),
    url(r'^DeliverData/GatewayAPI.aspx$',
        container.gateway_view(),
        name="gateway")
]
