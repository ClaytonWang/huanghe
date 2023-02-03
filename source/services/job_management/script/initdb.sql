--1.创建JOB表
CREATE TABLE "public"."bam_job" (
                                    "id" int4 NOT NULL DEFAULT nextval('bam_job_id_seq'::regclass),
                                    "created_at" timestamp(6) DEFAULT now(),
                                    "updated_at" timestamp(6) DEFAULT now(),
                                    "created_by_id" int4 NOT NULL,
                                    "project_by_id" int4 NOT NULL,
                                    "deleted_at" timestamp(6),
                                    "updated_by_id" int4,
                                    "updated_by" varchar COLLATE "pg_catalog"."default",
                                    "created_by" varchar COLLATE "pg_catalog"."default",
                                    "create_en_by" varchar COLLATE "pg_catalog"."default",
                                    "project_en_by" varchar COLLATE "pg_catalog"."default",
                                    "name" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
                                    "storage" json NOT NULL,
                                    "task_model" int2 DEFAULT 0,
                                    "start_command" text COLLATE "pg_catalog"."default",
                                    "image_type" int2 DEFAULT 0,
                                    "image_name" varchar(100) COLLATE "pg_catalog"."default",
                                    "status" int4,
                                    "work_dir" varchar(100) COLLATE "pg_catalog"."default",
                                    "source_id" int4,
                                    "project_by" varchar COLLATE "pg_catalog"."default",
                                    "k8s_info" json,
                                    CONSTRAINT "bam_job_pkey" PRIMARY KEY ("id"),
                                    CONSTRAINT "bam_job_status_fkey" FOREIGN KEY ("status") REFERENCES "public"."bam_status" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
)
;

ALTER TABLE "public"."bam_job"
    OWNER TO "root";

COMMENT ON COLUMN "public"."bam_job"."created_by_id" IS '创建者id';

COMMENT ON COLUMN "public"."bam_job"."project_by_id" IS '项目id';

COMMENT ON COLUMN "public"."bam_job"."name" IS '名称';

COMMENT ON COLUMN "public"."bam_job"."storage" IS '存储信息';

COMMENT ON COLUMN "public"."bam_job"."task_model" IS '任务模式，0：调试，1：非调试';

COMMENT ON COLUMN "public"."bam_job"."start_command" IS '启动命令';

COMMENT ON COLUMN "public"."bam_job"."image_type" IS '镜像类型，0：官方镜像，1：自定义镜像';

COMMENT ON COLUMN "public"."bam_job"."image_name" IS '镜像名称';

COMMENT ON COLUMN "public"."bam_job"."work_dir" IS '工作目录';

COMMENT ON COLUMN "public"."bam_job"."source_id" IS 'source表id逻辑关联';

--2.创建bam_job序列
CREATE SEQUENCE "public"."bam_job_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

SELECT setval('"public"."bam_job_id_seq"', 1, true);

ALTER SEQUENCE "public"."bam_job_id_seq"
OWNED BY "public"."bam_job"."id";

ALTER SEQUENCE "public"."bam_job_id_seq" OWNER TO "root";