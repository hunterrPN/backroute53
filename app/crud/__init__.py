from .user import (
    create_user,
    get_user_by_email,
    get_user          # Yeh ab add ho gaya
)

from .hosted_zone import (
    get_hosted_zones,
    get_hosted_zone,
    create_hosted_zone,
    update_hosted_zone,
    delete_hosted_zone
)

from .record import (
    get_records_by_zone,
    create_record,
    get_record,
    update_record,
    delete_record
)