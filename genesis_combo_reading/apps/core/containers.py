from dependency_injector import containers, providers

from genesis_combo_reading.apps.core.service.reading_encryption import ComboReadingEncryptionServiceImpl
from genesis_combo_reading.apps.core.service.reading_encryption_config import ComboReadingEncryptionConfig
from genesis_combo_reading.apps.core.service.reading_processing import ComboReadingProcessingServiceImpl
from genesis_combo_reading.apps.core.views.get_gateway_data import GetGatewayDataView


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    encryption_config = providers.Factory(
        ComboReadingEncryptionConfig,
        enable_encryption=config.READING_ENABLE_ENCRYPTION,
        secret=config.READING_ENCRYPTION_KEY,
        executable_dir=config.ENCRYPTION_BINARY_DIRECTORY
    )
    reading_encryption_service = providers.Factory(
        ComboReadingEncryptionServiceImpl,
        config=encryption_config
    )
    reading_processing_service = providers.Factory(
        ComboReadingProcessingServiceImpl,
        encryption_service=reading_encryption_service
    )

    view = GetGatewayDataView.as_view(reading_processing_service=reading_processing_service())

    get_gateway_data_view = providers.Object(view)
