--1.创建镜像表
create table public.bam_image
(
    created_at timestamp(6),
    updated_at timestamp(6),
    id         serial
        primary key,
    name       varchar(100)                                          not null
        unique,
    "desc"     varchar(80)
);

alter table public.bam_image
    owner to root;


--2.初始化镜像
insert into public.bam_image values (current_timestamp, current_timestamp, default, 'kubeflownotebookswg/jupyter-scipy:v1.6.1','真实镜像'),
                                    (current_timestamp, current_timestamp, default, 'swr.cn-north-4.myhuaweicloud.com/digitalbrain/notebook-server-yunchou:v0.1','jupyter占军0111');


--3.创建状态表
create table public.bam_status
(
    id     serial
        primary key,
    code   varchar(20)                                            not null
        unique,
    name   varchar(20)                                            not null
        unique,
    "desc" varchar(40)                                            not null
);

alter table public.bam_status
    owner to root;


--4.初始化状态
insert into public.bam_status values (default,01,'start','启动中'),
                                     (default,02,'stop','停止中'),
                                     (default,03,'pending','排队中'),
                                     (default,04,'running','已启动'),
                                     (default,05,'stopped','已停止'),
                                     (default,06,'error','异常');


--5.创建资源表
create table public.bam_source
(
    created_at timestamp(6),
    updated_at timestamp(6),
    id         serial
        primary key,
    cpu        integer                                                not null,
    memory     integer                                                not null,
    gpu        integer                                                not null,
    "desc"     varchar(80),
    type       varchar(20)
);

comment on column public.bam_source.cpu is 'CPU数量';

comment on column public.bam_source.memory is '存储容量G';

comment on column public.bam_source.gpu is 'GPU数量';

alter table public.bam_source
    owner to root;


--6.初始化资源
insert into public.bam_source values (current_timestamp,current_timestamp,default,2,4,0,'纯c','cpu'),
                                     (current_timestamp,current_timestamp,default,4,8,0,'纯c1','cpu'),
                                     (current_timestamp,current_timestamp,default,8,16,0,'纯c2','cpu'),
                                     (current_timestamp,current_timestamp,default,12,24,0,'纯c3','cpu'),
                                     (current_timestamp,current_timestamp,default,6,12,1,null,'T4'),
                                     (current_timestamp,current_timestamp,default,12,24,2,null,'T4');


--7.创建notebook表
create table public.bam_notebook
(
    created_at timestamp(6),
    updated_at timestamp(6),
    id         serial
        primary key,
    name       varchar(20)                                              not null,
    status     integer
        constraint fk_bam_notebook_bam_status_id_status
            references public.bam_status,
    source     integer
        constraint fk_bam_notebook_bam_source_id_source
            references public.bam_source,
    creator_id integer                                                  not null,
    project_id integer                                                  not null,
    image_id   integer                                                  not null,
    storage    json                                                     not null,
    url        varchar(160),
    k8s_info   json
);

comment on column public.bam_notebook.creator_id is '创建者id';

comment on column public.bam_notebook.project_id is '项目id';

comment on column public.bam_notebook.image_id is '镜像id';

comment on column public.bam_notebook.storage is '存储信息';

alter table public.bam_notebook
    owner to root;

