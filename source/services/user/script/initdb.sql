--1.创建角色表
create table public.bam_role
(
    created_at timestamp,
    updated_at timestamp,
    id         serial
        primary key,
    name       varchar(30) not null
        unique,
    value      varchar(30)
);

comment on column public.bam_role.value is '说明';

alter table public.bam_role
    owner to root;


--2.初始化角色
insert into public.bam_role values (current_timestamp, current_timestamp, 1, 'admin', '超级管理员'),
                                   (current_timestamp, current_timestamp, 2, 'owner', '项目负责人'),
                                   (current_timestamp, current_timestamp, 3, 'user', '普通用户');


--3.创建用户表
create table public.bam_user
(
    id         serial
        primary key,
    created_by integer,
    updated_by integer,
    created_at timestamp default now(),
    updated_at timestamp default now(),
    username   varchar(80)  not null,
    email      varchar(80)  not null
        unique,
    password   varchar(255) not null,
    first_name varchar(20),
    last_name  varchar(60),
    phone      varchar(12),
    is_delete  boolean,
    role       integer
        constraint fk_bam_user_bam_role_id_role
            references public.bam_role,
    en_name    varchar(20)
        unique
);

comment on column public.bam_user.created_by is '创建者';

comment on column public.bam_user.updated_by is '更新者';

comment on column public.bam_user.created_at is '创建日期';

comment on column public.bam_user.updated_at is '更新日期';

comment on column public.bam_user.username is '用户名';

comment on column public.bam_user.email is '邮箱';

comment on column public.bam_user.password is '密码';

comment on column public.bam_user.is_delete is '是否删除';

comment on column public.bam_user.en_name is '英文用户名';

alter table public.bam_user
    owner to root;


--4.初始化admin
insert into public.bam_user values (default, null, null, current_timestamp, current_timestamp, 'admin', 'admin@digitalbrain.cn',
                                    '$2b$12$fq0W0vI3wlZk0MnWSKt1o.Tlpu1sb6Wdpf9144aNaDf1ubAsUG3yG', null, null, null,
                                    false, 1, 'admin'
)


--5.创建项目表
create table public.bam_project
(
    id         serial
        primary key,
    created_by integer,
    updated_by integer,
    created_at timestamp(6) default now(),
    updated_at timestamp(6) default now(),
    code       varchar(80)                                                  not null
        unique,
    name       varchar(80)                                                  not null
        unique,
    owner      integer
        constraint fk_bam_project_bam_user_id_owner
            references public.bam_user,
    en_name    varchar(20)
        unique
);

comment on column public.bam_project.created_by is '创建者';

comment on column public.bam_project.updated_by is '更新者';

comment on column public.bam_project.created_at is '创建日期';

comment on column public.bam_project.updated_at is '更新日期';

comment on column public.bam_project.code is '项目Code';

comment on column public.bam_project.name is '项目名称';

comment on column public.bam_project.en_name is '项目英文名';

alter table public.bam_project
    owner to root;

create index ix_bam_project_id
    on public.bam_project (id);


--项目表many to many
create table public.projects_users
(
    id      serial
        primary key,
    "user"  integer
        constraint fk_projects_users_bam_user_user_id
            references public.bam_user
            on update cascade on delete cascade,
    project integer
        constraint fk_projects_users_bam_project_project_id
            references public.bam_project
            on update cascade on delete cascade
);

alter table public.projects_users
    owner to root;


--6.创建权限表
create table public.bam_permissions
(
    id         serial
        primary key,
    created_by integer,
    updated_by integer,
    created_at timestamp(6) default now(),
    updated_at timestamp(6) default now(),
    code       varchar(20)                                                      not null
        unique,
    name       varchar(30)                                                      not null,
    value      varchar(50),
    uri        json
);

comment on column public.bam_permissions.created_by is '创建者';

comment on column public.bam_permissions.updated_by is '更新者';

comment on column public.bam_permissions.created_at is '创建日期';

comment on column public.bam_permissions.updated_at is '更新日期';

comment on column public.bam_permissions.name is '模块/菜单/操作标题';

comment on column public.bam_permissions.value is '描述';

comment on column public.bam_permissions.uri is '资源（预留）';

alter table public.bam_permissions
    owner to root;

--权限表many to many
create table public.permissionss_roles
(
    id          serial
        primary key,
    role        integer
        constraint fk_permissionss_roles_bam_role_role_id
            references public.bam_role
            on update cascade on delete cascade,
    permissions integer
        constraint fk_permissionss_roles_bam_permissions_permissions_id
            references public.bam_permissions
            on update cascade on delete cascade
);

alter table public.permissionss_roles
    owner to root;


create table public.permissionss_users
(
    id          serial
        primary key,
    "user"      integer
        constraint fk_permissionss_users_bam_user_user_id
            references public.bam_user
            on update cascade on delete cascade,
    permissions integer
        constraint fk_permissionss_users_bam_permissions_permissions_id
            references public.bam_permissions
            on update cascade on delete cascade
);

alter table public.permissionss_users
    owner to root;


--7.初始化权限表
insert into public.bam_permissions values (15,null,null,current_timestamp,current_timestamp,0001,'bam','后台模块', null),
                                          (16,null,null,current_timestamp,current_timestamp,00010001,'projects','项目列表', null),
                                          (17,null,null,current_timestamp,current_timestamp,000100010001,'create','创建', null),
                                          (18,null,null,current_timestamp,current_timestamp,000100010002,'edit','编辑', null),
                                          (19,null,null,current_timestamp,current_timestamp,000100010003,'delete','删除', null),
                                          (20,null,null,current_timestamp,current_timestamp,00010002,'users','用户列表',null),
                                          (21,null,null,current_timestamp,current_timestamp,000100020001,'create','创建', null),
                                          (22,null,null,current_timestamp,current_timestamp,000100020002,'edit','编辑', null),
                                          (23,null,null,current_timestamp,current_timestamp,000100020003,'delete','删除', null),
                                          (24,null,null,current_timestamp,current_timestamp,0002,'settings','设置', null),
                                          (25,null,null,current_timestamp,current_timestamp,00020001,'users','用户列表', null),
                                          (26,null,null,current_timestamp,current_timestamp,000200010001,'create','新建', null),
                                          (27,null,null,current_timestamp,current_timestamp,000200010002,'edit','编辑', null),
                                          (28,null,null,current_timestamp,current_timestamp,000200010003,'delete','删除', null),
                                          (29,null,null,current_timestamp,current_timestamp,0003,'project','项目', null),
                                          (30,null,null,current_timestamp,current_timestamp,00030001,'readonly','查看', null),
                                          (31,null,null,current_timestamp,current_timestamp,00030002,'edit','编辑', null),
                                          (49,null,null,current_timestamp,current_timestamp,0004,'storages','存储', null),
                                          (50,null,null,current_timestamp,current_timestamp,00040001,'list','列表', null),
                                          (51,null,null,current_timestamp,current_timestamp,000400010001,'create','创建', null),
                                          (52,null,null,current_timestamp,current_timestamp,000400010002,'edit','编辑', null),
                                          (53,null,null,current_timestamp,current_timestamp,000400010003,'delete','删除', null),
                                          (54,null,null,current_timestamp,current_timestamp,0005,'notebooks','notebook', null),
                                          (55,null,null,current_timestamp,current_timestamp,00050001,'list','列表', null),
                                          (56,null,null,current_timestamp,current_timestamp,000500010001,'create','创建', null),
                                          (57,null,null,current_timestamp,current_timestamp,000500010002,'edit','编辑', null),
                                          (58,null,null,current_timestamp,current_timestamp,000500010003,'delete','删除', null);


--8.初始化角色权限表
insert into public.permissionss_roles values (default,1,15),
                                             (default,1,16),
                                             (default,1,17),
                                             (default,1,18),
                                             (default,1,19),
                                             (default,1,20),
                                             (default,1,21),
                                             (default,1,22),
                                             (default,1,23),
                                             (default,2,24),
                                             (default,2,25),
                                             (default,2,26),
                                             (default,2,27),
                                             (default,2,28),
                                             (default,1,49),
                                             (default,2,49),
                                             (default,3,49),
                                             (default,1,50),
                                             (default,2,50),
                                             (default,3,50),
                                             (default,1,51),
                                             (default,2,51),
                                             (default,3,51),
                                             (default,1,52),
                                             (default,2,52),
                                             (default,3,52),
                                             (default,1,53),
                                             (default,2,53),
                                             (default,3,53),
                                             (default,1,54),
                                             (default,2,54),
                                             (default,3,54),
                                             (default,1,55),
                                             (default,2,55),
                                             (default,3,55),
                                             (default,1,56),
                                             (default,2,56),
                                             (default,3,56),
                                             (default,1,57),
                                             (default,2,57),
                                             (default,3,57),
                                             (default,1,58),
                                             (default,2,58),
                                             (default,3,58);


--9.创建功能权限表
create table public.bam_pms_operation
(
    id         serial
        primary key,
    created_by integer,
    updated_by integer,
    created_at timestamp(6) default now(),
    updated_at timestamp(6) default now(),
    project    integer
        constraint fk_bam_pms_operation_bam_project_id_project
            references public.bam_project,
    "user"     integer
        constraint fk_bam_pms_operation_bam_user_id_user
            references public.bam_user
);

comment on column public.bam_pms_operation.created_by is '创建者';

comment on column public.bam_pms_operation.updated_by is '更新者';

comment on column public.bam_pms_operation.created_at is '创建日期';

comment on column public.bam_pms_operation.updated_at is '更新日期';

alter table public.bam_pms_operation
    owner to root;


--功能权限表many to many
create table public.operationpmss_permissionss
(
    id           serial
        primary key,
    permissions  integer
        constraint fk_operationpmss_permissionss_bam_permissions_permissions_id
            references public.bam_permissions
            on update cascade on delete cascade,
    operationpms integer
        constraint fk_operationpmss_permissionss_bam_pms_operation_operationpms_id
            references public.bam_pms_operation
            on update cascade on delete cascade
);

alter table public.operationpmss_permissionss
    owner to root;

