/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 18:03:06
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-01 18:11:48
 * @FilePath: /huanghe/source/services/frontend/src/common/components/Monitor/index.js
 * @Description: 监控公共组建
 */
const ChartMonitor = ({ url }) => {
  const grafana =
    url ??
    `https://grafana.digitalbrain.cn:32443/d/l_ZkLT5Vz
  /ji-qun-jian-kong?orgId=1&from=now-3h&to=now&theme=light&kiosk=tv&refresh=10s `;

  return (
    <div className="overview-list">
      <iframe name="iframe" className="content" src={grafana} />
    </div>
  );
};

export default ChartMonitor;
