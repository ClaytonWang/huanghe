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
  running: SuccessSvg,
  pending: LoadingSvg,
  error: ErrorFillSvg,
  stopped: StoppedSvg,
};
export default Icons;
