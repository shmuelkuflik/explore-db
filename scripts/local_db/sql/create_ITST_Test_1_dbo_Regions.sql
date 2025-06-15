use master
go

create table Regions
(
    Id                    bigint                         not null
        constraint PK_Regions
            primary key
                with (fillfactor = 80),
    CloudIdInt            int                            not null,
    RegionName            nvarchar(64)                   not null,
    RowVersion            int                            not null,
    CreateTime            datetime                       not null,
    LastUpdateTime        datetime                       not null,
    FriendlyName          nvarchar(128)                  not null,
    FlagImageName         nvarchar(128),
    PublicAvailable       bit
        constraint DF_PublicAvailable_Is_False default 0 not null,
    CanCopyToOtherRegions bit default 0                  not null
)
go

