/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-27 16:06:45
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-28 16:23:25
 * @Description overview grafana
 */
import './index.less';
const OverviewList = () => {
  const grafana = `https://grafana.digitalbrain.cn:32443/d/l_ZkLT5Vz
  /ji-qun-jian-kong?orgId=1&from=now-3h&to=now&theme=light&kiosk=tv&refresh=10s `;

  return (
    <div className="overview-list">
      <iframe name="iframe" className="content" src={grafana} />
    </div>
  );
};
export default OverviewList;
