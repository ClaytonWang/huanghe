/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-02-27 10:32:46
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-07 10:32:00
 * @FilePath: /frontend/src/pages/index.js
 * @Description: 页面路由
 */
import { NotebooksPages } from '@/pages/notebooks/routes';
import { JobsPages } from '@/pages/jobs/routes';
import { ServicesPages } from '@/pages/services/routes';

export const Pages = [...NotebooksPages, ...JobsPages, ...ServicesPages];
