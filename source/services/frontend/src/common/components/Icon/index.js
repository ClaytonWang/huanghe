/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-08 18:14:27
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-09 14:46:06
 * @FilePath: /huanghe/source/services/frontend/src/common/components/Icon/index.js
 * @Description: 自定义图标
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
  running: LoadingSvg,
  pending: PendingSvg,
  error: ErrorFillSvg,
  stopped: StoppedSvg,
  completed: SuccessSvg,
};
export default Icons;
