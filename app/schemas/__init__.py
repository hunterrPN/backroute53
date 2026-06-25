from .user import (
    UserBase,
    UserCreate,
    UserLogin,           # ← Yeh sahi hai
    Token,
    TokenData,
    UserResponse
)

from .hosted_zone import (
    HostedZoneBase,
    HostedZoneCreate,
    HostedZoneUpdate,
    HostedZoneResponse
)

from .record import (
    RecordBase,
    RecordCreate,
    RecordUpdate,
    RecordResponse
)