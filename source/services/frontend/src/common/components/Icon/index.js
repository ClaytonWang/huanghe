/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-01-31 16:21:26
 * @FilePath: /frontend/src/common/components/Icon/index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-24 15:53:57
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-11-24 16:00:46
 * @Description 自定义图标
 */

import BAMSvg from '@/common/images/BAM.svg';
import SettingsSvg from '@/common/images/Settings.svg';
import StorageSvg from '@/common/images/storages.svg';
import UserSvg from '@/common/images/user.svg';
import DataSvg from '@/common/images/data.svg';
import CustomSvg from '@/common/images/custom.svg';
import DevelopSvg from '@/common/images/develop.svg';
import JupyterSvg from '@/common/images/jupyter.svg';
import SuccessSvg from '@/common/images/success.svg';
import LoadingSvg from '@/common/images/loading.svg';
import PendingSvg from '@/common/images/pending.svg';
import ErrorFillSvg from '@/common/images/error-fill.svg';
import StoppedSvg from '@/common/images/stopped.svg';
import OverviewSvg from '@/common/images/Overview.svg';

const Icons = {
  overview: OverviewSvg,
  bam: BAMSvg,
  settings: SettingsSvg,
  storages: StorageSvg,
  account: UserSvg,
  data: DataSvg,
  custom: CustomSvg,
  develop: DevelopSvg,
  notebooks: JupyterSvg,
  jobs: JupyterSvg,
  start: LoadingSvg,
  stop: LoadingSvg,
  running: SuccessSvg,
  pending: PendingSvg,
  error: ErrorFillSvg,
  stopped: StoppedSvg,
};
export default Icons;
